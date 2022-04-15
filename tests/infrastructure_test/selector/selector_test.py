import pytest

from amocrm_asterisk_ng.infrastructure.selector import (
    ISelectable,
    ISelector,
    SelectorImpl,
)


class Interface(ISelectable):

    def a(self) -> None:
        pass


class ConcreteItem1(Interface):

    def unique_tag(self) -> str:
        return "foo"


class ConcreteItem2(Interface):

    def unique_tag(self) -> str:
        return "bar"


@pytest.fixture()
def selector() -> ISelector[Interface]:
    selector: SelectorImpl[Interface] = SelectorImpl()
    return selector


def test_get_non_existent_item(selector) -> None:

    with pytest.raises(KeyError):
        selector.get_item("foo")


def test_get_item(selector) -> None:

    item = ConcreteItem1()
    selector.add_item(item)
    assert selector.get_item("foo") is item


def test_get_different_items(selector) -> None:

    item1 = ConcreteItem1()
    item2 = ConcreteItem2()
    selector.add_item(item1)
    selector.add_item(item2)

    assert selector.get_item("foo") is item1
    assert selector.get_item("bar") is item2
