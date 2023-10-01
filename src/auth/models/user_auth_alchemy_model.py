from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import VARCHAR

from src.shared.models import BaseAlchemyModel
from .user_alchemy_model import UserAlchemyModel


class UserAuthAlchemyModel(BaseAlchemyModel):
    __tablename__ = "user_auth"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    credential: Mapped[str] = mapped_column(VARCHAR(255))

    user: Mapped[UserAlchemyModel] = relationship("UserAlchemyModel", back_populates="user_auths")
