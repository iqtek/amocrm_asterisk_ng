from pydantic import BaseModel

from .Interface import Interface


__all__ = ["PluginInterface"]


class PluginInterface(BaseModel):
    imported: Interface = Interface()
    exported: Interface = Interface()
