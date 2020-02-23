import unittest
from unittest import mock


class TestObject:

    def getHello(self):
        return 'Hello'


class TestHelloWorld(unittest.TestCase):

    def test_hello_world(self):
        self.assertTrue(1 == 1, "Hello world is working.")

    def test_hello_world_mock(self):
        with mock.patch.object(TestObject, 'getHello', return_value='mocked'):
            t = TestObject()
            self.assertEqual(t.getHello(), 'mocked')


if __name__ == '__main__':
    unittest.main()

