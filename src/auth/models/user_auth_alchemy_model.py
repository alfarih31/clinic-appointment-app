from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import VARCHAR

from src.shared.models import BaseAlchemyModel


class UserAuthAlchemyModel(BaseAlchemyModel):
    __tablename__ = "user_auth"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    credential: Mapped[str] = mapped_column(VARCHAR(255))

    user = relationship("UserAlchemyModel", back_populates="user_auths")
