from dataclasses import dataclass
from uuid import uuid4

from liexpress.domain.models.products import Product


@dataclass
class Order:
    reservation_id: int
    product: Product
    order_id: str = uuid4()

    def __eq__(self, o: object) -> bool:
        return (
            o.reservation_id == self.reservation_id
            and o.product.product_id == self.product.product_id
        )
