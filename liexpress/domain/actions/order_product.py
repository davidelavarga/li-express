import logging
from typing import List
from uuid import uuid4

import inject

from liexpress.domain.models.criteria import Criteria, Filter, FilterOperator
from liexpress.domain.models.exceptions import BadConfigurationError, ProductNotFound
from liexpress.domain.models.orders import Order
from liexpress.domain.models.products import Configuration
from liexpress.domain.ports import Repository


class OrderProduct:
    @inject.autoparams()
    def __init__(self, repo: Repository):
        self.repo = repo

    def __call__(
        self,
        reservation_id: int,
        product_id: int,
        configurations: List[Configuration],
    ):
        logging.info(f"Ordering product {product_id} ..")

        products = self.repo.get_products(
            criteria=Criteria(
                order=None,
                limit=1,
                offset=0,
                filters=[
                    Filter("reservation_exists", FilterOperator.IN, reservation_id),
                    Filter("product_id", FilterOperator.EQ, product_id),
                ],
            )
        )
        if not products:
            raise ProductNotFound(f"Product {product_id} not found")

        product = products[0]
        if not product.check_configurations(configurations):
            raise BadConfigurationError(
                f"Configurations {configurations} does not match with product configurations: {product.configurations} "
            )

        order = Order(
            order_id=str(uuid4()), reservation_id=reservation_id, product=product
        )

        logging.info(f"Storing order {order.order_id} ..")
        self.repo.store_order(order)

        return order.order_id
