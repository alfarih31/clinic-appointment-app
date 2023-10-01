from dihub.decorators import provider, inject
from sqlalchemy import URL

from src.shared import Env


@provider
class SqlAlchemyConfig:
    env: Env = inject(Env)

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.env.get_str("DB_DRIVER", "postgresql+psycopg"),
            database=self.env.get_str("DB_DATABASE"),
            username=self.env.get_str("DB_USER"),
            password=self.env.get_str("DB_PASSWORD"),
            port=self.env.get_int("DB_PORT"),
            host=self.env.get_str("DB_HOST")
        )
