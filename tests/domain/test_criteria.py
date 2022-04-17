import pytest

from liexpress.adapters.repository.in_memory_criteria import Criteria
from liexpress.domain.models.exceptions import OrderCriteriaNotSupported


def test_order_criteria_not_supported():
    with pytest.raises(OrderCriteriaNotSupported):
        Criteria(
            order="fail",
            limit=10,
            offset=0,
            filters=[],
        )
