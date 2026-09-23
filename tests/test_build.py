import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build import (  # noqa: E402
    assert_tier_nesting,
    deterministic_serial,
    normalize_domain,
    parse_abp_dns_line,
    parse_external_line,
    parse_plain_domain_line,
    previous_rpz_serial,
    render_dnsmasq,
    render_rpz,
    render_unbound,
)
from discover_tr_candidates import independent_projects, is_turkey_domain, local_domains  # noqa: E402


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

    def test_turkish_registration_zone_apex_is_rejected(self):
        for zone in ("com.tr", "gov.tr", "edu.tr"):
            with self.subTest(zone=zone), self.assertRaises(ValueError):
                normalize_domain(zone)
        self.assertEqual(normalize_domain("ads.example.com.tr"), "ads.example.com.tr")


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

    def test_registered_plain_domain_upstream_rejects_other_syntax(self):
        self.assertEqual(parse_plain_domain_line("Ads.Example.COM"), "ads.example.com")
        for line in ("0.0.0.0 ads.example.com", "||ads.example.com^",
                     "ads.example.com # inline", "! comment", "com.tr"):
            with self.subTest(line=line):
                self.assertIsNone(parse_plain_domain_line(line))

    def test_category_abp_extractor_accepts_only_exact_hostnames(self):
        self.assertEqual(parse_abp_dns_line("||BET.Example.COM^"), "bet.example.com")
        for line in ("@@||bet.example.com^", "||bet*.example.com^",
                     "||bet.example.com^$third-party", "||bet.example.com/path",
                     "||bet.example.com^$badfilter", "bet.example.com##.ad"):
            with self.subTest(line=line):
                self.assertIsNone(parse_abp_dns_line(line))


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

    def test_rpz_serial_reuses_unchanged_and_increments_changed(self):
        with tempfile.TemporaryDirectory() as directory:
            domain_file = Path(directory) / "domains.txt"
            zone_file = Path(directory) / "rpz.zone"
            domain_file.write_text("# previous\nads.example.com\n", encoding="utf-8")
            zone_file.write_text(render_rpz("test", ["ads.example.com"],
                                           license_id="GPL-3.0-only", serial=17),
                                 encoding="utf-8")
            self.assertEqual(previous_rpz_serial(["ads.example.com"], domain_file,
                                                 zone_file), 17)
            self.assertEqual(previous_rpz_serial(["other.example.com"], domain_file,
                                                 zone_file), 18)
            zone_file.write_text(render_rpz("test", ["ads.example.com"],
                                           license_id="GPL-3.0-only", serial=0xFFFFFFFF),
                                 encoding="utf-8")
            self.assertEqual(previous_rpz_serial(["other.example.com"], domain_file,
                                                 zone_file), 0)
            zone_file.write_text("invalid", encoding="utf-8")
            with self.assertRaises(ValueError):
                previous_rpz_serial(["ads.example.com"], domain_file, zone_file)


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

    def test_upstream_tiers_from_same_project_count_once(self):
        projects = {"light": "https://example.org/project", "normal": "https://example.org/project",
                    "other": "https://other.org"}
        self.assertEqual(independent_projects(set(projects), projects), 2)

    def test_functional_service_is_not_an_auto_promotion_candidate(self):
        self.assertIn("tdms.saglik.gov.tr", local_domains())


if __name__ == "__main__":
    unittest.main()
