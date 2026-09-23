import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build import (  # noqa: E402
    assert_tier_nesting,
    deterministic_serial,
    normalize_domain,
    parse_external_line,
    render_dnsmasq,
    render_rpz,
    render_unbound,
)
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

    def test_ip_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize_domain("127.0.0.1")


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


class ResolverFormatTests(unittest.TestCase):
    def test_dnsmasq_null_address(self):
        text = render_dnsmasq(
            "test", ["ads.example.com"], license_id="GPL-3.0-only"
        )
        self.assertIn("address=/ads.example.com/#", text)

    def test_unbound_always_null(self):
        text = render_unbound(
            "test", ["ads.example.com"], license_id="GPL-3.0-only"
        )
        self.assertIn('local-zone: "ads.example.com" always_null', text)

    def test_rpz_blocks_domain_and_subdomains(self):
        text = render_rpz(
            "test", ["ads.example.com"], license_id="GPL-3.0-only"
        )
        self.assertIn("ads.example.com CNAME .", text)
        self.assertIn("*.ads.example.com CNAME .", text)

    def test_rpz_is_deterministic(self):
        first = render_rpz(
            "test", ["ads.example.com", "tracker.example.com"],
            license_id="GPL-3.0-only",
        )
        second = render_rpz(
            "test", ["ads.example.com", "tracker.example.com"],
            license_id="GPL-3.0-only",
        )
        self.assertEqual(first, second)
        self.assertEqual(
            deterministic_serial(["ads.example.com"]),
            deterministic_serial(["ads.example.com"]),
        )


class TierTests(unittest.TestCase):
    def test_valid_nested_tiers(self):
        assert_tier_nesting(
            ["a.example.com"],
            ["a.example.com", "b.example.com"],
            ["a.example.com", "b.example.com", "c.example.com"],
            ["a.example.com", "b.example.com", "c.example.com", "d.example.com"],
        )

    def test_invalid_nested_tiers_raise(self):
        with self.assertRaises(RuntimeError):
            assert_tier_nesting(
                ["a.example.com"],
                ["b.example.com"],
                ["b.example.com"],
                ["b.example.com"],
            )


class TurkeyCandidateTests(unittest.TestCase):
    def test_tr_domains(self):
        self.assertTrue(is_turkey_domain("example.tr"))
        self.assertTrue(is_turkey_domain("ads.example.com.tr"))

    def test_non_tr_domains(self):
        self.assertFalse(is_turkey_domain("example.com"))
        self.assertFalse(is_turkey_domain("nottr.example"))


if __name__ == "__main__":
    unittest.main()
