from fastapi import Request, FastAPI
from sqlalchemy.exc import DatabaseError

from .response_envelope import ResponseEnvelope


def sql_alchemy_integrity_error_handler(fastapi: FastAPI):
    async def handler(request: Request, exc: DatabaseError):
        return ResponseEnvelope(status_code=400, content=exc.orig)

    fastapi.exception_handler(DatabaseError)(handler)
