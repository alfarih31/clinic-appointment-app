from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.shared import DomainException

_DOMAIN = "clinic"


class ClinicException(DomainException, HTTPException):
    message: str = ""

    def __init__(self, code: str, message: str = ""):
        super().__init__(_DOMAIN, code)
        super(HTTPException, self).__init__(status_code=HTTP_400_BAD_REQUEST, detail=str(self))

        if message == "":
            self.message = code


class UserNotTheClinicAdmins(ClinicException):
    def __init__(self):
        super().__init__("User not the clinic admins")


class UserAlreadyRegisteredAsPatient(ClinicException):
    def __init__(self):
        super().__init__("User already registered as patient")


class UserNotTheClinicPatients(ClinicException):
    def __init__(self):
        super().__init__("User not the clinic patients")


class PromisedAppointmentDateConflict(ClinicException):
    def __init__(self):
        super().__init__("Promised appointment date conflict")


class AppointmentNotFound(ClinicException):
    def __init__(self):
        super().__init__("Appointment not found")


class AppointmentStatusNotQueue(ClinicException):
    def __init__(self):
        super().__init__("Appointment status not queue")
