from dataclasses import dataclass


@dataclass(frozen=True)
class LoginResult:
    access_token: str
    expired_at: int
