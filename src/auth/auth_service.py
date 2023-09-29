from datetime import datetime, timezone

import bcrypt
import jwt
from dihub.decorators import inject, provider
from dihub.types import IProviderRunner
from jwt.utils import get_int_from_datetime

from src.shared import BcryptHash
from .config import AuthConfig
from .constants import AUTH_SERVICE
from .types import IAuthService, GenerateTokenResult


@provider(token=AUTH_SERVICE)
class AuthService(IAuthService, IProviderRunner):
    jwt_instance = jwt.JWT()
    auth_config: AuthConfig = inject(AuthConfig)
    jwt_signing_key = None

    def after_started(self):
        with open(self.auth_config.jwt_rsa_file, "rb") as fs:
            self.jwt_signing_key = jwt.jwk_from_pem(fs.read())

    def generate_password_hash(self, password: str) -> str:
        return BcryptHash.generate_hash(password, self.auth_config.bcrypt_salt_rounds)

    def password_hash_match(self, hashed_password: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def generate_token(self, user_id: int) -> GenerateTokenResult:
        now = get_int_from_datetime(datetime.now(timezone.utc))
        expired_at = now + self.auth_config.jwt_expires

        token = self.jwt_instance.encode({
            "sub": user_id,
            "aud": self.auth_config.jwt_audience,
            "iat": now,
            "exp": expired_at
        }, self.jwt_signing_key, alg=self.auth_config.jwt_rsa_alg)

        return {
            "access_token": token,
            'expired_at': expired_at
        }
