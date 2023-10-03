from datetime import datetime
from inspect import getmembers
from typing import Optional, List, Annotated

from dihub.decorators import inject, provider
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncConnection
from sqlalchemy.orm import MappedColumn
from sqlalchemy.types import DATE

from src.clinic.constants import APPOINTMENT_WRITE_REPOSITORY
from src.clinic.models import AppointmentAlchemyModel, AppointmentStatus, PatientAlchemyModel
from src.clinic.types import IAppointmentAlchemyWriteRepository
from src.sql_alchemy.engine_provider import EngineProvider

FindAllParams = IAppointmentAlchemyWriteRepository.FindAllParams


@provider(token=APPOINTMENT_WRITE_REPOSITORY)
class AppointmentAlchemyWriteRepository(IAppointmentAlchemyWriteRepository):
    engine: Annotated[EngineProvider, inject(EngineProvider)]

    async def insert(self, appointment: AppointmentAlchemyModel):
        async with async_sessionmaker(bind=self.engine.async_engine).begin() as session:
            session.add(appointment)

            await session.commit()

    async def find_last_appointment_in_day(self, date: datetime) -> Optional[AppointmentAlchemyModel]:
        async with self.engine.async_engine.connect() as session:
            if isinstance(session, AsyncConnection):
                stmt = select(AppointmentAlchemyModel).where(AppointmentAlchemyModel.promised_start_date.cast(DATE) == date.date()).order_by(
                    AppointmentAlchemyModel.queue.desc()).limit(1)

                result = await session.execute(stmt)
                return result.first()

    async def count_conflict_appointment(self, promised_start_date: datetime, estimated_end_date: datetime) -> int:
        async with self.engine.async_engine.connect() as session:
            if isinstance(session, AsyncConnection):
                stmt = select(AppointmentAlchemyModel.id). \
                    where(or_(
                    and_(AppointmentAlchemyModel.promised_start_date <= promised_start_date,
                         promised_start_date <= AppointmentAlchemyModel.estimated_end_date),
                    and_(AppointmentAlchemyModel.promised_start_date <= estimated_end_date,
                         estimated_end_date <= AppointmentAlchemyModel.estimated_end_date)),
                    AppointmentAlchemyModel.status_id == AppointmentStatus.QUEUED.value). \
                    order_by(AppointmentAlchemyModel.queue.desc())

                result = await session.execute(stmt)

                return len(result.scalars().all())

    async def update(self, appointment: AppointmentAlchemyModel):
        async with async_sessionmaker(bind=self.engine.async_engine).begin() as session:
            select_stmt = select(AppointmentAlchemyModel).where(AppointmentAlchemyModel.id == appointment.id).limit(1)

            curr = await session.scalars(select_stmt)
            old_appointment = curr.one()

            for attr_name, attr_value in getmembers(appointment, predicate=lambda x: isinstance(x, MappedColumn)):
                setattr(old_appointment, attr_name, attr_value)

            await session.commit()

    async def find_by_id(self, id: int) -> Optional[AppointmentAlchemyModel]:
        async with self.engine.async_engine.connect() as session:
            if isinstance(session, AsyncConnection):
                stmt = select(AppointmentAlchemyModel).where(AppointmentAlchemyModel.id == id).limit(1)

                result = await session.execute(stmt)
                return result.first()

    async def find_all(self, params: FindAllParams) -> List[AppointmentAlchemyModel]:
        async with async_sessionmaker(bind=self.engine.async_engine)() as session:
            where_params = []
            if params.clinic_id is not None:
                where_params.append(PatientAlchemyModel.clinic_id == params.clinic_id)

            if params.patient_id is not None:
                where_params.append(AppointmentAlchemyModel.patient_id == params.patient_id)
            stmt = select(AppointmentAlchemyModel).where(*where_params).join(AppointmentAlchemyModel.patient)

            curr = await session.scalars(stmt)
            results = curr.all()
            return [r for r in results]
