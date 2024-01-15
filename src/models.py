from pydantic import BaseModel, validator
from typing import List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Username(BaseModel):
    username: str

class Email(BaseModel):
    email: str


class NewUser(BaseModel):
    username: str
    password: str


class AddSpend(BaseModel):
    name: str
    value: float
    payer: str
    shareholder: List[str]

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
