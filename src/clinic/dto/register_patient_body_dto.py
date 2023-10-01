from pydantic import BaseModel


class RegisterPatientBodyDto(BaseModel):
    user_id: int
    clinic_id: int
