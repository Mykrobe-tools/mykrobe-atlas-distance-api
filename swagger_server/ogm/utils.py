def with_retry(method, max_retries=3):
    def wrapper(instance, *args, **kwargs):
        done = False

        for count in range(max_retries):
            if done:
                break

            while True:
                try:
                    method(instance, *args, **kwargs)
                except BufferError:
                    if count == max_retries - 1:
                        raise

                    count += 1
                    continue

                break

    return wrapper