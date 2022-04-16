from datetime import date

import pytest

from liexpress.adapters.data_provider.in_memory import InMemoryRepository
from liexpress.adapters.data_provider.in_memory_criteria import (
    Criteria,
    Filter,
    FilterOperator,
)
from liexpress.domain.models.exceptions import ProductNotFound, ReservationIdNotFound
from liexpress.domain.models.products import Configuration, Product


@pytest.fixture
def all_products_criteria() -> Criteria:
    return Criteria(
        order=None,
        limit=10,
        offset=0,
        filters=[],
    )


def test_get_products(all_products_criteria: Criteria):
    im = InMemoryRepository()
    products = im.get_products(all_products_criteria)

    assert len(products) == 3


def test_get_products_by_id():
    criteria = Criteria(
        order=None,
        limit=10,
        offset=0,
        filters=[
            Filter("product_id", FilterOperator.EQ, 0),
        ],
    )

    im = InMemoryRepository()
    product = im.get_products(criteria)[0]

    assert product.product_id == 0
    assert product.name == "surf"


def test_get_products_by_id_not_found():
    criteria = Criteria(
        order=None,
        limit=10,
        offset=0,
        filters=[
            Filter("product_id", FilterOperator.EQ, 6),
        ],
    )
    with pytest.raises(ProductNotFound):
        im = InMemoryRepository()
        im.get_products(criteria)[0]


def test_get_products_by_reservation_id():
    criteria = Criteria(
        order=None,
        limit=10,
        offset=0,
        filters=[
            Filter("reservations", FilterOperator.IN, 1),
        ],
    )

    im = InMemoryRepository()
    products = im.get_products(criteria)

    assert len(products) == 2
    assert [p.product_id for p in products] == [1, 2]


def test_get_products_by_reservation_id_reservation_not_found():
    criteria = Criteria(
        order=None,
        limit=10,
        offset=0,
        filters=[
            Filter("reservations", FilterOperator.IN, 5),
        ],
    )

    with pytest.raises(ReservationIdNotFound):
        im = InMemoryRepository()
        im.get_products(criteria)


def test_add_new_product(all_products_criteria: Criteria):
    im = InMemoryRepository()
    product_id = im.add_product(
        Product(
            product_id=3,
            name="new product",
            description="New product description",
            price=19.9,
            date_added=date.today(),
            configurations=[Configuration(name="name", type="string")],
            orders=0,
            active=True,
        )
    )

    assert product_id in [p.product_id for p in im.get_products(all_products_criteria)]
