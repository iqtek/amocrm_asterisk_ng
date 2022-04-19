from pydantic import BaseModel

__all__ = [
    "ClassicScenarioConfig",
    "CallCompletedEventHandlerConfig",
]


class CallCompletedEventHandlerConfig(BaseModel):
    postprocessing_delay: int
    source: str
    source_uid: str
    service_code: str
    pipeline_name: str


class ClassicScenarioConfig(BaseModel):
    call_logging: CallCompletedEventHandlerConfig
    internal_number_pattern: str
