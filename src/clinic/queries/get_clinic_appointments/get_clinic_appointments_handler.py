from dihub.decorators import inject
from dihub_cqrs.decorators import query_handler

from src.clinic.clinic_exceptions import UserNotTheClinicAdmins
from src.clinic.constants import CLINIC_WRITE_REPOSITORY, APPOINTMENT_WRITE_REPOSITORY
from src.clinic.types import IClinicAlchemyWriteRepository, IAppointmentAlchemyWriteRepository
from .get_clinic_appointments_query import GetClinicAppointmentsQuery
from .get_clinic_appointments_result import GetClinicAppointmentsResult, ClinicAppointmentsResultProps


@query_handler(GetClinicAppointmentsQuery, GetClinicAppointmentsResult)
class GetClinicAppointmentsHandler:
    clinic_write_repo: IClinicAlchemyWriteRepository = inject(CLINIC_WRITE_REPOSITORY)
    appointment_write_repo: IAppointmentAlchemyWriteRepository = inject(APPOINTMENT_WRITE_REPOSITORY)

    async def handle(self, query: GetClinicAppointmentsQuery) -> GetClinicAppointmentsResult:
        admin_count = self.clinic_write_repo.count_clinic_admin(query.admin_user_id, query.clinic_id)
        if admin_count == 0:
            raise UserNotTheClinicAdmins()

        rows = await self.appointment_write_repo.find_all(IAppointmentAlchemyWriteRepository.FindAllParams(clinic_id=query.clinic_id))

        return GetClinicAppointmentsResult(
            appointments=[ClinicAppointmentsResultProps(id=r.id, patient_id=r.patient_id, queue=r.queue, promised_start_date=r.promised_start_date)
                          for r in rows])
