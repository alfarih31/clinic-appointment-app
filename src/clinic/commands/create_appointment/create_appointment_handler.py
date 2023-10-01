from datetime import timedelta

from dihub.decorators import inject
from dihub_cqrs.decorators import command_handler

from src.clinic.clinic_exceptions import UserNotTheClinicPatients, PromisedAppointmentDateConflict
from src.clinic.constants import APPOINTMENT_WRITE_REPOSITORY, PATIENT_WRITE_REPOSITORY
from src.clinic.models import AppointmentAlchemyModel
from src.clinic.types import IAppointmentAlchemyWriteRepository, IPatientAlchemyWriteRepository
from .create_appointment_command import CreateAppointmentCommand
from .create_appointment_result import CreateAppointmentResult


@command_handler(CreateAppointmentCommand)
class CreateAppointmentHandler:
    appointment_write_repo: IAppointmentAlchemyWriteRepository = inject(APPOINTMENT_WRITE_REPOSITORY)
    patient_write_repo: IPatientAlchemyWriteRepository = inject(PATIENT_WRITE_REPOSITORY)

    async def handle(self, command: CreateAppointmentCommand) -> CreateAppointmentResult:
        patient = await self.patient_write_repo.find_by_user_and_clinic_id(command.patient_user_id, command.clinic_id)
        if patient is None:
            raise UserNotTheClinicPatients()

        estimated_end_date = command.promised_date + timedelta(seconds=command.promised_duration)
        has_conflict = await self.appointment_write_repo.count_conflict_appointment(command.promised_date, estimated_end_date)
        if has_conflict > 0:
            raise PromisedAppointmentDateConflict()

        queue = 1
        last_appointment = await self.appointment_write_repo.find_last_appointment_in_day(command.promised_date)
        if last_appointment is not None:
            queue = last_appointment.queue + 1

        await self.appointment_write_repo.insert(
            AppointmentAlchemyModel(
                queue=queue,
                patient_id=patient.id,
                promised_start_date=command.promised_date,
                promised_duration=command.promised_duration,
                estimated_end_date=estimated_end_date))

        return CreateAppointmentResult(queue=queue)
