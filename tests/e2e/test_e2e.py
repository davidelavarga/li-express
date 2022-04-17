import inject
import pytest
from fastapi.testclient import TestClient

from liexpress.adapters.repository.in_memory import InMemoryRepository
from liexpress.domain.actions.create_product import ProductCreator
from liexpress.domain.actions.order_product import OrderProduct
from liexpress.domain.actions.product_detail import ProductDetail
from liexpress.domain.actions.products_list import ProductList
from liexpress.domain.ports import Repository
from liexpress.entrypoints.fastapi import app

# Reservation e0388679-f1f4-4b70-87fe-6dba6c66183b

# Reservation 1092a4bd-0e7a-42cc-ab12-12d7155ee772

# Products
# surf 5e1d3c2-08c7-40b7-8045-f5748e004b9c
# brunch 25dae451-7bf4-41f9-ae2d-2307fa8f38ec
# musseum bd4ea9f6-e984-46a0-b674-b61302047cb1
# spa 44b260d9-78c9-47f7-a644-afec0482ae03

client = TestClient(app)


@pytest.fixture
def injector() -> inject.Injector:
    inject.clear_and_configure(
        lambda binder: binder.bind(Repository, InMemoryRepository())
    )
    yield inject
    inject.clear()


@pytest.fixture
def product_creator(injector) -> ProductCreator:
    return ProductCreator()


@pytest.fixture
def order_product(injector) -> OrderProduct:
    return OrderProduct()


@pytest.fixture
def product_detail(injector) -> ProductDetail:
    return ProductDetail()


@pytest.fixture
def product_list(injector) -> ProductList:
    return ProductList()


def test_list_reservation_product_order_by_n_orders(product_list):
    response = client.get(
        "/reservations/e0388679-f1f4-4b70-87fe-6dba6c66183b/products/?order_by=orders&active_products=true",
        headers={"Authorization": "1234"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "product_id": "25dae451-7bf4-41f9-ae2d-2307fa8f38ec",
            "name": "Brunch",
            "description": "Delicious homemade brunch.",
            "date_added": "2022-04-05",
            "price": 12,
        },
        {
            "product_id": "f5e1d3c2-08c7-40b7-8045-f5748e004b9c",
            "name": "Surf",
            "description": "Amazing surf classes.",
            "date_added": "2022-04-01",
            "price": 20,
        },
    ]


def test_list_reservation_product_order_by_date_added(product_list):
    response = client.get(
        "/reservations/e0388679-f1f4-4b70-87fe-6dba6c66183b/products/?order_by=date_added&active_products=true",
        headers={"Authorization": "1234"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "product_id": "f5e1d3c2-08c7-40b7-8045-f5748e004b9c",
            "name": "Surf",
            "description": "Amazing surf classes.",
            "date_added": "2022-04-01",
            "price": 20,
        },
        {
            "product_id": "25dae451-7bf4-41f9-ae2d-2307fa8f38ec",
            "name": "Brunch",
            "description": "Delicious homemade brunch.",
            "date_added": "2022-04-05",
            "price": 12,
        },
    ]


def test_list_reservation_product_reservation_not_found(product_list):
    response = client.get(
        "/reservations/11111111-f1f4-4b70-87fe-6dba6c66183b/products/?order_by=orders&active_products=true",
        headers={"Authorization": "1234"},
    )
    assert response.status_code == 400


def test_product_detail(product_detail):

    response = client.get(
        "/products/25dae451-7bf4-41f9-ae2d-2307fa8f38ec",
        headers={"Authorization": "1234"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "product_id": "25dae451-7bf4-41f9-ae2d-2307fa8f38ec",
        "name": "Brunch",
        "description": "Delicious homemade brunch.",
        "date_added": "2022-04-05",
        "price": 12,
        "order_fields": [
            {"name": "consumption date", "type": "date"},
            {"name": "brunch type", "type": "string"},
        ],
    }


def test_product_detail_product_not_found(product_detail):

    response = client.get(
        "/products/11111111-7bf4-41f9-ae2d-2307fa8f38ec",
        headers={"Authorization": "1234"},
    )
    assert response.status_code == 400


def test_create_product_new_product(product_creator):

    response = client.put(
        "/products/44b260d9-78c9-47f7-a644-afec0482ae22",
        headers={"Authorization": "1234"},
        json={
            "name": "New",
            "description": "New product description",
            "price": 11.1,
            "order_fields": [
                {"name": "date", "type": "date"},
                {"name": "other", "type": "boolean"},
            ],
        },
    )
    assert response.status_code == 201
    assert response.json()["product_id"] == "44b260d9-78c9-47f7-a644-afec0482ae22"


def test_create_product_product_already_exist(product_creator):

    response = client.put(
        "/products/25dae451-7bf4-41f9-ae2d-2307fa8f38ec",
        headers={"Authorization": "1234"},
        json={
            "name": "New",
            "description": "New product description",
            "price": 11.1,
            "order_fields": [
                {"name": "consumption date", "type": "date"},
                {"name": "brunch type", "type": "string"},
            ],
        },
    )
    assert response.status_code == 201
    assert response.json()["product_id"] == "25dae451-7bf4-41f9-ae2d-2307fa8f38ec"


def test_order_product(order_product):

    response = client.post(
        "/reservations/e0388679-f1f4-4b70-87fe-6dba6c66183b/products/44b260d9-78c9-47f7-a644-afec0482ae03/order",
        headers={"Authorization": "1234"},
        json={
            "order_fields": [
                {"name": "date", "type": "date"},
                {"name": "time", "type": "time"},
                {"name": "adults", "type": "int"},
                {"name": "massage", "type": "boolean"},
            ]
        },
    )
    assert response.status_code == 201


def test_order_product_reservation_not_found(order_product):

    response = client.post(
        "/reservations/11111111-0e7a-42cc-ab12-12d7155ee772/products/44b260d9-78c9-47f7-a644-afec0482ae03/order",
        headers={"Authorization": "1234"},
        json={
            "order_fields": [
                {"name": "date", "type": "date"},
                {"name": "time", "type": "time"},
                {"name": "adults", "type": "int"},
                {"name": "massage", "type": "boolean"},
            ]
        },
    )
    assert response.status_code == 400


def test_order_product_product_not_found(order_product):

    response = client.post(
        "/reservations/1092a4bd-0e7a-42cc-ab12-12d7155ee772/products/11111111-78c9-47f7-a644-afec0482ae03/order",
        headers={"Authorization": "1234"},
        json={
            "order_fields": [
                {"name": "date", "type": "date"},
                {"name": "time", "type": "time"},
                {"name": "adults", "type": "int"},
                {"name": "massage", "type": "boolean"},
            ]
        },
    )
    assert response.status_code == 400


def test_order_product_product_already_ordered(order_product):

    response = client.post(
        "/reservations/1092a4bd-0e7a-42cc-ab12-12d7155ee772/products/11111111-78c9-47f7-a644-afec0482ae03/order",
        headers={"Authorization": "1234"},
        json={
            "order_fields": [
                {"name": "date", "type": "date"},
                {"name": "time", "type": "time"},
                {"name": "adults", "type": "int"},
                {"name": "massage", "type": "boolean"},
            ]
        },
    )
    assert response.status_code == 400
