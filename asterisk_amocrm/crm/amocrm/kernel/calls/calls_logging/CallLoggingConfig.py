from pydantic import BaseModel
from pydantic import AnyUrl


__all__ = [
    "CallLoggingConfig",
]


class CallLoggingConfig(BaseModel):
    internal_number_regex: str
    tmp_directory: str
    base_url: AnyUrl
    source: str
    source_uid: str
    service_code: str
    pipeline_id: int
    postprocessing_delay: int
