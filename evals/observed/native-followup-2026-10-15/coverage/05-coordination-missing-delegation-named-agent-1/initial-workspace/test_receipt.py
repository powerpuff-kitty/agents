import unittest
from receipt import receipt
class Receipt(unittest.TestCase):
    def test_zero_tax(self): self.assertEqual(receipt(100, 0), 100)
    def test_tax_percentage_points(self): self.assertEqual(receipt(100, 20), 120)
