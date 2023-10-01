from datetime import datetime, timedelta, timezone
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator


def must_tomorrow(v: datetime) -> datetime:
    assert v.date() >= datetime.now(tz=timezone.utc).date() + timedelta(days=1), f'{v} is not tomorrow'
    return v


class CreateAppointmentBodyDto(BaseModel):
    clinic_id: int
    promised_date: Annotated[datetime, AfterValidator(must_tomorrow)]
    promised_duration: Annotated[int, Field(gt=600)]
