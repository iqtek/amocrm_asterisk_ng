from .core import Key


__all__ = [
    "UnableToResolveDependency",
    "ResolverNotFound",
]


class ChestException(Exception):
    pass


class UnableToResolveDependency(ChestException):

    def __init__(self, key: Key) -> None:
        super().__init__(f"Unable to resolve dependency by: {key}.")


class ResolverNotFound(ChestException):

    def __init__(self, key: Key) -> None:
        super().__init__(f"Resolver for: {key} not found.")
