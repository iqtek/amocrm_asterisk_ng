from pydantic import BaseModel
from pydantic import DirectoryPath


__all__ = [
    "FileConverterPluginConfig",
]


class FileConverterPluginConfig(BaseModel):
    tmp_dir: DirectoryPath = "./tmp"
