from abc import ABC, abstractmethod
from typing import Optional, TypedDict

from .models import UserAlchemyModel, UserAuthAlchemyModel


class IUserWriteRepo(ABC):
    @abstractmethod
    def insert(self, user: UserAlchemyModel): ...

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[UserAuthAlchemyModel]: ...


class GenerateTokenResult(TypedDict):
    access_token: str
    expired_at: int


class IAuthService(ABC):
    @abstractmethod
    def generate_password_hash(self, password: str) -> str: ...

    @abstractmethod
    def password_hash_match(self, hashed_password: str, password: str) -> bool: ...

    @abstractmethod
    def generate_token(self, user_id: int) -> GenerateTokenResult: ...
