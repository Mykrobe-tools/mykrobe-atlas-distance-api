from _pytest.python_api import raises
from hypothesis import given
from hypothesis.strategies import integers

from swagger_server.ogm.utils import with_retry


def test_retry_decorator_calls_method_at_least_once(mocker):
    exception_class = BufferError
    instance = mocker.MagicMock()
    instance.method_to_test = mocker.MagicMock(side_effect=exception_class)

    with raises(exception_class):
        with_retry(exception_class, max_retries=0)(instance.method_to_test)(instance)

    assert instance.method_to_test.call_count == 1


def test_retry_decorator(mocker):
    @given(max_retries=integers(min_value=1, max_value=3))
    def inner(max_retries):
        exception_class = BufferError
        instance = mocker.MagicMock()
        instance.method_to_test = mocker.MagicMock(side_effect=exception_class)

        with raises(exception_class):
            with_retry(exception_class, max_retries=max_retries)(instance.method_to_test)(instance)

        assert instance.method_to_test.call_count == max_retries + 1

    inner()


def test_retry_decorator_with_no_error(mocker):
    @given(max_retries=integers())
    def inner(max_retries):
        exception_class = BufferError
        instance = mocker.MagicMock()
        instance.method_to_test = mocker.MagicMock()

        with_retry(exception_class, max_retries=max_retries)(instance.method_to_test)(instance)

        assert instance.method_to_test.call_count == 1

    inner()