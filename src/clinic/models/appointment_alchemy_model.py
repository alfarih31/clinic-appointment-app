from datetime import datetime
from enum import Enum

from dihub.decorators import provider
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import SMALLINT, TIMESTAMP

from src.clinic.constants import APPOINTMENT_WRITE_REPOSITORY
from src.shared import BaseAlchemyModel


class AppointmentStatus(Enum):
    QUEUED = 1
    FULFILLED = 2
    COMPLETED = 3
    CANCELLED = 4


@provider(token=APPOINTMENT_WRITE_REPOSITORY)
class AppointmentAlchemyModel(BaseAlchemyModel):
    __tablename__ = "appointment"

    queue: Mapped[int] = mapped_column(SMALLINT)
    status_id: Mapped[AppointmentStatus] = mapped_column(SMALLINT, default=AppointmentStatus.QUEUED.value)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    promised_start_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    estimated_end_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    promised_duration: Mapped[int] = mapped_column(SMALLINT)

    patient = relationship("PatientAlchemyModel", back_populates="appointments")
