from dataclasses import dataclass


@dataclass
class FulfillAppointmentCommand:
    appointment_id: int
