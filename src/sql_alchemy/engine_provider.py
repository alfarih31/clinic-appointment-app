from dihub.decorators import inject, provider, export
from dihub.types import IProviderRunner
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .sql_alchemy_config import SqlAlchemyConfig


@export
@provider
class EngineProvider(IProviderRunner):
    config: SqlAlchemyConfig = inject(SqlAlchemyConfig)
    __engine: Engine
    __async_engine: AsyncEngine

    def after_started(self):
        self.__engine = create_engine(url=self.config.url)
        self.__async_engine = create_async_engine(url=self.config.url)

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def async_engine(self) -> AsyncEngine:
        return self.__async_engine
