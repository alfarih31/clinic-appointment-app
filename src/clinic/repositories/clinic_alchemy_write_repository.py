from typing import List, Annotated

from dihub.decorators import provider, inject
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.clinic.constants import CLINIC_WRITE_REPOSITORY
from src.clinic.models import ClinicAlchemyModel, ClinicAdminAlchemyModel
from src.clinic.types import IClinicAlchemyWriteRepository, FindAllParams
from src.sql_alchemy import EngineProvider


@provider(token=CLINIC_WRITE_REPOSITORY)
class ClinicAlchemyWriteRepository(IClinicAlchemyWriteRepository):
    engine: Annotated[EngineProvider, inject(EngineProvider)]

    def insert(self, clinic: ClinicAlchemyModel):
        with Session(self.engine.engine) as session:
            session.add(clinic)

            session.commit()

    def find_all(self, params: FindAllParams) -> List[ClinicAlchemyModel]:
        with Session(self.engine.engine) as session:
            where_params = []
            if params.user_id is not None:
                where_params.append(ClinicAdminAlchemyModel.user_id == params.user_id)

            if params.name is not None:
                where_params.append(ClinicAlchemyModel.name.ilike("%{}%".format(params.name)))

            stmt = select(ClinicAdminAlchemyModel).where(*where_params).join(ClinicAdminAlchemyModel.clinic)

            results = session.scalars(stmt).all()
            return [r.clinic for r in results]

    def count_clinic_admin(self, user_id: int, clinic_id: int) -> int:
        with Session(self.engine.engine) as session:
            stmt = select(ClinicAdminAlchemyModel.id).where(ClinicAdminAlchemyModel.user_id == user_id,
                                                            ClinicAdminAlchemyModel.clinic_id == clinic_id)

            results = session.scalars(stmt).all()

            return len(results)
