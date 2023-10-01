from dataclasses import dataclass


@dataclass
class GetPatientAppointmentsQuery:
    patient_user_id: int
    clinic_id: int
