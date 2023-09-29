from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import VARCHAR, SMALLINT

from src.shared import BaseAlchemyModel


class RoleAlchemyModel(BaseAlchemyModel):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    users = relationship("UserHasRoleAlchemyModel", back_populates="role")
