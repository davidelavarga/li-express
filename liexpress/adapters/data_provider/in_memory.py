from datetime import date
from typing import List

from liexpress.domain.models.products import Configuration, Product
from liexpress.domain.ports import DataProvider


class InMemoryDataProvider(DataProvider):
    def __init__(self):
        self.products = self._in_memory_products()

    def get_products(self, active: bool = True) -> List[Product]:
        """
        Get products.
        If active=True return only active product,
        return all products otherwise.
        """
        if active:
            return list(filter(lambda x: x.active == active, self.products))

        return self.products

    def _in_memory_products(self) -> List[Product]:
        return [
            Product(
                product_id=0,
                name="surf",
                description="Amazing surf classes.",
                price=20.0,
                date_added=date(2022, 4, 1),
                orders=2,
                configuration=[
                    Configuration(name="date", type="date"),
                    Configuration(name="time", type="time"),
                    Configuration(name="additional notes", type="string"),
                ],
                active=True,
            ),
            Product(
                product_id=1,
                name="brunch",
                description="Delicious homemade brunch.",
                price=12.0,
                date_added=date(2022, 4, 5),
                orders=5,
                configuration=[
                    Configuration(name="consumption date", type="date"),
                    Configuration(name="brunch type", type="string"),
                ],
                active=True,
            ),
            Product(
                product_id=2,
                name="natural science museum",
                description="Natural Science Museum",
                price=5.0,
                date_added=date(2022, 4, 10),
                orders=5,
                configuration=[
                    Configuration(name="date", type="date"),
                    Configuration(name="time", type="time"),
                    Configuration(name="adults", type="int"),
                    Configuration(name="children", type="int"),
                ],
                active=False,
            ),
        ]
