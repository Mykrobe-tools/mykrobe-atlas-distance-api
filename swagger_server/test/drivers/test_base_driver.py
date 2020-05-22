from concurrent.futures.thread import ThreadPoolExecutor
from unittest import TestCase

from swagger_server.drivers import BaseDriver


class DerivedDriver(BaseDriver):
    @classmethod
    def _make_instance(cls):
        return DerivedDriver()


class BaseDriverTestCase(TestCase):
    def test_driver_implement_singleton_pattern(self):
        self.assertIs(DerivedDriver.get(), DerivedDriver.get())

    def test_singleton_instance_across_threads(self):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: DerivedDriver.get())
        self.assertIs(DerivedDriver.get(), future.result())
