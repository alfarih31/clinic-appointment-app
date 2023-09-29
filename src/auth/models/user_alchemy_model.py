from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import VARCHAR

from src.shared.models import BaseAlchemyModel


class UserAlchemyModel(BaseAlchemyModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    user_auths = relationship("UserAuthAlchemyModel")
    user_roles = relationship("UserHasRoleAlchemyModel", back_populates="user")
