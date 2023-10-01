from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import VARCHAR

from src.shared import BaseAlchemyModel


class ClinicAlchemyModel(BaseAlchemyModel):
    __tablename__ = "clinic"

    name: Mapped[str] = mapped_column(VARCHAR(length=255))
    slug: Mapped[str] = mapped_column(VARCHAR(length=255), unique=True)

    patients = relationship("PatientAlchemyModel", back_populates="clinic")
    admins = relationship("ClinicAdminAlchemyModel", back_populates="clinic")
