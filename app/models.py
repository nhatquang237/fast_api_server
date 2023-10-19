from pydantic import BaseModel
from typing import List

class Spend(BaseModel):
    id: str
    name: str
    value: float
    payer: str
    shareholder: List[str]
    # Add other properties as needed

class SpendList(BaseModel):
    items: List[Spend]

