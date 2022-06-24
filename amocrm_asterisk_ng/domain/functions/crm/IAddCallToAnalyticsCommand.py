from typing import Literal

from glassio.dispatcher import ICommand


__all__ = [
    "EntityWithThisNumberNotExistException",
    "IAddCallToAnalyticsCommand",
]


class EntityWithThisNumberNotExistException(Exception):
    pass


class IAddCallToAnalyticsCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        unique_id: str,
        phone_number: str,
        direction: Literal["inbound", "outbound"],
        duration: int,
        source: str,
        created_at: int,
        responsible_user_id: int,
        call_status: int,
        call_result: str,
    ) -> None:
        """
        Add cal to amoCRM Analytics.

        If an entity with such a number is not in the database,
        then the call will not be added.

        :raise EntityWithThisNumberNotExistException: If pass
        """
        raise NotImplementedError()
