from pydantic import BaseModel

from .OperatorStatus import OperatorStatus
from .ConversationProperties import ConversationProperties


__all__ = [
    "OperatorState",
]


class OperatorState(BaseModel):
    status: OperatorStatus = OperatorStatus.DISABLED
    talking_info: Optional[ConversationProperties] = None

    class Config:
        use_enum_values = True
