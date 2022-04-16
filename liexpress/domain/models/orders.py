from dataclasses import dataclass

from liexpress.domain.models.products import Product


@dataclass
class Order:
    order_id: str
    reservation_id: int
    product: Product

    def __eq__(self, o: object) -> bool:
        return (
            o.reservation_id == self.reservation_id
            and o.product.product_id == self.product.product_id
        )
