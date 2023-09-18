import typing as t

from pydantic import BaseModel


__all__ = ["PluginStoreConfig"]


class PluginStoreConfig(BaseModel):
    uploaded: t.Sequence[str] = []
    plugins_settings: t.Mapping[str, t.Mapping[str, t.Any]] = {}
