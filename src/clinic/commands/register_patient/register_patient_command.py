from dataclasses import dataclass


@dataclass
class RegisterPatientCommand:
    admin_user_id: int
    user_id: int
    clinic_id: int
