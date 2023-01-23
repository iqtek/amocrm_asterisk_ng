from asyncio import AbstractEventLoop
from asyncio import Task

from typing import Any
from typing import Mapping
from typing import Optional

from fastapi import FastAPI
from uvicorn import Config
from uvicorn import Server

from asterisk_ng import __description__
from asterisk_ng import __name__
from asterisk_ng import __version__

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver

from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .FastapiPluginConfig import FastapiPluginConfig
from starlette.middleware.cors import CORSMiddleware


__all__ = ["FastapiPlugin"]


class FastapiPlugin(AbstractPlugin):

    __slots__ = (
        "__server",
        "__serve_task",
    )

    def __init__(self) -> None:
        self.__server: Optional[Server] = None
        self.__serve_task: Optional[Task] = None

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[Key(AbstractEventLoop)],
            ),
            exported=Interface(
                container=[Key(FastAPI)],
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        event_loop = container.resolve(Key(AbstractEventLoop))

        config = FastapiPluginConfig(**settings)

        app = FastAPI(
            title=__name__,
            version=__version__,
            description=__description__,
            swagger_ui_parameters={"defaultModelsExpandDepth": -1}
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
        )

        config = Config(
            app=app,
            host=config.host,
            port=config.port,
            workers=config.workers,
        )

        self.__server = Server(config=config)

        self.__serve_task = event_loop.create_task(self.__server.serve())
        container.set_resolver(Key(FastAPI), SingletonResolver(app))

    async def unload(self) -> None:
        container.delete_resolver(Key(FastAPI))
        await self.__server.shutdown()
        self.__serve_task.cancel()
