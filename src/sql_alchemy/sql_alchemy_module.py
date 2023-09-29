from dihub.decorators import module

from .engine_provider import EngineProvider
from .sql_alchemy_config import SqlAlchemyConfig


@module(providers=[SqlAlchemyConfig, EngineProvider])
class SqlAlchemyModule: ...
