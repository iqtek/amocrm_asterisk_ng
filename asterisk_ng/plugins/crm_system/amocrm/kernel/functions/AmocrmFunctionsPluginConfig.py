from pydantic import BaseModel


__all__ = ["AmocrmFunctionsPluginConfig"]


class AmocrmFunctionsPluginConfig(BaseModel):
    pipeline: str = "Воронка"
    source: str = "AsteriskNG"
    source_uid: str = "AsteriskNG"
    source_name: str = "AsteriskNG"
    service_code: str = "AsteriskNG"
