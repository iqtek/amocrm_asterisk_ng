from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Union


__all__ = [
    "Properties",
    "HeaderValue",
]


HeaderValue = Union[bytes, int]


@dataclass()
class Properties:

    """
    Message properties.

    :param headers: An arbitrary map of headers with string header names.
    :type headers: Mapping[str, HeaderValue]

    :param content_type: MIME content type.
    :type content_type: str
    :param content_encoding: MIME content encoding.
    :type content_encoding: str

    :param message_id: Message id.
    :type message_id: str
    :param correlation_id: Helps correlate requests with responses.
    :type correlation_id: str
    :param message_type: Arbitrary string - a short description of the message.
    :type message_type: str

    :param priority: Priority of the message.
        It is advisable to use numbers in the range [0, 9].
    :type priority: int (non-negative number)
    :param timestamp: Time of publication of the message.
    :type timestamp: int (UNIX timestamp)
    :param expiration: Message TTL (seconds).
    :type expiration: float
    """

    headers: Mapping[str, HeaderValue] = field(default_factory=dict)
    content_type: Optional[str] = None
    content_encoding: Optional[str] = None
    message_id: Optional[str] = None
    correlation_id: Optional[str] = None
    message_type: Optional[str] = None
    priority: Optional[int] = None
    timestamp: Optional[int] = None
    expiration: Optional[float] = None
