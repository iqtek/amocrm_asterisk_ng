from typing import List
from asterisk_amocrm.infrastructure.dispatcher import ICommand


__all__ = [
    "RaiseCardCommand",
]


class RaiseCardCommand(ICommand):
    phone_number: str
    users: List[int]
