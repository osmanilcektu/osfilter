import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build import protected_block_rules  # noqa: E402
from check_release import change_fractions  # noqa: E402
from regional import is_sensitive_domain, regional_profile  # noqa: E402


class RegionalProfilesTests(unittest.TestCase):
    def test_only_tr_upstream_domains_and_curated_core_are_emitted(self):
        result = regional_profile(
            ["ads.example.tr", "tracker.example.com", "api.bank.tr",
             "metrics.gov.tr", "login.shop.com.tr"],
            ["adserver.example.com", "ads.example.tr"],
            ["reklam.publisher.com", "login.publisher.com"],
        )
        self.assertEqual(result, ["ads.example.tr", "adserver.example.com",
                                  "reklam.publisher.com"])

    def test_safety_exclusions_are_at_dns_label_boundaries(self):
        self.assertTrue(is_sensitive_domain("metrics.gov.tr"))
        self.assertTrue(is_sensitive_domain("api.shop.com.tr"))
        self.assertFalse(is_sensitive_domain("adserver.bankers.com.tr"))

    def test_cumulative_upstreams_make_cumulative_regional_profiles(self):
        core = ["adserver.example.com"]
        standard = regional_profile(["ads.example.tr"], core)
        ultra = regional_profile(["ads.example.tr", "pixel.other.tr"], core)
        self.assertTrue(set(standard).issubset(ultra))


class ProtectedServiceTests(unittest.TestCase):
    def test_parent_block_rule_is_removed_for_protected_host(self):
        protected = protected_block_rules({"accounts.google.com", "api.openai.com"})
        self.assertTrue({"accounts.google.com", "google.com", "api.openai.com",
                         "openai.com"}.issubset(protected))
        self.assertNotIn("com", protected)
        self.assertNotIn("ads.google.com", protected)


class ReleaseGuardTests(unittest.TestCase):
    def test_normal_change_passes_and_large_change_is_detectable(self):
        old = {f"d{number}.example.com" for number in range(100)}
        small = (old - {"d0.example.com"}) | {"new.example.com"}
        large = old - {f"d{number}.example.com" for number in range(20)}
        self.assertEqual(change_fractions(old, small), (0.01, 0.01))
        self.assertEqual(change_fractions(old, large), (0.0, 0.2))

    def test_empty_previous_release_fails_closed(self):
        with self.assertRaises(ValueError):
            change_fractions(set(), {"a.example.com"})
