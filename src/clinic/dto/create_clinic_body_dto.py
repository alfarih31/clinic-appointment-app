from typing import Annotated

from pydantic import BaseModel, Field


class CreateClinicBodyDto(BaseModel):
    name: Annotated[str, Field(max_length=255)]
