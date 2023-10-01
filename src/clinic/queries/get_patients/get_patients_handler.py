from dihub.decorators import inject
from dihub_cqrs.decorators import query_handler

from src.clinic.clinic_exceptions import UserNotTheClinicAdmins
from src.clinic.constants import CLINIC_WRITE_REPOSITORY, PATIENT_WRITE_REPOSITORY
from src.clinic.types import IPatientAlchemyWriteRepository, IClinicAlchemyWriteRepository
from .get_patients_query import GetPatientsQuery
from .get_patients_result import GetPatientsResult, PatientResultProps

FindAllParams = IPatientAlchemyWriteRepository.FindAllParams


@query_handler(GetPatientsQuery, GetPatientsResult)
class GetPatientsHandler:
    patient_write_repo: IPatientAlchemyWriteRepository = inject(PATIENT_WRITE_REPOSITORY)
    clinic_write_repo: IClinicAlchemyWriteRepository = inject(CLINIC_WRITE_REPOSITORY)

    async def handle(self, query: GetPatientsQuery) -> GetPatientsResult:
        admin_count = self.clinic_write_repo.count_clinic_admin(query.admin_user_id, query.clinic_id)
        if admin_count == 0:
            raise UserNotTheClinicAdmins()

        rows = self.patient_write_repo.find_all(FindAllParams(user_full_name=query.user_full_name, clinic_id=query.clinic_id))

        return GetPatientsResult(patients=[PatientResultProps(id=r.id, user_id=r.user_id, user_full_name=r.user.full_name) for r in rows])
