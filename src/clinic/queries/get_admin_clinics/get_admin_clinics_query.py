from dataclasses import dataclass
from typing import Optional


@dataclass
class GetAdminClinicsQuery:
    user_id: int
    name: Optional[str] = None
