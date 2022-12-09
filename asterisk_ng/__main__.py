from asyncio import Event
from asyncio import get_running_loop
from asyncio import run
import argparse
from signal import SIGINT

import uvloop

from asterisk_ng.system.application import Application
from asterisk_ng.system.configurator import ConfiguratorComponentImpl
from asterisk_ng.system.configurator import ConfiguratorConfig
from asterisk_ng.system.greeting import greet


async def main(application: Application) -> None:
    stop_event = Event()
    event_loop = get_running_loop()

    await application.handle_startup()

    event_loop.add_signal_handler(SIGINT, stop_event.set)
    await stop_event.wait()
    await application.handle_shutdown()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='AsteriskNG')
    parser.add_argument("--config", type=str, default="config.yml", help='Config file.')
    args = parser.parse_args()

    configurator = ConfiguratorComponentImpl(
        ConfiguratorConfig(
            config_path=args.config,
            enable_saving=False,
        )
    )
    application = Application(configurator)

    greet()
    uvloop.install()
    run(main(application))
