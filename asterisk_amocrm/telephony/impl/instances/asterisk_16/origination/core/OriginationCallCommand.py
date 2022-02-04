from asterisk_amocrm.infrastructure.dispatcher import ICommand


__all__ = [
    "OriginationCallCommand",
]


class OriginationCallCommand(ICommand):

    caller_phone_number: str
    called_phone_number: str
