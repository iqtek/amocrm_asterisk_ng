from asterisk_amocrm.infrastructure.dispatcher import IQuery


__all__ = [
    "GetUserIdByPhoneQuery"
]


class GetUserIdByPhoneQuery(IQuery):
    phone_number: str
