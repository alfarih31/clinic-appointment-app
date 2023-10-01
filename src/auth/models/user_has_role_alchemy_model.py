from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP

from src.shared import BaseAlchemyModel


class Base(DeclarativeBase): ...


class UserHasRoleAlchemyModel(BaseAlchemyModel):
    __tablename__ = "user_has_role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = None

    user = relationship("UserAlchemyModel", back_populates="user_roles")
    role = relationship("RoleAlchemyModel", back_populates="users")
