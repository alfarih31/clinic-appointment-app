from typing import List, Optional

from dihub.decorators import inject, provider
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.orm import Session

from src.auth.models import UserAlchemyModel
from src.clinic.constants import PATIENT_WRITE_REPOSITORY
from src.clinic.models import PatientAlchemyModel
from src.clinic.types import IPatientAlchemyWriteRepository
from src.sql_alchemy import EngineProvider

FindAllParams = IPatientAlchemyWriteRepository.FindAllParams


@provider(token=PATIENT_WRITE_REPOSITORY)
class PatientAlchemyWriteRepository(IPatientAlchemyWriteRepository):
    engine: EngineProvider = inject(EngineProvider)

    def insert(self, patient: PatientAlchemyModel):
        with Session(self.engine.engine) as session:
            session.add(patient)

            session.commit()

    def count_patient(self, user_id: int, clinic_id) -> int:
        with Session(self.engine.engine) as session:
            stmt = select(PatientAlchemyModel.id).where(PatientAlchemyModel.user_id == user_id, PatientAlchemyModel.clinic_id == clinic_id)

            results = session.scalars(stmt).all()
            return len(results)

    def find_all(self, params: FindAllParams) -> List[PatientAlchemyModel]:
        with Session(self.engine.engine) as session:
            where_params = []

            if params.clinic_id is not None:
                where_params.append(PatientAlchemyModel.clinic_id == params.clinic_id)
            if params.user_full_name is not None:
                where_params.append(UserAlchemyModel.full_name.ilike("%{}%".format(params.user_full_name)))

            stmt = select(PatientAlchemyModel).where(*where_params).join(PatientAlchemyModel.user)
            results = session.scalars(stmt).all()

            return [r.detach_relationship() for r in results]

    async def find_by_user_and_clinic_id(self, user_id: int, clinic_id: int) -> Optional[PatientAlchemyModel]:
        async with self.engine.async_engine.connect() as session:
            if isinstance(session, AsyncConnection):
                stmt = select(PatientAlchemyModel).where(PatientAlchemyModel.user_id == user_id, PatientAlchemyModel.clinic_id == clinic_id).limit(1)

                result = await session.execute(stmt)
                return result.first()
