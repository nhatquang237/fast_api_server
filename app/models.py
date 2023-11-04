from pydantic import BaseModel, validator
from typing import List, Optional

class Spend(BaseModel):
    id: Optional[str] = None
    name: str
    value: float
    payer: str
    shareholder: List[str]

    # Custom validator for the 'shareholder'
    @validator('shareholder')
    def validate_shareholder(cls, shareholder):
        if not shareholder:
            raise ValueError("shareholder can not be an empty list")
        return shareholder

class SpendList(BaseModel):
    items: List[Spend]
