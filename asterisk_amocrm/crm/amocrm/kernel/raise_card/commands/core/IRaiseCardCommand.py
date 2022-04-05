from asterisk_amocrm.infrastructure.dispatcher import ICommand
from typing import Collection


__all__ = [
    "IRaiseCardCommand",
]


class IRaiseCardCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        phone_number: str,
        users: Collection[int],
    ) -> None:
        raise NotImplementedError()
