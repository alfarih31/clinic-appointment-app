from dihub.decorators import export, provider
from dihub.types import IProviderRunner
from fastapi import FastAPI

from .exception_handlers import sql_alchemy_integrity_error_handler
from .response_envelope import ResponseEnvelope


@export
@provider
class FastAPIProvider(FastAPI, IProviderRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(default_response_class=ResponseEnvelope, *args, **kwargs)

    def after_started(self):
        sql_alchemy_integrity_error_handler(self)
