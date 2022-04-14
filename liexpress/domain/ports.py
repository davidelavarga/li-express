from abc import ABC, abstractmethod
from typing import List

from liexpress.domain.models.products import Product


class DataProvider(ABC):
    @abstractmethod
    def get_products(self, active: bool = True) -> List[Product]:
        """
        Get products.
        If active=True return only active product,
        return all products otherwise.
        """
        pass
