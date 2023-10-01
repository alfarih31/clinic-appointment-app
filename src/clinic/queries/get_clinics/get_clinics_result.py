from dataclasses import dataclass
from typing import List


@dataclass
class ClinicResultProps:
    id: int
    name: str


@dataclass
class GetClinicsResult:
    clinics: List[ClinicResultProps]
