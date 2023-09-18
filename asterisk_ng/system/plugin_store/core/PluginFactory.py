import typing as t

from .Plugin import Plugin


__all__ = ["PluginFactory"]


class PluginFactory:

    __slots__ = ()

    def __call__(self, settings: t.Mapping[str, t.Any]) -> Plugin:
        raise NotImplementedError()
