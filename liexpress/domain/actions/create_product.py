import logging
from datetime import date
from typing import List
from uuid import uuid4

import inject

from liexpress.domain.models.products import Configuration, Product
from liexpress.domain.ports import Repository


class ProductCreator:
    @inject.autoparams()
    def __init__(self, repo: Repository):
        self.repo = repo

    def __call__(
        self,
        product_id: str,
        name: str,
        description: str,
        price: str,
        configurations: List[Configuration],
    ):
        logging.info(f"Creating new product {name} ..")

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
        product_id = self.repo.add_product(new)

        logging.info(f"Product {product_id} has been added")
        return product_id
