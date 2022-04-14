from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Configuration:
    name: str
    type: str


@dataclass
class Product:
    product_id: int
    name: str
    description: str
    price: float
    date_added: date
    orders: int
    configuration: List[Configuration]
    active: bool = True
