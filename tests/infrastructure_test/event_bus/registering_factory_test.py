import pytest

from amocrm_asterisk_ng.infrastructure.event_bus.impl.instances.extended.core import IRegisteringFactory
from amocrm_asterisk_ng.infrastructure.event_bus.impl.instances.extended.impl.event_serialization.RegisteringFactory import RegisteringFactory


class Foo:

    __slots__ = (
        "__bar",
    )

    def __init__(self, bar: str = None) -> None:
        self.__bar = bar

    @property
    def bar(self) -> str:
        return self.__bar


@pytest.fixture()
def registering_factory() -> IRegisteringFactory[Foo]:
    return RegisteringFactory()


def test_get_instance_unregister_type(registering_factory) -> None:

    with pytest.raises(KeyError):
        registering_factory.get_instance("foo")


def test_get_instance(registering_factory) -> None:

    registering_factory.register_type("foo", Foo)

    obj = registering_factory.get_instance(
        type_name='foo',
        bar="value"
    )

    assert obj.bar == "value"
