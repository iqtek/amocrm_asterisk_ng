from pydantic import BaseModel, AnyUrl


__all__ = [
    "CallLoggingConfig",
]


class CallLoggingConfig(BaseModel):
    webhook_url: AnyUrl
    source: str
    source_uid: str
    service_code: str
    pipeline_id: int
    postprocessing_delay: int
