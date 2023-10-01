from dataclasses import dataclass


@dataclass
class GetClinicAppointmentsQuery:
    admin_user_id: int
    clinic_id: int
