from typing import List

from liexpress.domain.models.criteria import Criteria, Filter, FilterOperator
from liexpress.domain.models.exceptions import (
    ActiveProductNotFound,
    ProductNotFound,
    ReservationIdNotFound,
)
from liexpress.domain.models.products import Product


class InMemoryCriteriaConverter:
    OPERATORS = {
        FilterOperator.EQ: lambda x, y: x == y,
        FilterOperator.IDEQ: lambda x, y: x is y,
        FilterOperator.IN: lambda x, y: y in x,
    }

    @classmethod
    def convert(cls, criteria: Criteria):
        return lambda x: cls._convert(x, criteria)

    @classmethod
    def _convert(cls, collection: List[Product], criteria: Criteria):
        for my_filter in criteria.filters:
            collection = cls._filter_products(collection, my_filter)

        if criteria.order:
            collection = sorted(collection, key=lambda x: getattr(x, criteria.order))

        return collection[criteria.offset : criteria.offset + criteria.limit]

    @classmethod
    def _filter_products(cls, collection: List[Product], my_filter: Filter):
        collection = list(
            filter(
                lambda x: cls.OPERATORS[my_filter.operator](
                    getattr(x, my_filter.field), my_filter.value
                ),
                collection,
            )
        )
        if not collection and my_filter.field == "reservations":
            raise ReservationIdNotFound(f"Reservation {my_filter.value} not found")

        if not collection and my_filter.field == "active":
            raise ActiveProductNotFound("No active products found")

        if not collection and my_filter.field == "product_id":
            raise ProductNotFound(f"Product {my_filter.value} not found")

        return collection
