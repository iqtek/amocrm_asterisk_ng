from logging import Filter

from glassio.context import get_context


__all__ = [
    "TraceIdFilter",
]


class TraceIdFilter(Filter):

    __slots__ = ()

    def filter(self, record):
        context = get_context()
        trace_id = context.get("trace_id", "undefined")
        record.trace_id = trace_id
        return True
