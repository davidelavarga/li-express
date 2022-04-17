from dataclasses import dataclass
from enum import Enum
from typing import List

from liexpress.domain.models.exceptions import OrderCriteriaNotSupported
from liexpress.utils.config_loader import get_config


class FilterOperator(Enum):
    EQ = 1
    IDEQ = 2
    IN = 3


@dataclass
class Filter:
    field: str
    operator: FilterOperator
    value: str


class Criteria:
    def __init__(
        self, order: str, limit: int, offset: int, filters: List[Filter] = None
    ):
        """
        Shared object to apply filter in the repository.
        Filters will be applied in order.
        """
        self.order_filters_supported = get_config()["order_filters_supported"]
        self.order = self._check_order_types(order)
        self.limit = limit
        self.offset = offset
        self.filters = filters or []

    def _check_order_types(self, order: str):
        if order not in self.order_filters_supported:
            raise OrderCriteriaNotSupported(
                f"Order by '{order}' is not supported, only: {self.order_filters_supported}"
            )
        return order
