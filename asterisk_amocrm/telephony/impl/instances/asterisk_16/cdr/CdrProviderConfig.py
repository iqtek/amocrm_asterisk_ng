from typing import Mapping, Any
from pydantic import BaseModel


__all__ = [
    "CdrProviderConfig",
]


class CdrProviderConfig(BaseModel):

    mysql: Mapping[str, Any]
    media_root: str
    tmp_media_root: str
    wav_extension: str = "wav"
