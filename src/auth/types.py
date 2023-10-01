from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, TypedDict, List

from .models import UserAlchemyModel, UserAuthAlchemyModel


class IUserWriteRepo(ABC):
    @dataclass
    class FindAllParams:
        full_name: Optional[str] = None
        username: Optional[str] = None

    @abstractmethod
    def find_all_auths(self, params: FindAllParams) -> List[UserAuthAlchemyModel]: ...

    @abstractmethod
    def insert(self, user: UserAlchemyModel): ...

    @abstractmethod
    def find_auth_by_username(self, username: str) -> Optional[UserAuthAlchemyModel]: ...

    @abstractmethod
    def find_auth_by_user_id(self, id: int) -> Optional[UserAuthAlchemyModel]: ...


class GenerateTokenResult(TypedDict):
    access_token: str
    expired_at: int


class ValidateTokenResult(TypedDict):
    user_id: int


class IAuthService(ABC):
    @abstractmethod
    def generate_password_hash(self, password: str) -> str: ...

    @abstractmethod
    def password_hash_match(self, hashed_password: str, password: str) -> bool: ...

    @abstractmethod
    def generate_token(self, user_id: int) -> GenerateTokenResult: ...

    @abstractmethod
    def validate_token(self, token: str) -> ValidateTokenResult: ...


@dataclass(frozen=True)
class UserInfo:
    user_id: int
    username: str
    full_name: str
