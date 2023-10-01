from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared import BaseAlchemyModel


class PatientAlchemyModel(BaseAlchemyModel):
    __tablename__ = "patient"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    clinic_id: Mapped[int] = mapped_column(ForeignKey("clinic.id"))

    user = relationship("UserAlchemyModel", back_populates="clinic_patients")
    clinic = relationship("ClinicAlchemyModel", back_populates="patients")
    appointments = relationship("AppointmentAlchemyModel", back_populates="patient")
