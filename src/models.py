from pydantic import BaseModel, validator
from typing import List



class AddSpend(BaseModel):
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

class DeleteSpend(BaseModel):
    id: str

class UpdateSpend(AddSpend, DeleteSpend):
    ...

class UpdateSpendList(BaseModel):
    """List of Spend object"""
    items: List[UpdateSpend]

class AddSpendList(BaseModel):
    """List of Spend object"""
    items: List[AddSpend]

class DeleteSpendList(BaseModel):
    """List of Deleted Spend object"""
    ids: List[str]
