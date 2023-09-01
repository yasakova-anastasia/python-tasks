from datetime import datetime


def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """
    def wrapped(*args, **kwargs):   # type: ignore
        if wrapped.depth == 0:
            wrapped.rdepth = 0
            wrapped.calls = 0

        wrapped.depth += 1
        wrapped.calls += 1
        wrapped.rdepth = max(wrapped.rdepth, wrapped.depth)
        start_time = datetime.now()
        try:
            res = func(*args, **kwargs)
        finally:
            wrapped.depth -= 1
        wrapped.last_time_taken = (datetime.now() - start_time).total_seconds()
        return res

    wrapped.__name__ = func.__name__
    wrapped.__doc__ = func.__doc__
    wrapped.__module__ = func.__module__

    wrapped.depth = 0
    wrapped.rdepth = 0
    wrapped.calls = 0
    return wrapped
