from datetime import date
from typing import List

from pydantic import BaseModel


class PlainProductResponse(BaseModel):
    product_id: int
    name: str
    description: str
    date_added: date
    price: float


class Configuration(BaseModel):
    name: str
    type: str


class DetailProductResponse(BaseModel):
    product_id: int
    name: str
    description: str
    date_added: date
    price: float
    order_fields: List[Configuration]


class NewProductRequest(BaseModel):
    name: str
    description: str
    price: float
    order_fields: List[Configuration]


class NewProductResponse(BaseModel):
    product_id: int
