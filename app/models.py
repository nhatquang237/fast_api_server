from pydantic import BaseModel
from typing import List

class UpdateSpend(BaseModel):
    id: str
    name: str
    value: float
    payer: str
    shareholder: List[str]
    # Add other properties as needed

class UpdateSpendList(BaseModel):
    items: List[UpdateSpend]


class CreateSpend(BaseModel):
    name: str
    value: float
    payer: str
    shareholder: List[str]
    # Add other properties as needed

class CreateSpendList(BaseModel):
    items: List[CreateSpend]

