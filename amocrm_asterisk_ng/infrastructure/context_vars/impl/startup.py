from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import ioc

from .logger_filter import TraceFilter
from .MakeContextSnapshotFunction import MakeContextSnapshotFunction
from .SetContextVarsFunction import SetContextVarsFunction
from .trace_id import trace_id, TraceIdValueFactory
from ..core import IMakeContextSnapshotFunction
from ..core import ISetContextVarsFunction


__all__ = [
    "context_vars_startup",
]


def context_vars_startup() -> None:

    variables = [trace_id]
    make_context_snapshot_function = MakeContextSnapshotFunction(variables)

    set_context_vars_function = SetContextVarsFunction()

    set_context_vars_function.add_context_var(
        context_var=trace_id,
        value_factory=TraceIdValueFactory(),
    )

    ioc.set_instance(
        key=ISetContextVarsFunction,
        instance=set_context_vars_function,
    )

    ioc.set_instance(
        key=IMakeContextSnapshotFunction,
        instance=make_context_snapshot_function,
    )

    logger = ioc.get_instance(ILogger)
    logger.addFilter(TraceFilter(variables))
