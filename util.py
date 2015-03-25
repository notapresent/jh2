import time


def retry_on_exception(retryable=None, retry_count=3, initial_delay=5):
    """Retry call if function raises retryable exception"""
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            mtries = retry_count + 1
            delay = initial_delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except Exception as err:
                    # Re-raise if non-retryable error
                    if retryable is not None and type(err) not in retryable:
                        raise

                    time.sleep(delay)
                    mtries -= 1
                    delay = delay * 2

            # Only one last try left
            return f(*args, **kwargs)

        return wrapped_f
    return wrap
