from datetime import date
from typing import Dict, List

from liexpress.domain.models.exceptions import ReservationIdNotFound
from liexpress.domain.models.products import Configuration, Product, Products
from liexpress.domain.ports import DataProvider


class InMemoryDataProvider(DataProvider):
    def __init__(self):
        self._products = self._in_memory_products()
        self._reservations = self._in_memory_reservations()

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
            return reservation_products.filter_active()

        return reservation_products.products

    def get_product(self, product_id: int) -> Product:
        """
        Get the product for the given product id
        """
        return Products(products=self._products).find(product_id)

    def _get_products_by_reservation_id(self, reservation_id: int) -> List[Product]:
        try:
            return Products(
                products=self._reservations[reservation_id],
            )
        except KeyError:
            raise ReservationIdNotFound(f"Reservation {reservation_id} not found")

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

    def _in_memory_reservations(self) -> Dict[int, List[Product]]:
        surf, brunch, museum = self._products
        return {0: [surf, brunch, museum], 1: [brunch, museum]}
