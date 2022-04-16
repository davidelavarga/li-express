from datetime import date
from typing import List

from liexpress.adapters.data_provider.in_memory_criteria import (
    InMemoryCriteriaConverter,
)
from liexpress.domain.models.criteria import Criteria
from liexpress.domain.models.products import Configuration, Product
from liexpress.domain.ports import Repository


class InMemoryRepository(Repository):
    def __init__(self):
        self._products = self._in_memory_products()
        self._in_memory_reservations()

    def get_products(self, criteria: Criteria) -> List[Product]:
        """
        Get stored products.
        """
        query = InMemoryCriteriaConverter().convert(criteria)
        return query(self._products)

    def add_product(self, new: Product) -> int:
        """
        Add new product
        """
        self._products.append(new)
        return new.product_id

    def _in_memory_products(self) -> List[Product]:
        surf = Product(
            product_id=0,
            name="surf",
            description="Amazing surf classes.",
            price=20.0,
            date_added=date(2022, 4, 1),
            orders=2,
            configurations=[
                Configuration(name="date", type="date"),
                Configuration(name="time", type="time"),
                Configuration(name="additional notes", type="string"),
            ],
            active=True,
        )
        brunch = Product(
            product_id=1,
            name="brunch",
            description="Delicious homemade brunch.",
            price=12.0,
            date_added=date(2022, 4, 5),
            orders=5,
            configurations=[
                Configuration(name="consumption date", type="date"),
                Configuration(name="brunch type", type="string"),
            ],
            active=True,
        )
        museum = Product(
            product_id=2,
            name="natural science museum",
            description="Natural Science Museum",
            price=5.0,
            date_added=date(2022, 4, 10),
            orders=5,
            configurations=[
                Configuration(name="date", type="date"),
                Configuration(name="time", type="time"),
                Configuration(name="adults", type="int"),
                Configuration(name="children", type="int"),
            ],
            active=False,
        )
        return [surf, brunch, museum]

    def _in_memory_reservations(self):
        surf, brunch, museum = self._products
        surf.reservations.append(0)
        brunch.reservations.append(0)
        museum.reservations.append(0)

        brunch.reservations.append(1)
        museum.reservations.append(1)
