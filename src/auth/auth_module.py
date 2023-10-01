from dihub.decorators import module

from .auth_controller import AuthController
from .auth_service import AuthService
from .commands import command_handlers
from .config.auth_config_module import AuthConfigModule
from .fastapi_dependencies import fastapi_dependencies
from .queries import query_handlers
from .repositories import repositories


@module(
    providers=[AuthService, AuthController] + command_handlers + repositories + fastapi_dependencies + query_handlers,
    imports=[AuthConfigModule])
class AuthModule: ...
