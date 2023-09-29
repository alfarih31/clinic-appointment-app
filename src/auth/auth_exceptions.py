from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from src.shared import DomainException

_DOMAIN = "auth"


class AuthException(DomainException):
    message: str = ""

    def __init__(self, code: str, message: str = ""):
        super().__init__(_DOMAIN, code)
        if message == "":
            self.message = code


class InvalidCredentialException(AuthException, HTTPException):
    def __init__(self):
        super(InvalidCredentialException, self).__init__("Invalid credentials")
        super(HTTPException, self).__init__(status_code=HTTP_401_UNAUTHORIZED, detail=super(InvalidCredentialException, self).__str__())
