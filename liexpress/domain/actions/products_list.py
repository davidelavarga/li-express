import logging

import inject

from liexpress.domain.models.products import ProductSorter
from liexpress.domain.ports import Repository


class ProductList:
    @inject.autoparams()
    def __init__(self, data_provider: Repository):
        self.data_provider = data_provider

    def __call__(self, reservation_id: int, order_by: str, active: bool):
        logging.info(f"Getting product for reservation {reservation_id} ..")
        products = self.data_provider.get_products_by_reservation_id(reservation_id)

        if active:
            products = products.filter_active()

        logging.info(f"Ordering products by {order_by} ..")
        return ProductSorter(products.products)(order_by)
