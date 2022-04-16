from datetime import date

import pytest

from liexpress.domain.models.products import Configuration, Product


@pytest.fixture
def product() -> Product:
    return Product(
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
        reservations=[0],
    )


def test_check_configurations_happy_path(product: Product):
    confs = [
        Configuration(name="date", type="date"),
        Configuration(name="time", type="time"),
        Configuration(name="additional notes", type="string"),
    ]

    assert product.check_configurations(confs)


def test_check_configurations_less_confs(product: Product):
    confs = [
        Configuration(name="date", type="date"),
        Configuration(name="time", type="time"),
    ]

    assert product.check_configurations(confs) is False


def test_check_configurations_bad_confs(product: Product):
    confs = [
        Configuration(name="date", type="date"),
        Configuration(name="time", type="time"),
        Configuration(name="bad", type="bad"),
    ]

    assert product.check_configurations(confs) is False
