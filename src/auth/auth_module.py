from dihub.decorators import module

from .auth_controller import AuthController
from .auth_service import AuthService
from .commands import command_handlers
from .config.auth_config_module import AuthConfigModule
from .repositories import repositories


@module(providers=[AuthService, AuthController] + command_handlers + repositories, imports=[AuthConfigModule])
class AuthModule: ...
