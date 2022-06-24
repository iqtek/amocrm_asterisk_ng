from typing import Optional

from pydantic import BaseModel


__all__ = [
    "ClassicScenarioConfig",
    "CallCompletedEventHandlerConfig",
]


class CallCompletedEventHandlerConfig(BaseModel):
    postprocessing_delay: int = 30
    source: str = "amocrm_asterisk_ng"
    source_name: str = "amocrm_asterisk_ng"
    source_uid: str = "amocrm_asterisk_ng"
    service_code: str = "amocrm_asterisk_ng"
    pipeline_name: str = "Воронка"


class ClassicScenarioConfig(BaseModel):
    call_logging: CallCompletedEventHandlerConfig
    internal_number_pattern: Optional[str] = None
