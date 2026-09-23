import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build import normalize_domain  # noqa: E402


class NormalizeDomainTests(unittest.TestCase):
    def test_lowercase_and_trailing_dot(self):
        self.assertEqual(normalize_domain("Ads.Example.COM."), "ads.example.com")

    def test_idn_becomes_ascii(self):
        self.assertTrue(normalize_domain("örnek.com").startswith("xn--"))

    def test_url_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize_domain("https://example.com/path")

    def test_single_label_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize_domain("localhost")


if __name__ == "__main__":
    unittest.main()
