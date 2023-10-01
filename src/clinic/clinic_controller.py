from typing import Annotated

from dihub.decorators import provider, inject
from dihub.types import IProviderRunner, IProviderProxy
from dihub_cqrs.constants import DISPATCHER, QUERY_BUS
from dihub_cqrs.types import IDispatcher, IQueryBus
from fastapi import APIRouter, Body, Query

from src.auth.constants import ACCESS_TOKEN_VALIDATOR
from src.auth.types import UserInfo
from src.fast_api import FastAPIProvider
from .commands import CreateClinicCommand, RegisterPatientCommand, CreateAppointmentCommand
from .dto import CreateClinicBodyDto, RegisterPatientBodyDto, CreateAppointmentBodyDto
from .queries import (GetAdminClinicsQuery, GetClinicsQuery, GetPatientsQuery, GetClinicAppointmentsQuery, GetPatientAppointmentsQuery)


@provider
class ClinicController(IProviderRunner):
    dispatcher: IDispatcher = inject(DISPATCHER)
    query_bus: IQueryBus = inject(QUERY_BUS)
    fastapi_provider: FastAPIProvider = inject(FastAPIProvider)
    access_token_validator: IProviderProxy = inject(ACCESS_TOKEN_VALIDATOR)

    def after_started(self):
        router = APIRouter(prefix="/clinics")

        router.get("/appointments/list")(self.get_clinic_appointments(self.access_token_validator.release()))

        router.post("/create")(self.create_clinic(self.access_token_validator.release()))
        router.get("/list/owned")(self.get_admin_clinics(self.access_token_validator.release()))
        router.get("/list")(self.get_clinics)

        router.post("/patients/register")(self.register_patient_handler(self.access_token_validator.release()))
        router.get("/patients/list")(self.get_clinic_patients(self.access_token_validator.release()))

        router.post("/patients/appointments/create")(self.create_appointment(self.access_token_validator.release()))
        router.get("/patients/appointments/list")(self.get_patient_appointments(self.access_token_validator.release()))
        self.fastapi_provider.include_router(router)

    def create_clinic(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], body: Annotated[CreateClinicBodyDto, Body()]):
            await self.dispatcher.dispatch(CreateClinicCommand(user_id=user.user_id, name=body.name))

        return handler

    async def get_clinics(self, name: Annotated[str, Query(min_length=3)]):
        return await self.query_bus.query(GetClinicsQuery(name=name))

    def get_admin_clinics(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], name: str | None = None):
            return await self.query_bus.query(GetAdminClinicsQuery(user_id=user.user_id, name=name))

        return handler

    def register_patient_handler(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], body: Annotated[RegisterPatientBodyDto, Body()]):
            await self.dispatcher.dispatch(RegisterPatientCommand(admin_user_id=user.user_id, user_id=body.user_id, clinic_id=body.clinic_id))

        return handler

    def get_clinic_patients(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], clinic_id: Annotated[int, Query()],
                          full_name: Annotated[str, Query(min_length=3)]):
            return await self.query_bus.query(GetPatientsQuery(admin_user_id=user.user_id, user_full_name=full_name, clinic_id=clinic_id))

        return handler

    def create_appointment(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], body: Annotated[CreateAppointmentBodyDto, Body()]):
            return await self.dispatcher.dispatch(
                CreateAppointmentCommand(patient_user_id=user.user_id, clinic_id=body.clinic_id, promised_date=body.promised_date,
                                         promised_duration=body.promised_duration))

        return handler

    def get_clinic_appointments(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], clinic_id: Annotated[int, Query()]):
            return await self.query_bus.query(GetClinicAppointmentsQuery(admin_user_id=user.user_id, clinic_id=clinic_id))

        return handler

    def get_patient_appointments(self, token_validator):
        async def handler(user: Annotated[UserInfo, token_validator], clinic_id: Annotated[int, Query()]):
            return await self.query_bus.query(GetPatientAppointmentsQuery(patient_user_id=user.user_id, clinic_id=clinic_id))

        return handler
