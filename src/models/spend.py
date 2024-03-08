from pydantic import BaseModel, StringConstraints, conlist
from pydantic import PositiveInt, field_validator
from typing import List
from typing_extensions import Annotated

class AddSpend(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    payer: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    shareholder: conlist(Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)], min_length=1) # type: ignore
    value: PositiveInt

    @field_validator('shareholder')
    def shareholder_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('shareholder list cannot be empty')
        return v

    @field_validator('payer')
    def payer_must_not_be_digits_only(cls, v):
        """Checking if the payer contains only digits"""
        if v.isdigit():
            raise ValueError('payer cannot contain only digits')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "apple",
                    "payer": "John",
                    "shareholder": ["John", "and", "his", "friend's", "names"],
                    "value": 1000,
                }
            ]
        }
    }

class DeleteSpend(BaseModel):
    id: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "The id string of deleted spend",
                }
            ]
        }
    }

class UpdateSpend(AddSpend, DeleteSpend):
    ...


class UpdateSpendList(BaseModel):
    """List of Spend object"""
    items: conlist(UpdateSpend, min_length=1) # type: ignore


class AddSpendList(BaseModel):
    """List of Spend object"""
    items: conlist(AddSpend, min_length=1) # type: ignore


class DeleteSpendList(BaseModel):
    """List of Deleted Spend object"""
    ids: List[str]

