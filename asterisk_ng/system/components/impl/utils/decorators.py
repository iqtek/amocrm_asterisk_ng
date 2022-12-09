from functools import wraps
from inspect import iscoroutinefunction

from typing import Type
from typing import TypeVar

from ...core import IState
from ...core import InitializableComponent
from ...core import InitializableComponentException


__all__ = [
    "required_state",
]


T = TypeVar("T")


def compare_state(state: Type[IState], current_state: Type[IState]):
    if not issubclass(current_state, state):
        raise InitializableComponentException(
            f"The component must have the `{state}` state. "
            f"Current state: `{current_state}`."
        )


def required_state(state: Type[IState]):
    """
    Specify the state in which the component should be in order to call this method.

    :param state: required state.
    """

    def comparing_state_decorator(method: T) -> T:

        if iscoroutinefunction(method):
            @wraps(method)
            async def asynchronous_wrapper(self: InitializableComponent, *args, **kwargs):
                compare_state(state, type(self.state))
                return await method(self, *args, **kwargs)
            return asynchronous_wrapper

        @wraps(method)
        def synchronous_wrapper(self: InitializableComponent, *args, **kwargs):
            compare_state(state, type(self.state))
            return method(self, *args, **kwargs)

        return synchronous_wrapper

    return comparing_state_decorator
