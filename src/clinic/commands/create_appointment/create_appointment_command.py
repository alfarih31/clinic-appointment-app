from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateAppointmentCommand:
    patient_user_id: int
    clinic_id: int
    promised_date: datetime
    promised_duration: int
