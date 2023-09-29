from .fastapi_provider import FastAPIProvider
from dihub.decorators import module


@module(providers=[FastAPIProvider])
class FastAPIModule: ...
