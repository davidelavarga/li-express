from abc import ABC, abstractmethod
from typing import List

from liexpress.domain.models.criteria import Criteria
from liexpress.domain.models.orders import Order
from liexpress.domain.models.products import Product


class Repository(ABC):
    @abstractmethod
    def get_products(self, criteria: Criteria) -> List[Product]:
        """
        Get stored products.
        """
        pass

    @abstractmethod
    def add_product(self, new: Product) -> int:
        """
        Add new product or update if it exists
        """
        pass

    @abstractmethod
    def store_order(self, order: Order):
        """
        Store new order
        """
