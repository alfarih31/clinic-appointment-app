from dihub.decorators import inject
from dihub_cqrs.decorators import command_handler

from src.clinic.clinic_exceptions import UserNotTheClinicAdmins, UserAlreadyRegisteredAsPatient
from src.clinic.constants import CLINIC_WRITE_REPOSITORY, PATIENT_WRITE_REPOSITORY
from src.clinic.models import PatientAlchemyModel
from src.clinic.types import IClinicAlchemyWriteRepository, IPatientAlchemyWriteRepository
from .register_patient_command import RegisterPatientCommand


@command_handler(RegisterPatientCommand)
class RegisterPatientHandler:
    clinic_write_repo: IClinicAlchemyWriteRepository = inject(CLINIC_WRITE_REPOSITORY)
    patient_write_repo: IPatientAlchemyWriteRepository = inject(PATIENT_WRITE_REPOSITORY)

    async def handle(self, command: RegisterPatientCommand):
        count_admin = self.clinic_write_repo.count_clinic_admin(command.admin_user_id, command.clinic_id)
        if count_admin == 0:
            raise UserNotTheClinicAdmins()

        count_patient = self.patient_write_repo.count_patient(command.user_id, command.clinic_id)
        if count_patient > 0:
            raise UserAlreadyRegisteredAsPatient()

        self.patient_write_repo.insert(PatientAlchemyModel(user_id=command.user_id, clinic_id=command.clinic_id))
