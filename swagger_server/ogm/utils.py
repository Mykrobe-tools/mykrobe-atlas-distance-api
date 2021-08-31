def with_retry(exception_class, max_retries=3):
    def outer_wrapper(method):
        def wrapper(instance, *args, **kwargs):
            count = 0
            while count < max_retries:
                try:
                    return method(instance, *args, **kwargs)
                except exception_class:
                    count += 1
            return method(instance, *args, **kwargs)

        return wrapper
    return outer_wrapper

