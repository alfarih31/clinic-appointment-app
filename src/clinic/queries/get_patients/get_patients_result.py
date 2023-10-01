from dataclasses import dataclass
from typing import List


@dataclass
class PatientResultProps:
    id: int

    user_id: int
    user_full_name: str


@dataclass
class GetPatientsResult:
    patients: List[PatientResultProps]
