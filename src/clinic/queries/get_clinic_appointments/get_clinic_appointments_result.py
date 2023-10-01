from dataclasses import dataclass
from typing import List


@dataclass
class ClinicAppointmentsResultProps:
    id: int
    patient_id: int
    queue: int
    promised_start_date: str


@dataclass
class GetClinicAppointmentsResult:
    appointments: List[ClinicAppointmentsResultProps]
