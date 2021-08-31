def with_retry(method, exception_class, max_retries=3):
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
