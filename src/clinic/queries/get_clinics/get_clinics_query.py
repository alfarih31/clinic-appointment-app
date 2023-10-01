from dataclasses import dataclass
from typing import Optional


@dataclass
class GetClinicsQuery:
    user_id: Optional[int] = None
    name: Optional[str] = None
