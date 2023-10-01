from dihub.decorators import inject
from dihub_cqrs.decorators import query_handler

from src.clinic.clinic_exceptions import UserNotTheClinicPatients
from src.clinic.constants import CLINIC_WRITE_REPOSITORY, APPOINTMENT_WRITE_REPOSITORY, PATIENT_WRITE_REPOSITORY
from src.clinic.types import IClinicAlchemyWriteRepository, IAppointmentAlchemyWriteRepository, IPatientAlchemyWriteRepository
from .get_patient_appointments_query import GetPatientAppointmentsQuery
from .get_patient_appointments_result import GetPatientAppointmentsResult, PatientAppointmentsResultProps


@query_handler(GetPatientAppointmentsQuery, GetPatientAppointmentsResult)
class GetPatientAppointmentsHandler:
    patient_write_repo: IPatientAlchemyWriteRepository = inject(PATIENT_WRITE_REPOSITORY)
    clinic_write_repo: IClinicAlchemyWriteRepository = inject(CLINIC_WRITE_REPOSITORY)
    appointment_write_repo: IAppointmentAlchemyWriteRepository = inject(APPOINTMENT_WRITE_REPOSITORY)

    async def handle(self, query: GetPatientAppointmentsQuery) -> GetPatientAppointmentsResult:
        patient = await self.patient_write_repo.find_by_user_and_clinic_id(query.patient_user_id, query.clinic_id)
        if patient is None:
            raise UserNotTheClinicPatients()

        rows = await self.appointment_write_repo.find_all(IAppointmentAlchemyWriteRepository.FindAllParams(patient_id=patient.id))

        return GetPatientAppointmentsResult(
            appointments=[PatientAppointmentsResultProps(id=r.id, patient_id=r.patient_id, queue=r.queue, promised_start_date=r.promised_start_date)
                          for r in rows])
