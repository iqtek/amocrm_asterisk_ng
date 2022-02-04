from typing import (
    Mapping,
    Any
)
from fastapi import FastAPI
from asterisk_amocrm.infrastructure import (
    IComponent,
    IFactory,
    IDispatcher,
    IEventBus,
    ILogger,
)
from .AsteriskWidgetComponent import AsteriskWidgetComponent
from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .views import OriginationView
from asterisk_amocrm.infrastructure.context_vars import (
    AddContextVarFunction,
    TraceIdValueFactory,
    trace_id,
)

__all__ = [
    "AsteriskWidgetComponentFactory"
]


class AsteriskWidgetComponentFactory(IFactory):

    def __init__(
        self,
        app: FastAPI,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__logger = logger

    @classmethod
    def type(cls) -> str:
        return "asterisk_widget"

    def get_instance(self, settings: Mapping[str, Any]) -> IComponent:

        config = AsteriskWidgetConfig(**settings)

        value_factory = TraceIdValueFactory()
        add_context_var_function = AddContextVarFunction(
            context_var=trace_id,
            value_factory=value_factory,
        )

        origination_view = OriginationView(
            config=config,
            event_bus=self.__event_bus,
            add_context_var_function=add_context_var_function,
            logger=self.__logger,
        )

        component = AsteriskWidgetComponent(
            config=config,
            app=self.__app,
            dispatcher=self.__dispatcher,
            origination_view=origination_view,
            logger=self.__logger,
        )
        return component
