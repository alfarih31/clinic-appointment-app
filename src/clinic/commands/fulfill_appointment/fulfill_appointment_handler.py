from dihub.decorators import inject
from dihub_cqrs.decorators import command_handler

from src.clinic.clinic_exceptions import AppointmentNotFound, AppointmentStatusNotQueue
from src.clinic.constants import APPOINTMENT_WRITE_REPOSITORY, PATIENT_WRITE_REPOSITORY
from src.clinic.models import AppointmentStatus
from src.clinic.types import IAppointmentAlchemyWriteRepository, IPatientAlchemyWriteRepository
from .fulfill_appointment_command import FulfillAppointmentCommand


@command_handler(FulfillAppointmentCommand)
class FulfillAppointmentHandler:
    appointment_write_repo: IAppointmentAlchemyWriteRepository = inject(APPOINTMENT_WRITE_REPOSITORY)
    patient_write_repo: IPatientAlchemyWriteRepository = inject(PATIENT_WRITE_REPOSITORY)

    async def handle(self, command: FulfillAppointmentCommand):
        appointment = await self.appointment_write_repo.find_by_id(command.appointment_id)
        if appointment is None:
            raise AppointmentNotFound()

        if appointment.status_id != AppointmentStatus.QUEUED:
            raise AppointmentStatusNotQueue()

        appointment.status_id = AppointmentStatus.FULFILLED

        await self.appointment_write_repo.update(appointment)
