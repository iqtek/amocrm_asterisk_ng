import pytest

from asterisk_amocrm.infrastructure.dispatcher import get_dispatcher
from asterisk_amocrm.infrastructure.dispatcher import IDispatcher
from asterisk_amocrm.infrastructure.dispatcher import IQuery


@pytest.fixture()
def dispatcher() -> IDispatcher:
    return get_dispatcher()


@pytest.mark.asyncio
async def test_add_function(dispatcher) -> None:
    my_result = 123456
    dispatcher: IDispatcher

    class ISomeQuery(IQuery[int]):
        async def __call__(self, *args, **kwargs) -> int:
            raise NotImplementedError()

    class SomeQueryImpl(ISomeQuery):
        async def __call__(self, *args, **kwargs) -> int:
            nonlocal my_result
            return my_result

    dispatcher.add_function(
        function_type=ISomeQuery,
        function=SomeQueryImpl(),
    )

    function = dispatcher.get_function(
        function_type=ISomeQuery,
    )

    result = await function()
    assert result == my_result
