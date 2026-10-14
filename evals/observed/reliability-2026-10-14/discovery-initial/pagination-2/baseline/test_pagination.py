import unittest
from pagination import pages
class Pages(unittest.TestCase):
    def test_empty(self): self.assertEqual(pages([], 2), [])
    def test_exact_first(self): self.assertEqual(pages([1, 2], 2), [[1, 2]])
    def test_exact_last(self): self.assertEqual(pages([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
    def test_partial_last(self): self.assertEqual(pages([1, 2, 3], 2), [[1, 2], [3]])
    def test_invalid_size(self):
        with self.assertRaises(ValueError): pages([1], 0)
