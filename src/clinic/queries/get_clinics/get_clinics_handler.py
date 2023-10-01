from dihub.decorators import inject
from dihub_cqrs.decorators import query_handler

from src.clinic.constants import CLINIC_WRITE_REPOSITORY
from src.clinic.types import IClinicAlchemyWriteRepository, FindAllParams
from .get_clinics_query import GetClinicsQuery
from .get_clinics_result import GetClinicsResult, ClinicResultProps


@query_handler(GetClinicsQuery, GetClinicsResult)
class GetClinicsHandler:
    clinic_write_repo: IClinicAlchemyWriteRepository = inject(CLINIC_WRITE_REPOSITORY)

    async def handle(self, query: GetClinicsQuery) -> GetClinicsResult:
        rows = self.clinic_write_repo.find_all(FindAllParams(user_id=query.user_id, name=query.name))

        return GetClinicsResult(clinics=[ClinicResultProps(id=r.id, name=r.name) for r in rows])
