from datetime import date
from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    region: str = Field(min_length=1, max_length=80)
    segment: str = Field(min_length=1, max_length=80)


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)


class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    order_date: date
    quantity: int = Field(gt=0)
    amount: float = Field(gt=0)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AskResponse(BaseModel):
    answer: str
    data: dict
