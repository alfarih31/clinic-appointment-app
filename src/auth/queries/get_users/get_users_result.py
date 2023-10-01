from dataclasses import dataclass
from typing import List


@dataclass
class UserResultProps:
    id: int
    username: str
    full_name: str


@dataclass
class GetUsersResult:
    users: List[UserResultProps]
