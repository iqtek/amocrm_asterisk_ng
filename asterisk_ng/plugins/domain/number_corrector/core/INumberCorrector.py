__all__ = "INumberCorrector"


class INumberCorrector:

    __slots__ = ()

    def correct(self, phone: str) -> str:
        raise NotImplementedError()
