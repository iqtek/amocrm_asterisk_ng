from pydantic import BaseModel


__all__ = ["AmocrmRecordsProviderPluginConfig"]


class AmocrmRecordsProviderPluginConfig(BaseModel):
    base_url: str
    enable_conversion: bool = True
