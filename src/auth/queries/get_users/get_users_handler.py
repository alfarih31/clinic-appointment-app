from dihub.decorators import inject
from dihub_cqrs.decorators import query_handler

from src.auth.constants import USER_WRITE_REPOSITORY
from src.auth.types import IUserWriteRepo
from .get_users_query import GetUsersQuery
from .get_users_result import GetUsersResult, UserResultProps


@query_handler(GetUsersQuery, GetUsersResult)
class GetUsersHandler:
    user_write_repo: IUserWriteRepo = inject(USER_WRITE_REPOSITORY)

    async def handle(self, query: GetUsersQuery) -> GetUsersResult:
        rows = self.user_write_repo.find_all_auths(IUserWriteRepo.FindAllParams(full_name=query.full_name, username=query.username))

        return GetUsersResult(users=[UserResultProps(id=r.user_id, username=r.username, full_name=r.user.full_name) for r in rows])
