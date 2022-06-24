from pydantic import BaseModel


__all__ = [
    "CallRecordsConfig",
]


class CallRecordsConfig(BaseModel):
    enable_conversion: bool = True
    tmp_directory: str = "./convert_dir"
