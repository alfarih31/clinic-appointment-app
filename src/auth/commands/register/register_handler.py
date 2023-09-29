from dihub.decorators import inject
from dihub_cqrs.decorators import command_handler
from dihub_cqrs.types import ICommandHandler

from src.auth.constants import USER_WRITE_REPOSITORY, AUTH_SERVICE
from src.auth.models import UserAlchemyModel, UserAuthAlchemyModel, UserHasRoleAlchemyModel
from src.auth.types import IUserWriteRepo, IAuthService
from .register_command import RegisterCommand


@command_handler(RegisterCommand)
class RegisterHandler(ICommandHandler[RegisterCommand, None]):
    user_write_repo: IUserWriteRepo = inject(USER_WRITE_REPOSITORY)
    auth_service: IAuthService = inject(AUTH_SERVICE)

    async def handle(self, command: RegisterCommand) -> None:
        hashed_password = self.auth_service.generate_password_hash(command.password)

        user = UserAlchemyModel(full_name=command.full_name, user_auths=[UserAuthAlchemyModel(username=command.username, credential=hashed_password)],
                                user_roles=[UserHasRoleAlchemyModel(role_id=2)])

        self.user_write_repo.insert(user)
