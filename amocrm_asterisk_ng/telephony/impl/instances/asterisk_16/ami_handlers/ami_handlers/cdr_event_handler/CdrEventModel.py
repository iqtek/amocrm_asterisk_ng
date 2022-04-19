from pydantic import BaseModel
from pydantic import Field


__all__ = [
    "CdrEventModel",
]


class CdrEventModel(BaseModel):
    unique_id = Field(alias="Uniqueid")
    channel = Field(alias="Channel")
    destination_channel = Field(alias="DestinationChannel")
    duration = Field(alias="Duration")
    disposition = Field(alias="Disposition")
    str_start_time = Field(alias="StartTime")
    str_end_time = Field(alias="EndTime")
