from fastapi import FastAPI
from uvicorn import config

import yaml

from .integration import IntegrationFactory
from .integration import IntegrationLauncher
from .version import APP_VERSION


__all__ = [
    "app",
]


app = FastAPI()
integration_launcher: IntegrationLauncher


async def handle_startup() -> None:

    global integration_launcher

    with open('./configs/config.yml') as config_file:
        settings = yaml.safe_load(config_file)

    integration_factory = IntegrationFactory(
        app=app,
        current_app_version=APP_VERSION,
    )

    integration_launcher = IntegrationLauncher(
        integration_factory=integration_factory,
        settings=settings,
    )

    await integration_launcher.handle_startup()


async def handle_shutdown() -> None:
    global integration_launcher
    await integration_launcher.handle_shutdown()


app.add_event_handler("startup", handle_startup)
app.add_event_handler("shutdown", handle_shutdown)
