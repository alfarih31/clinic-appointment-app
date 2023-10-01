from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GetPatientsQuery:
    admin_user_id: int
    clinic_id: int
    user_full_name: Optional[str] = None
