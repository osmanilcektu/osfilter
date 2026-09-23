import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build import normalize_domain, parse_external_line  # noqa: E402
from discover_tr_candidates import is_turkey_domain  # noqa: E402


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


class ExternalParserTests(unittest.TestCase):
    def test_hosts_line(self):
        self.assertEqual(
            parse_external_line("0.0.0.0 ads.example.com"),
            "ads.example.com",
        )

    def test_abp_domain_rule(self):
        self.assertEqual(
            parse_external_line("||tracker.example.com^"),
            "tracker.example.com",
        )

    def test_plain_domain(self):
        self.assertEqual(
            parse_external_line("pixel.example.com"),
            "pixel.example.com",
        )

    def test_comments_and_localhost_are_ignored(self):
        self.assertIsNone(parse_external_line("# comment"))
        self.assertIsNone(parse_external_line("0.0.0.0 localhost"))


class TurkeyCandidateTests(unittest.TestCase):
    def test_tr_domains(self):
        self.assertTrue(is_turkey_domain("example.tr"))
        self.assertTrue(is_turkey_domain("ads.example.com.tr"))

    def test_non_tr_domains(self):
        self.assertFalse(is_turkey_domain("example.com"))
        self.assertFalse(is_turkey_domain("nottr.example"))


if __name__ == "__main__":
    unittest.main()
