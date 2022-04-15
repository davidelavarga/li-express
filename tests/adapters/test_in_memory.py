from datetime import date

from liexpress.adapters.data_provider.in_memory import InMemoryRepository
from liexpress.domain.models.products import Configuration, Product


def test_get_products():
    im = InMemoryRepository()
    products = im.get_products()

    assert len(products.products) == 3


def test_get_products_by_reservation_id():
    im = InMemoryRepository()
    products = im.get_products_by_reservation_id(1)

    assert len(products.products) == 2
    assert [p.product_id for p in products.products] == [1, 2]


def test_add_new_product():
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

    assert product_id in [p.product_id for p in im.get_products().products]
