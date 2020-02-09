import unittest


class TestHelloWorld(unittest.TestCase):

    def test_hello_world(self):
        self.assertTrue(1 == 1, "Hello world is working.")

if __name__ == '__main__':
    unittest.main()
