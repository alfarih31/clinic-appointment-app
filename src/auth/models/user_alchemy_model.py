from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import VARCHAR

from src.shared.models import BaseAlchemyModel


class UserAlchemyModel(BaseAlchemyModel):
    __tablename__ = "user"

    full_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    user_auths = relationship("UserAuthAlchemyModel")
    user_roles = relationship("UserHasRoleAlchemyModel", back_populates="user")

    clinic_patients = relationship("PatientAlchemyModel", back_populates="user")
