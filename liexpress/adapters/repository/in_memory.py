from datetime import date
from typing import List

from liexpress.adapters.repository.in_memory_criteria import InMemoryCriteriaConverter
from liexpress.domain.models.criteria import Criteria
from liexpress.domain.models.exceptions import ProductAlreadyRequested
from liexpress.domain.models.orders import Order
from liexpress.domain.models.products import Configuration, Product
from liexpress.domain.ports import Repository


class InMemoryRepository(Repository):
    def __init__(self):
        self._products = self._in_memory_products()
        self._reservations = self._in_memory_reservations()
        self._orders = []

    def get_products(self, criteria: Criteria) -> List[Product]:
        """
        Get stored products.
        """
        query = InMemoryCriteriaConverter().convert(criteria)
        return query(self._products, self._reservations)

    def add_product(self, new: Product) -> int:
        """
        Add new product or update if it exists
        """
        to_update = self._get_product(new)
        if to_update:
            self._products.remove(to_update)
        self._products.append(new)

        return new.product_id

    def store_order(self, order: Order):
        """
        Store new order
        """
        if order in self._orders:
            raise ProductAlreadyRequested(
                f"Product {order.product.product_id} already requested for reservation {order.reservation_id}"
            )

        order.product.orders += 1
        self._orders.append(order)

    def _get_product(self, new: Product):
        for p in self._products:
            if p.product_id == new.product_id:
                return p
        return None

    def _in_memory_products(self) -> List[Product]:
        surf = Product(
            product_id="f5e1d3c2-08c7-40b7-8045-f5748e004b9c",
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
            product_id="25dae451-7bf4-41f9-ae2d-2307fa8f38ec",
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
            product_id="bd4ea9f6-e984-46a0-b674-b61302047cb1",
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

        spa = Product(
            product_id="44b260d9-78c9-47f7-a644-afec0482ae03",
            name="spa",
            description="Peaceful spa",
            price=40.0,
            date_added=date(2022, 4, 12),
            orders=20,
            configurations=[
                Configuration(name="date", type="date"),
                Configuration(name="time", type="time"),
                Configuration(name="adults", type="int"),
                Configuration(name="massage", type="boolean"),
            ],
            active=True,
        )
        return [surf, brunch, museum, spa]

    def _in_memory_reservations(self):
        surf, brunch, museum, _ = self._products
        reservation0 = "e0388679-f1f4-4b70-87fe-6dba6c66183b"
        surf.reservations.append(reservation0)
        brunch.reservations.append(reservation0)
        museum.reservations.append(reservation0)

        reservation1 = "1092a4bd-0e7a-42cc-ab12-12d7155ee772"
        brunch.reservations.append(reservation1)
        museum.reservations.append(reservation1)

        reservation2 = "20a3d0a3-5297-4d64-a161-0f2cc29590df"

        return [reservation0, reservation1, reservation2]
