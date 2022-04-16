import logging

import inject

from liexpress.domain.models.criteria import Criteria, Filter, FilterOperator
from liexpress.domain.ports import Repository


class ProductList:
    @inject.autoparams()
    def __init__(self, repository: Repository):
        self.repository = repository

    def __call__(self, reservation_id: int, order_by: str, active: bool):
        logging.info(f"Getting product for reservation {reservation_id} ..")
        logging.info(f"Ordering products by {order_by}")

        criteria = Criteria(
            order=order_by,
            limit=10,
            offset=0,
            filters=[
                Filter("reservations", FilterOperator.IN, reservation_id),
                Filter("active", FilterOperator.IDEQ, active),
            ],
        )
        products = self.repository.get_products(criteria)
        return products
