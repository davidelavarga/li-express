import logging

import inject

from liexpress.domain.ports import DataProvider


class ProductDetail:
    @inject.autoparams()
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider

    def __call__(self, reservation_id: int, product_id: int):
        logging.info(
            f"Getting product {product_id} for reservation {reservation_id} .."
        )

        product = self.data_provider.get_product(reservation_id, product_id)

        logging.info(
            f" Product {product.name} for reservation {reservation_id} has been found"
        )
        return product
