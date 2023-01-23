from logging import LoggerAdapter
from .context import get_trace_id


__all__ = ["TracingLoggerAdapter"]


class TracingLoggerAdapter(LoggerAdapter):

    __slots__ = ()

    def process(self, msg, kwargs):
        kwargs["extra"] = self.extra

        trace_id = get_trace_id()
        if trace_id is not None:
            return msg + f"(trace_id: {trace_id})", kwargs

        return msg, kwargs
