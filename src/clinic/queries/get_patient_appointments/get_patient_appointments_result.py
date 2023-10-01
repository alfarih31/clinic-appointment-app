from dataclasses import dataclass
from typing import List


@dataclass
class PatientAppointmentsResultProps:
    id: int
    patient_id: int
    queue: int
    promised_start_date: str


@dataclass
class GetPatientAppointmentsResult:
    appointments: List[PatientAppointmentsResultProps]
