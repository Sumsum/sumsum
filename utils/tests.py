import unittest
from .datastructures import List, NSDict


class TestList(unittest.TestCase):
    def test_size(self):
        self.assertEqual(List([1, 2]).size, 2)

    def test_first(self):
        self.assertEqual(List([1, 2]).first, 1)
        self.assertEqual(List().first, None)


class TestNSDict(unittest.TestCase):
    def test_basic(self):
        d = NSDict({'a': 1, 'b': 2})
        self.assertEqual(d['a'], 1)
        self.assertEqual(sorted(d.keys()), ['a', 'b'])

    def test_ns(self):
        d = NSDict({
            'ns1.a': 1,
            'ns1.b': 2,
            'ns2.a': 10,
            'ns2.b': 20,
        })
        self.assertEqual(d.ns1, {'a': 1, 'b': 2})
        self.assertEqual(d.ns2, {'a': 10, 'b': 20})
        self.assertEqual(d, {
            'ns1.a': 1,
            'ns1.b': 2,
            'ns2.a': 10,
            'ns2.b': 20,
        })
