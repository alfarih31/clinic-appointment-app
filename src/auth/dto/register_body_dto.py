from pydantic import BaseModel, Field
from typing import Annotated


class RegisterBodyDto(BaseModel):
    full_name: Annotated[str, Field(max_length=255)]
    username: Annotated[str, Field(max_length=255)]
    password: str
