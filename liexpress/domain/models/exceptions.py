class InputException(Exception):
    pass


class OrderCriteriaNotSupported(InputException):
    pass


class ReservationIdNotFound(InputException):
    pass


class ProductNotFound(InputException):
    pass


class BadConfigurationError(InputException):
    pass


class ProductAlreadyRequested(InputException):
    pass


class ActiveProductNotFound(Exception):
    pass
