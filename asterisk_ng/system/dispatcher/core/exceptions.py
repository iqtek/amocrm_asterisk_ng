__all__ = [
    "DispatcherException",
    "FunctionNotFoundException"
]


class DispatcherException(Exception):
    pass


class FunctionNotFoundException(DispatcherException):
    pass
