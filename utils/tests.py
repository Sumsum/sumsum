import unittest
from .datastructures import List


class TestList(unittest.TestCase):
    def test_size(self):
        self.assertEqual(List([1, 2]).size, 2)

    def test_first(self):
        self.assertEqual(List([1, 2]).first, 1)
        self.assertEqual(List().first, None)
