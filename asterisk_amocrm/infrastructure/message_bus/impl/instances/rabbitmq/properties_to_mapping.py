from dataclasses import asdict
from dataclasses import fields
import time
from typing import Any
from typing import Mapping

from aioamqp.properties import Properties as AioamqpProperties
from aioamqp.constants import MESSAGE_PROPERTIES
from ....core import Properties

__all__ = [
    "properties_to_mapping",
    "mapping_to_properties",
]


def properties_to_mapping(properties: Properties) -> Mapping[str, Any]:
    """
    Bring the Properties to match so it
    can be crafted into an AioamqpProperties.
    """
    dict_properties = asdict(properties)

    float_expiration = dict_properties["expiration"]

    if float_expiration is not None:
        float_expiration = int(float_expiration * 1000)
        dict_properties["expiration"] = str(float_expiration)

    return dict_properties


def mapping_to_properties(aioamqp_properties: AioamqpProperties) -> Properties:

    required_fields = [field.name for field in fields(Properties)]

    values = [aioamqp_properties.__getattribute__(key) for key in required_fields]

    dict_properties = dict(zip(required_fields, values))

    for key in dict_properties.keys():
        if dict_properties[key] == "":
            dict_properties[key] = None

    str_expiration = dict_properties["expiration"]

    try:
        float_expiration = int(str_expiration) / 1000.0
    except Exception:
        pass
    else:
        dict_properties["expiration"] = float_expiration

        timestamp = dict_properties["timestamp"]
        if timestamp is None:
            dict_properties["timestamp"] = int(time.time())

    return Properties(**dict_properties)
