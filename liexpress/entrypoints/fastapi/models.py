from datetime import date

from pydantic import BaseModel


class PlainProductResponse(BaseModel):
    product_id: int
    name: str
    description: str
    date_added: date
    price: float
