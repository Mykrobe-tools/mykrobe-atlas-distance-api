def capture_logs(func):
    def wrapped(test_case_instance, *args, **kwargs):
        with test_case_instance.assertLogs():
            return func(test_case_instance, *args, **kwargs)

    return wrapped
