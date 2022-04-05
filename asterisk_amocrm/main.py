from typing import Any
from typing import Mapping

from fastapi import FastAPI
from uvicorn import run

from .integration import ServerConfig
from .integration import IntegrationFactory
from .integration import IntegrationLauncher
from .version import APP_VERSION


__all__ = [
    "main",
]


def main(settings: Mapping[str, Any]) -> None:

    integration_config = ServerConfig(
        **settings["infrastructure"]["integration"],
    )

    app = FastAPI(debug=True)

    integration_factory = IntegrationFactory(
        app=app,
        current_app_version=APP_VERSION,
    )
    integration_launcher = IntegrationLauncher(
        integration_factory=integration_factory,
        settings=settings,
    )

    app.add_event_handler("startup", integration_launcher.handle_startup)
    app.add_event_handler("shutdown", integration_launcher.handle_shutdown)

    run(
        app,
        host=integration_config.host,
        port=integration_config.port,
    )
