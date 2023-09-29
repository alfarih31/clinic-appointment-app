from dihub.decorators import inject, provider, export
from dihub.types import IProviderRunner
from sqlalchemy import Engine, create_engine

from .sql_alchemy_config import SqlAlchemyConfig


@export
@provider
class EngineProvider(IProviderRunner):
    config: SqlAlchemyConfig = inject(SqlAlchemyConfig)
    engine: Engine

    def after_started(self):
        self.engine = create_engine(url=self.config.dsn_url)
