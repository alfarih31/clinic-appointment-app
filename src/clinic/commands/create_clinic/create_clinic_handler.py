from dihub.decorators import inject
from dihub_cqrs.decorators import command_handler
from slugify import slugify

from src.clinic.constants import CLINIC_WRITE_REPOSITORY
from src.clinic.models import ClinicAlchemyModel, ClinicAdminAlchemyModel
from src.clinic.types import IClinicAlchemyWriteRepository
from .create_clinic_command import CreateClinicCommand


@command_handler(CreateClinicCommand)
class CreateClinicHandler:
    clinic_write_repo: IClinicAlchemyWriteRepository = inject(CLINIC_WRITE_REPOSITORY)

    async def handle(self, command: CreateClinicCommand):
        self.clinic_write_repo.insert(ClinicAlchemyModel(
            name=command.name,
            slug=slugify(command.name, max_length=255),
            admins=[
                ClinicAdminAlchemyModel(user_id=command.user_id)
            ]))
