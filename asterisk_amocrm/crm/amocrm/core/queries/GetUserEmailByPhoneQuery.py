from asterisk_amocrm.infrastructure.dispatcher import IQuery

__all__ = [
    "GetUserEmailByPhoneQuery"
]


class GetUserEmailByPhoneQuery(IQuery):
    phone_number: str
