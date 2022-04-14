from datetime import date
from typing import List

import pytest

from liexpress.domain.models.exceptions import OrderCriteriaNotSupported
from liexpress.domain.models.products import Configuration, Product, ProductSorter


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
