import unittest
from unittest.mock import patch

from ai_proof_generator import generate_ai_proof
from app import app
from proof_verifier import verify_proof


class ProofFeatureTests(unittest.TestCase):
    examples = (
        ("The square of an odd integer is odd", "direct"),
        ("1 + 2 + ... + n = n(n+1)/2", "induction"),
        ("sqrt(2) is irrational", "contradiction"),
        ("If n^2 is odd, then n is odd", "contraposition"),
    )

    def test_auto_selection_generates_supported_method_proofs(self):
        for statement, expected_method in self.examples:
            with self.subTest(method=expected_method):
                result = generate_ai_proof(statement, "auto")
                self.assertTrue(result["success"])
                self.assertEqual(result["method"], expected_method)
                self.assertTrue(result["steps"])
                self.assertTrue(result["ai_response"])

    def test_auto_selection_does_not_claim_unsupported_statements(self):
        result = generate_ai_proof("Every prime number is odd", "auto")
        self.assertFalse(result["success"])
        self.assertIn("supported proof pattern", result["error"])

    def test_generated_proofs_are_accepted_by_the_verifier(self):
        for statement, method in self.examples:
            with self.subTest(method=method):
                result = generate_ai_proof(statement, method)
                verification = verify_proof(statement, "\n".join(result["steps"]))
                self.assertTrue(verification["verified"])
                self.assertEqual(verification["status"], "verified")

    def test_incomplete_and_unsupported_proofs_are_not_verified(self):
        incomplete = verify_proof(
            "The square of an odd integer is odd",
            "Let n be odd. Hence proved.",
        )
        unsupported = verify_proof("Every prime number is odd", "Proof.")
        self.assertFalse(incomplete["verified"])
        self.assertEqual(incomplete["status"], "incomplete")
        self.assertFalse(unsupported["verified"])
        self.assertEqual(unsupported["status"], "unsupported")

    def test_generate_api_accepts_auto_method(self):
        client = app.test_client()
        with patch("app.add_history_entry", return_value={"id": "test"}):
            response = client.post(
                "/api/generate-proof",
                json={
                    "statement": "If n^2 is odd, then n is odd",
                    "method": "auto",
                },
            )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["requested_method"], "auto")
        self.assertEqual(payload["method"], "contraposition")

    def test_verify_api_reports_incomplete_proof(self):
        response = app.test_client().post(
            "/api/verify-proof",
            json={
                "statement": "The square of an odd integer is odd",
                "proof": "Let n be odd. Hence proved.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()["verified"])
        self.assertEqual(response.get_json()["status"], "incomplete")


if __name__ == "__main__":
    unittest.main()
