from asterisk_amocrm.infrastructure import ICommand


__all__ = [
    "AddCallToUnsortedCommand",
]


class AddCallToUnsortedCommand(ICommand):

    source_name: str
    source_uid: str
    pipeline_id: int
    created_at: int
    uniq: str
    duration: int
    service_code: str
    link: str
    called: str
    created_at: int
    caller: str
