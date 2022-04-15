import logging

import inject

from liexpress.domain.models.products import ProductSorter
from liexpress.domain.ports import DataProvider


class ProductList:
    @inject.autoparams()
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider

    def __call__(self, reservation_id: int, order_by: str, active: bool):
        logging.info(f"Getting product for reservation {reservation_id} ..")
        products = self.data_provider.get_products(reservation_id, active=active)

        logging.info(f"Ordering products by {order_by} ..")
        return ProductSorter(products)(order_by)
