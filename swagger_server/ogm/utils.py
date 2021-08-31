def with_retry(exception_class, max_retries=3):
    def outer_wrapper(method):
        def wrapper(instance, *args, **kwargs):
            try:
                return method(instance, *args, **kwargs)
            except exception_class:
                if max_retries == 0:
                    raise

                done = False

                for count in range(max_retries):
                    if done:
                        break

                    while True:
                        try:
                            return method(instance, *args, **kwargs)
                        except exception_class:
                            if count == max_retries - 1:
                                raise

                            count += 1
                            continue

        return wrapper
    return outer_wrapper

