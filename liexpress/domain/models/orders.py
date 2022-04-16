from dataclasses import dataclass
from uuid import uuid4

from liexpress.domain.models.products import Product


@dataclass
class Order:
    reservation_id: int
    product: Product
    order_id: str = uuid4()
