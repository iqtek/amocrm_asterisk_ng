__all__ = [
    "IAddContextVarFunction",
]


class IAddContextVarFunction:

    def __call__(self) -> None:
        raise NotImplementedError()
