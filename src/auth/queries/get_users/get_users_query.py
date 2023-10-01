from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GetUsersQuery:
    full_name: str
    username: Optional[str] = None
