from amocrm_asterisk_ng.infrastructure import InitializableComponent


__all__ = [
    "WidgetViewComponent",
]


class WidgetViewComponent(InitializableComponent):

    __slots__ = (
        "__app",
    )

    async def initialize(self) -> None:
        self.__app.add_route(
            "/amocrm/calls",
            self.__origination_view.handle,
            methods=["GET"]
        )

    async def deinitialize(self) -> None:
        self.__app.routes.remove(widget_view)
