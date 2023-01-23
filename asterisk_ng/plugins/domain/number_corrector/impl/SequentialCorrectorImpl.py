from typing import Sequence

from ..core import INumberCorrector


__all__ = ["SequentialCorrectorImpl"]


class SequentialCorrectorImpl(INumberCorrector):

    __slots__ = (
        "__correctors",
        "__as_pipeline",
    )

    def __init__(
        self,
        correctors: Sequence[INumberCorrector],
        as_pipeline: bool = True,
    ) -> None:
        self.__correctors = correctors
        self.__as_pipeline = as_pipeline

    def correct(self, phone: str) -> str:
        result: str = phone
        for corrector in self.__correctors:
            try:
                result = corrector.correct(result)
            except Exception as exc:
                if not self.__as_pipeline:
                    return phone
        return result
