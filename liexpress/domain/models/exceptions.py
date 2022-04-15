class InputException(Exception):
    pass


class OrderCriteriaNotSupported(InputException):
    pass


class ReservationIdNotFound(InputException):
    pass


class ProductNotFound(InputException):
    pass
