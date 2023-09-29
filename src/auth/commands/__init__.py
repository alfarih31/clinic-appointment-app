from .login.login_command import LoginCommand
from .login.login_handler import LoginHandler
from .login.login_result import LoginResult
from .register.register_command import RegisterCommand
from .register.register_handler import RegisterHandler

command_handlers = [RegisterHandler, LoginHandler]
