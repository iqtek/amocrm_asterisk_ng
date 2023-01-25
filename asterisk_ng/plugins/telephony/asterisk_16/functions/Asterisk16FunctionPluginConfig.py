from pydantic import BaseModel


__all__ = ["Asterisk16FunctionPluginConfig"]


class Asterisk16FunctionPluginConfig(BaseModel):
    origination_context: str = "from-internal"
    origination_timeout: int = 30_000
    redirect_context: str = "from-internal"
