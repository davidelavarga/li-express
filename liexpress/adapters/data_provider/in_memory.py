from datetime import date
from typing import Dict, List

from liexpress.domain.models.exceptions import ProductNotFound, ReservationIdNotFound
from liexpress.domain.models.products import Configuration, Product
from liexpress.domain.ports import DataProvider


class InMemoryDataProvider(DataProvider):
    def __init__(self):
        self._products = self._in_memory_products()

    def get_products(self, reservation_id: int, active: bool = True) -> List[Product]:
        """
        Get products for the given reservation_id.
        If active=True return only active product,
        return all products otherwise.
        """
        try:
            reservation_products = self._get_products_by_reservation_id(reservation_id)
        except KeyError:
            raise ReservationIdNotFound(f"Reservation {reservation_id} not found")

        if active:
            return list(filter(lambda x: x.active == active, reservation_products))

        return reservation_products

    def get_product(self, reservation_id: int, product_id: int) -> Product:
        """
        Get the product for the given reservation_id and product id
        """
        reservation_products = self._get_products_by_reservation_id(reservation_id)
        product = next(
            (p for p in reservation_products if p.product_id == product_id), None
        )
        if not product:
            raise ProductNotFound(
                f"Product {product_id} not found in reservation {reservation_id}"
            )
        return product

    def _get_products_by_reservation_id(self, reservation_id: int) -> List[Product]:
        try:
            return self._products[reservation_id]
        except KeyError:
            raise ReservationIdNotFound(f"Reservation {reservation_id} not found")

    def _in_memory_products(self) -> Dict[int, List[Product]]:
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
        return {0: [surf, brunch, museum], 1: [brunch, museum]}
