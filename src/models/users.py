from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated

from regex_pattern import password_pattern


class Username(BaseModel):
    username: str

class NewUser(BaseModel):
    username: str
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=8, pattern=password_pattern)]

