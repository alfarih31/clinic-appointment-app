from dihub.decorators import module

from .auth_config import AuthConfig


@module(providers=[AuthConfig])
class AuthConfigModule: ...
