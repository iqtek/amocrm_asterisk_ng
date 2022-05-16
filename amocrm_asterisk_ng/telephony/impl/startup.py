from typing import Any
from typing import Mapping

from fastapi import FastAPI

from glassio.dispatcher import IDispatcher
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig

from .instances import asterisk16_startup
from .redirect_to_responsible import RedirectToResponsibleComponent


__all__ = [
    "telephony_startup",
]


def telephony_startup(
    settings: Mapping[str, Any],
) -> None:

    startup_config = SelectedComponentConfig(**settings)

    control_components = ioc.get("control_components")
    app = ioc.get_instance(FastAPI)
    dispatcher = ioc.get_instance(IDispatcher)

    if startup_config.type != "asterisk_16":
        raise Exception("Integration does not support telephony switching yet.")

    asterisk16_startup(startup_config.settings)
    redirect_to_responsible_component = RedirectToResponsibleComponent(
        app=app,
        dispatcher=dispatcher,
    )

    control_components.append(redirect_to_responsible_component)
