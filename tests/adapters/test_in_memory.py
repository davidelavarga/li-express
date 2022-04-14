from liexpress.adapters.data_provider.in_memory import InMemoryDataProvider


def test_get_active_products():
    im = InMemoryDataProvider()
    active_products = im.get_products(0)

    assert len(active_products) == 2


def test_get_all_products():
    im = InMemoryDataProvider()
    active_products = im.get_products(0, active=False)

    assert len(active_products) == 3
