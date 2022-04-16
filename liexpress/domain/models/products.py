from dataclasses import dataclass, field
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
    configurations: List[Configuration]
    active: bool = True
    reservations: List[int] = field(default_factory=list)
