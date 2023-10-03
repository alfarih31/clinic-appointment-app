from typing import Optional, Type, List, Annotated

from dihub.decorators import provider, inject
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.auth.constants import USER_WRITE_REPOSITORY
from src.auth.models import UserAlchemyModel, UserAuthAlchemyModel
from src.auth.types import IUserWriteRepo
from src.sql_alchemy import EngineProvider

FindAllParams = IUserWriteRepo.FindAllParams


@provider(token=USER_WRITE_REPOSITORY)
class UserAlchemyWriteRepository(IUserWriteRepo):
    engine: Annotated[EngineProvider, inject(EngineProvider)]

    def insert(self, user: UserAlchemyModel):
        with Session(self.engine.engine) as session:
            session.add(user)

            session.commit()

    def find_all_auths(self, params: FindAllParams) -> List[UserAuthAlchemyModel]:
        with Session(self.engine.engine) as session:
            where_params = []
            if params.full_name is not None:
                where_params.append(UserAlchemyModel.full_name.ilike("%{}%".format(params.full_name)))
            if params.username is not None:
                where_params.append(UserAuthAlchemyModel.username.ilike("%{}%".format(params.username)))

            stmt = select(UserAuthAlchemyModel).join(UserAuthAlchemyModel.user).where(*where_params)
            results = session.scalars(stmt).all()

            return [r.detach_relationship() for r in results]

    def find_auth_by_username(self, username: str) -> Optional[Type[UserAuthAlchemyModel]]:
        with Session(self.engine.engine) as session:
            try:
                stmt = select(UserAuthAlchemyModel).where(UserAuthAlchemyModel.username == username).join(UserAuthAlchemyModel.user)
                result = session.scalar(stmt)

                return result
            except NoResultFound:
                return None

    def find_auth_by_user_id(self, user_id: int) -> Optional[UserAuthAlchemyModel]:
        with Session(self.engine.engine) as session:
            try:
                stmt = select(UserAuthAlchemyModel).where(UserAuthAlchemyModel.user_id == user_id).join(UserAuthAlchemyModel.user)
                result = session.scalar(stmt)
                if result is not None:
                    result.detach_relationship()

                return result
            except NoResultFound:
                return None
