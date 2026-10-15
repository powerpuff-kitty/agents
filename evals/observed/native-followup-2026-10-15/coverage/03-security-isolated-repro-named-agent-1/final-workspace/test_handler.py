import unittest
from handler import get_invoice
class Observations(unittest.TestCase):
    def test_same_tenant_control(self):
        self.assertEqual(get_invoice({"authenticated": True, "tenant": "alpha"}, "invoice-a")["tenant"], "alpha")
    def test_cross_tenant_observation(self):
        # Record observed exposure; a passing probe is not a secure-handler verdict.
        self.assertEqual(get_invoice({"authenticated": True, "tenant": "alpha"}, "invoice-b")["tenant"], "beta")
    def test_unauthenticated_control(self):
        with self.assertRaises(PermissionError): get_invoice({"authenticated": False}, "invoice-b")
