from datetime import date
from typing import List

import pytest

from liexpress.domain.models.exceptions import (
    ActiveProductNotFound,
    OrderCriteriaNotSupported,
)
from liexpress.domain.models.products import (
    Configuration,
    Product,
    ProductNotFound,
    ProductSorter,
    ReservationProducts,
)


@pytest.fixture
def products() -> List[Product]:
    return [
        Product(
            product_id=0,
            name="surf",
            description="Amazing surf classes.",
            price=20.0,
            date_added=date(2022, 4, 12),
            orders=2,
            configurations=[
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
            configurations=[
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
            orders=1,
            configurations=[
                Configuration(name="date", type="date"),
                Configuration(name="time", type="time"),
                Configuration(name="adults", type="int"),
                Configuration(name="children", type="int"),
            ],
            active=False,
        ),
    ]


def test_sort_products_by_date(products: List[Product]):
    sorted_products = ProductSorter(products)("date")
    sorted_products_id = [p.product_id for p in sorted_products]
    assert sorted_products_id == [1, 2, 0]


def test_sort_products_by_n_order(products: List[Product]):
    sorted_products = ProductSorter(products)("most_popular")
    sorted_products_id = [p.product_id for p in sorted_products]
    assert sorted_products_id == [1, 0, 2]


def test_sort_products_criteria_not_supported(products: List[Product]):
    with pytest.raises(OrderCriteriaNotSupported):
        ProductSorter(products)("fail")


def test_reservation_products_filter_active(products: List[Product]):
    rp = ReservationProducts(0, products)
    active_products = rp.filter_active()

    products_ids = [p.product_id for p in active_products]

    assert len(active_products) == 2
    assert products_ids == [0, 1]


def test_reservation_products_no_active(products: List[Product]):
    rp = ReservationProducts(0, products[2:])
    with pytest.raises(ActiveProductNotFound):
        rp.filter_active()


def test_reservation_products_find(products: List[Product]):
    rp = ReservationProducts(0, products)
    p = rp.find(0)

    assert p.active is True
    assert p.product_id == 0
    assert p.name == "surf"


def test_reservation_products_product_not_foudnd(products: List[Product]):
    rp = ReservationProducts(0, products)
    with pytest.raises(ProductNotFound):
        rp.find(5)


def test_reservation_products_find_with_no_active(products: List[Product]):
    rp = ReservationProducts(0, products[2:])
    with pytest.raises(ActiveProductNotFound):
        rp.find(0)
