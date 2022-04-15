from liexpress.adapters.data_provider.in_memory import InMemoryDataProvider


def test_get_products():
    im = InMemoryDataProvider()
    products = im.get_products()

    assert len(products.products) == 3


def test_get_products_by_reservation_id():
    im = InMemoryDataProvider()
    products = im.get_products_by_reservation_id(1)

    assert len(products.products) == 2
    assert [p.product_id for p in products.products] == [1, 2]
