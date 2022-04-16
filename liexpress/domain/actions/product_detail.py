import logging

import inject

from liexpress.domain.models.criteria import Criteria, Filter, FilterOperator
from liexpress.domain.ports import Repository


class ProductDetail:
    @inject.autoparams()
    def __init__(self, repository: Repository):
        self.repository = repository

    def __call__(self, product_id: int):
        logging.info(f"Getting product {product_id} ..")

        criteria = Criteria(
            order=None,
            limit=1,
            offset=0,
            filters=[
                Filter("product_id", FilterOperator.EQ, product_id),
            ],
        )
        product = self.repository.get_products(criteria)[0]

        logging.info(f" Product {product.name} has been found")
        return product
