from abc import ABC, abstractmethod

from liexpress.domain.models.products import Product, Products


class DataProvider(ABC):
    @abstractmethod
    def get_products(self) -> Products:
        """
        Get all stored products for the given reservation_id.
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

    @abstractmethod
    def get_products_by_reservation_id(self, reservation_id: int) -> Products:
        """
        Get products for the given reservation_id.
        """
        pass

    @abstractmethod
    def add_product(self, new: Product) -> int:
        """
        Add new product
        """
        pass
