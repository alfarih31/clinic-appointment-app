from datetime import datetime
from inspect import getmembers

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, BIGINT


class BaseAlchemyModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    def detach_relationship(self):
        for attr_name, _ in getmembers(self, predicate=lambda x: isinstance(x, BaseAlchemyModel)):
            if attr_name is not None:
                hasattr(self, attr_name)

        return self
