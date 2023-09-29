from dihub.decorators import inject
from dihub_cqrs.decorators import command_handler
from dihub_cqrs.types import ICommandHandler

from src.auth.auth_exceptions import InvalidCredentialException
from src.auth.constants import AUTH_SERVICE, USER_WRITE_REPOSITORY
from src.auth.types import IAuthService, IUserWriteRepo
from .login_command import LoginCommand
from .login_result import LoginResult


@command_handler(LoginCommand)
class LoginHandler(ICommandHandler[LoginCommand, LoginResult]):
    auth_service: IAuthService = inject(AUTH_SERVICE)
    user_write_repo: IUserWriteRepo = inject(USER_WRITE_REPOSITORY)

    async def handle(self, command: LoginCommand) -> LoginResult:
        user_auth = self.user_write_repo.find_by_username(command.username)

        if user_auth is None:
            raise InvalidCredentialException()

        if not self.auth_service.password_hash_match(user_auth.credential, command.password):
            raise InvalidCredentialException()

        generated = self.auth_service.generate_token(user_auth.user_id)
        return LoginResult(access_token=generated["access_token"], expired_at=generated["expired_at"])
