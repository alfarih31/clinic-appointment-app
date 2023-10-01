from dihub.decorators import provider, inject, export

from src.shared.providers import Env


@export
@provider
class AuthConfig:
    __env: Env = inject(Env)

    @property
    def bcrypt_salt_rounds(self) -> int:
        return self.__env.get_int("BCRYPT_SALT_ROUNDS")

    @property
    def jwt_rsa_file(self) -> str:
        return self.__env.get_str("JWT_RSA_FILE")

    @property
    def jwt_rsa_alg(self) -> str:
        return self.__env.get_str("JWT_RSA_ALG", "RS256")

    @property
    def jwt_audience(self) -> str:
        return self.__env.get_str("JWT_AUDIENCE")

    @property
    def jwt_issuer(self) -> str:
        return self.__env.get_str("JWT_ISSUER")

    @property
    def jwt_expires(self) -> int:
        return self.__env.get_int("JWT_EXPIRES", 43200)
