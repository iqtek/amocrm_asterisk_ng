from pydantic import BaseModel


__all__ = [
    "CallRecordsConfig",
]


class CallRecordsConfig(BaseModel):
    tmp_directory: str
