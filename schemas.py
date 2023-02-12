from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: int
    name: str
    email: str

class Account(BaseModel):
    customer_id: int
    account_number: str
    

class AccountExtend(Account):
    balance: float


class Card(BaseModel):
    account_id: int
    card_number: str
    card_type: str
