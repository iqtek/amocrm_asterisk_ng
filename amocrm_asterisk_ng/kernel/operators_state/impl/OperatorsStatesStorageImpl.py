from asyncio import Future
from asyncio.exceptions import InvalidStateError

from amocrm_asterisk_ng.infrastructure import IKeyValueStorage

from .utils import state_from_json
from .utils import state_to_json

from ..core import IOperatorsStatesStorage
from ..core import OperatorState


__all__ = [
    "OperatorsStatesStorageImpl",
]


class OperatorsStatesStorageImpl(IOperatorStates):

    STORAGE_PREFIX: str = "operator-state"

    __slots__ = (
        "__key_value_storage",
        "__futures",
    )

    def __init__(self, key_value_storage: IKeyValueStorage) -> None:
        self.__key_value_storage = key_value_storage
        self.__futures: MutableMapping[int, Collection[Future[OperatorState]]] = defaultdict(list)

    def get_key_by_amouser_id(self, amouser_id: int) -> str:
        return f"{self.STORAGE_PREFIX}-{amouser_id}"

    async def set_state(self, amouser_id: int, state: OperatorState) -> None:
        key = get_key_by_amouser_id(amouser_id)
        operator_state_json = state_to_json(state)

        await self.__key_value_storage.set(key, operator_state_json)

        if amouser_id in self.__futures.keys():
            futures = self.__futures[user_id]
            for future in futures:
                try:
                    future.set_result(state)
                except InvalidStateError:
                    pass
            futures.clear()

    async def get_state(self, amouser_id: int) -> OperatorState:
        operator_state_json = await self.__key_value_storage.get(get_key_by_amouser_id(amouser_id))
        return state_from_json(operator_state_json)

    async def get_state_difference(self, amouser_id: int, timeout: float = 10) -> OperatorState:
        future = Future()
        self.__futures[amouser_id].append(future)
        return await asyncio.wait_for(future, timeout=timeout)

    async def delete_state(self, amouser_id: int) -> None:
        await self.__key_value_storage.delete(get_key_by_amouser_id(amouser_id))
