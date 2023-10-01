from dataclasses import dataclass


@dataclass(frozen=True)
class CreateClinicCommand:
    user_id: int
    name: str
