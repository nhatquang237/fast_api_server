from pydantic import BaseModel
from typing import List, Optional

class Spend(BaseModel):
    id: Optional[str] = None
    name: str
    value: float
    payer: str
    shareholder: List[str]

class SpendList(BaseModel):
    items: List[Spend]
