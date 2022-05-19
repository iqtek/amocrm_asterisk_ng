from typing import Collection

from glassio.dispatcher import ICommand


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
        """
        Raise the incoming call card in the crm.
        """
        raise NotImplementedError()
