from datetime import datetime, timezone
from typing import Annotated

from dihub.decorators import inject, provider
from dihub.types import IProviderRunner, IProviderProxy
from dihub_cqrs.constants import DISPATCHER, QUERY_BUS
from dihub_cqrs.types import IDispatcher, IQueryBus
from fastapi import APIRouter, Depends, Response, Query
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from src.fast_api import FastAPIProvider
from .commands import RegisterCommand, LoginCommand, LoginResult
from .constants import LOGGED_IN_COOKIE, ACCESS_TOKEN_VALIDATOR
from .dto import RegisterBodyDto
from .queries import GetUsersQuery
from .types import UserInfo


@provider
class AuthController(IProviderRunner):
    dispatcher: IDispatcher = inject(DISPATCHER)
    query_bus: IQueryBus = inject(QUERY_BUS)
    fastapi_provider: FastAPIProvider = inject(FastAPIProvider)
    access_token_validator: IProviderProxy = inject(ACCESS_TOKEN_VALIDATOR)

    def after_started(self):
        router = APIRouter(prefix="/auth")

        router.post("/register")(self.register)
        router.get("/login")(self.login)

        router.get("/users/list")(self.get_users(self.access_token_validator.release()))

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

    def get_users(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], full_name: Annotated[str, Query(min_length=3)], username: str | None = None):
            return await self.query_bus.query(GetUsersQuery(full_name=full_name, username=username))

        return handler
