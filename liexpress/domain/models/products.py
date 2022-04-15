from dataclasses import dataclass
from datetime import date
from typing import List

from liexpress.domain.models.exceptions import (
    ActiveProductNotFound,
    OrderCriteriaNotSupported,
    ProductNotFound,
)


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


@dataclass
class Products:
    products: List[Product]

    def filter_active(self) -> List[Product]:
        active_products = list(filter(lambda x: x.active is True, self.products))

        if not active_products:
            raise ActiveProductNotFound("No active products found")

        return Products(active_products)

    def find(self, product_id: int) -> Product:
        product = next(
            (p for p in self.filter_active().products if p.product_id == product_id),
            None,
        )
        if not product:
            raise ProductNotFound(f"Product {product_id} not found")
        return product

    def get_highest_product_id(self):
        return max([p.product_id for p in self.products] or [0])


class ProductSorter:
    def __init__(
        self,
        products: List[Product],
    ):
        self._products = products
        self._supported_criteria = list(self._order_rules().keys())

    def _order_rules(self):
        return {
            "date": sorted(self._products, key=lambda x: x.date_added),
            "most_popular": sorted(
                self._products, key=lambda x: x.orders, reverse=True
            ),
        }

    def _check_order_criteria(self, order_by: str):
        if order_by not in self._supported_criteria:
            raise OrderCriteriaNotSupported(
                f"'{order_by}' order criteria is not supported. Only {self._supported_criteria}"
            )

    def __call__(self, order_by: str) -> List[Product]:
        self._check_order_criteria(order_by)
        return self._order_rules()[order_by]
