from datetime import datetime, timezone
from typing import Annotated

from dihub.decorators import inject
from dihub.decorators import provider
from dihub.types import IProviderRunner
from dihub_cqrs.constants import DISPATCHER
from dihub_cqrs.types import IDispatcher
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from src.fast_api import FastAPIProvider
from .commands import RegisterCommand, LoginCommand, LoginResult
from .constants import LOGGED_IN_COOKIE
from .dto import RegisterBodyDto


@provider
class AuthController(IProviderRunner):
    dispatcher: IDispatcher = inject(DISPATCHER)
    fastapi_provider: FastAPIProvider = inject(FastAPIProvider)

    def after_started(self):
        router = APIRouter(prefix="/auth")

        router.post("/register")(self.register)
        router.get("/login")(self.login)

        self.fastapi_provider.include_router(router)

    async def register(self, body: RegisterBodyDto):
        await self.dispatcher.dispatch(RegisterCommand(
            username=body.username,
            password=body.password,
            full_name=body.full_name))

    async def login(self, credential: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())], response: Response):
        result = await self.dispatcher.create_static_dispatcher(LoginCommand, LoginResult).dispatch(
            LoginCommand(username=credential.username, password=credential.password))
        response.set_cookie(LOGGED_IN_COOKIE, result.access_token, expires=datetime.fromtimestamp(result.expired_at, timezone.utc), samesite="strict")
