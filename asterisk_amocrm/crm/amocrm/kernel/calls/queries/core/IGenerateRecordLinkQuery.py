from asterisk_amocrm.infrastructure import IQuery


class IGenerateRecordLinkQuery(IQuery[str]):

    async def __call__(self, unique_id: str) -> str:
        raise NotImplementedError()
