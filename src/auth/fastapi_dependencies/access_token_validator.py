from dihub.decorators import provider, export, inject
from fastapi import Request
from fastapi.params import Depends

from src.auth.auth_exceptions import NotLoggedInException, InvalidCredentialException
from src.auth.constants import ACCESS_TOKEN_VALIDATOR, USER_WRITE_REPOSITORY, LOGGED_IN_COOKIE, AUTH_SERVICE
from src.auth.types import IUserWriteRepo, IAuthService, UserInfo


@export
@provider(token=ACCESS_TOKEN_VALIDATOR)
class AccessTokenValidator(Depends):
    user_write_repo: IUserWriteRepo = inject(USER_WRITE_REPOSITORY)
    auth_svc: IAuthService = inject(AUTH_SERVICE)

    def __init__(self):
        super().__init__(self)

    async def __call__(self, request: Request) -> UserInfo:
        logged_in_cookie = request.cookies.get(LOGGED_IN_COOKIE)
        if logged_in_cookie is None:
            raise NotLoggedInException()

        validate_result = self.auth_svc.validate_token(logged_in_cookie)

        user_auth = self.user_write_repo.find_auth_by_user_id(validate_result["user_id"])
        if user_auth is None:
            raise InvalidCredentialException()

        return UserInfo(full_name=user_auth.user.full_name, user_id=user_auth.user_id, username=user_auth.username)
