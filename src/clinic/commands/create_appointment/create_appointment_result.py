from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAppointmentResult:
    queue: int
