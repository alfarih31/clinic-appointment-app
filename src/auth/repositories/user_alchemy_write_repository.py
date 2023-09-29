from typing import Optional, Type

from dihub.decorators import provider, inject
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.auth.constants import USER_WRITE_REPOSITORY
from src.auth.models import UserAlchemyModel, UserAuthAlchemyModel
from src.auth.types import IUserWriteRepo
from src.sql_alchemy import EngineProvider


@provider(token=USER_WRITE_REPOSITORY)
class UserAlchemyWriteRepository(IUserWriteRepo):
    engine: EngineProvider = inject(EngineProvider)

    def insert(self, user: UserAlchemyModel):
        with Session(self.engine.engine) as session:
            session.add(user)

            session.commit()

    def find_by_username(self, username: str) -> Optional[Type[UserAuthAlchemyModel]]:
        with Session(self.engine.engine) as session:
            try:
                result = session.query(UserAuthAlchemyModel).where(UserAuthAlchemyModel.username == username).one()

                return result
            except NoResultFound:
                return None
