from abc import ABC, abstractmethod
from typing import List

from liexpress.domain.models.products import Product


class DataProvider(ABC):
    @abstractmethod
    def get_products(self, reservation_id: int, active: bool = True) -> List[Product]:
        """
        Get products for the given reservation_id.
        If active=True return only active product,
        return all products otherwise.
        """
        pass

    @abstractmethod
    def get_product(self, product_id: int) -> Product:
        """
        Get the product for the given product id
        """
        pass
