import logging
from datetime import date
from typing import List

import inject

from liexpress.domain.models.products import Configuration, Product
from liexpress.domain.ports import Repository


class ProductCreator:
    @inject.autoparams()
    def __init__(self, data_provider: Repository):
        self.data_provider = data_provider

    def __call__(
        self,
        name: str,
        description: str,
        price: str,
        configurations: List[Configuration],
    ):
        logging.info(f"Creating new product {name} ..")

        products = self.data_provider.get_products()

        product_id = products.get_highest_product_id()

        new = Product(
            product_id=product_id,
            name=name.lower(),
            description=description,
            price=price,
            date_added=date.today(),
            configurations=configurations,
            orders=0,
            active=True,
        )
        product_id = self.data_provider.add_product(new)

        logging.info(f"Product {product_id} has been added")
        return product_id
