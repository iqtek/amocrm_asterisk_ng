from typing import Collection
from typing import Mapping

from amocrm_api_client import AmoCrmApiClient

from asterisk_ng.interfaces import CrmUser
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetCrmUsersByEmailsQuery


__all__ = ["GetCrmUsersByEmailsQueryImpl"]


class GetCrmUsersByEmailsQueryImpl(IGetCrmUsersByEmailsQuery):

    __slots__ = (
        "__amo_client",
    )

    def __init__(self, amo_client: AmoCrmApiClient) -> None:
        self.__amo_client = amo_client

    async def __call__(self, emails: Collection[str]) -> Mapping[str, CrmUser]:
        required_emails = set(emails)

        page_count = (await self.__amo_client.users.get_page()).page_count

        result = {}

        for page_index in range(page_count):

            page = await self.__amo_client.users.get_page(page=page_index + 1)

            for user in page.embedded:
                if user.email in required_emails:
                    result[user.email] = CrmUser(
                        id=CrmUserId(
                            id=user.id,
                            email=user.email,
                        ),
                        name=user.name,
                    )
                    required_emails.remove(user.email)

            if len(required_emails) == 0:
                break

        return result
