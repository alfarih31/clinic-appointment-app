from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .models import ClinicAlchemyModel, PatientAlchemyModel, AppointmentAlchemyModel


@dataclass
class FindAllParams:
    user_id: Optional[int] = None
    name: Optional[str] = None


class IClinicAlchemyWriteRepository(ABC):
    @abstractmethod
    def insert(self, clinic: ClinicAlchemyModel): ...

    @abstractmethod
    def find_all(self, params: FindAllParams) -> List[ClinicAlchemyModel]: ...

    @abstractmethod
    def count_clinic_admin(self, user_id: int, clinic_id: int) -> int: ...


class IPatientAlchemyWriteRepository(ABC):
    @dataclass
    class FindAllParams:
        clinic_id: Optional[int] = None
        user_full_name: Optional[str] = None

    @abstractmethod
    def insert(self, patient: PatientAlchemyModel): ...

    @abstractmethod
    def count_patient(self, user_id: int, clinic_id) -> int: ...

    @abstractmethod
    def find_all(self, params: FindAllParams) -> List[PatientAlchemyModel]: ...

    @abstractmethod
    async def find_by_user_and_clinic_id(self, user_id: int, clinic_id: int) -> Optional[PatientAlchemyModel]: ...


class IAppointmentAlchemyWriteRepository(ABC):
    @dataclass
    class FindAllParams:
        patient_id: Optional[int] = None
        clinic_id: Optional[int] = None

    @abstractmethod
    async def insert(self, appointment: AppointmentAlchemyModel): ...

    @abstractmethod
    async def find_last_appointment_in_day(self, date: datetime) -> Optional[AppointmentAlchemyModel]: ...

    @abstractmethod
    async def count_conflict_appointment(self, promised_start_date: datetime, estimated_end_date: datetime) -> int: ...

    @abstractmethod
    async def update(self, appointment: AppointmentAlchemyModel): ...

    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[AppointmentAlchemyModel]: ...

    @abstractmethod
    async def find_all(self, params: FindAllParams) -> List[AppointmentAlchemyModel]: ...
