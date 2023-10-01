from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared import BaseAlchemyModel


class ClinicAdminAlchemyModel(BaseAlchemyModel):
    __tablename__ = "clinic_admin"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    clinic_id: Mapped[int] = mapped_column(ForeignKey("clinic.id"))

    clinic = relationship("ClinicAlchemyModel", back_populates="admins")
