import logging

import inject

from liexpress.domain.ports import Repository


class ProductDetail:
    @inject.autoparams()
    def __init__(self, data_provider: Repository):
        self.data_provider = data_provider

    def __call__(self, product_id: int):
        logging.info(f"Getting product {product_id} ..")

        product = self.data_provider.get_product(product_id)

        logging.info(f" Product {product.name} has been found")
        return product
