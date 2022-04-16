import logging

import inject

from liexpress.domain.models.criteria import Criteria, Filter, FilterOperator
from liexpress.domain.ports import Repository


class ProductDetail:
    @inject.autoparams()
    def __init__(self, data_provider: Repository):
        self.data_provider = data_provider

    def __call__(self, product_id: int):
        logging.info(f"Getting product {product_id} ..")

        criteria = Criteria(
            order="date_added",
            limit=1,
            offset=0,
            filters=[
                Filter("product_id", FilterOperator.EQ, product_id),
            ],
        )
        product = self.data_provider.get_products(criteria)[0]

        logging.info(f" Product {product.name} has been found")
        return product
