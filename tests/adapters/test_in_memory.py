from datetime import date

import pytest

from liexpress.adapters.repository.in_memory import InMemoryRepository
from liexpress.adapters.repository.in_memory_criteria import (
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

    assert len(products) == 4


def test_get_products_by_id():
    criteria = Criteria(
        order=None,
        limit=10,
        offset=0,
        filters=[
            Filter(
                "product_id", FilterOperator.EQ, "f5e1d3c2-08c7-40b7-8045-f5748e004b9c"
            ),
        ],
    )

    im = InMemoryRepository()
    product = im.get_products(criteria)[0]

    assert product.product_id == "f5e1d3c2-08c7-40b7-8045-f5748e004b9c"
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
    assert [p.product_id for p in products] == [
        "25dae451-7bf4-41f9-ae2d-2307fa8f38ec",
        "bd4ea9f6-e984-46a0-b674-b61302047cb1",
    ]


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
            product_id="44b260d9-78c9-47f7-a644-afec0482ae03",
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
