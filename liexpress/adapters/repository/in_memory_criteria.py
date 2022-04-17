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
        return lambda x, y: cls._convert(x, y, criteria)

    @classmethod
    def _convert(
        cls, products: List[Product], reservations: List[str], criteria: Criteria
    ):
        for my_filter in criteria.filters:
            if my_filter.field == "reservation_exists":
                reservations = cls._filter_reservations(reservations, my_filter)
            else:
                products = cls._filter_products(products, my_filter)

        if criteria.order:
            products = sorted(
                products,
                key=lambda x: getattr(x, criteria.order),
                reverse=(criteria.order == "orders"),
            )

        return products[criteria.offset : criteria.offset + criteria.limit]

    @classmethod
    def _filter_reservations(cls, reservations: List[str], my_filter: Filter):
        reservations = list(
            filter(
                lambda x: cls.OPERATORS[my_filter.operator](x, my_filter.value),
                reservations,
            )
        )
        if not reservations:
            raise ReservationIdNotFound(f"Reservation {my_filter.value} not found")

        return reservations

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

        if not collection and my_filter.field == "active":
            raise ActiveProductNotFound("No active products found")

        return collection
