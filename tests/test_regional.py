import sys
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build import protected_block_rules  # noqa: E402
from check_release import CHECKED_FILES, OPTIONAL_FILES, change_fractions, check_release  # noqa: E402
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

    def test_regional_only_wipeout_stops_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path(directory) / "previous"
            current = Path(directory) / "current"
            content = "".join(f"d{n}.example.tr\n" for n in range(100))
            for filename in CHECKED_FILES:
                for root in (previous, current):
                    path = root / filename
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
            (current / "lists/osfilter-tr-regional-domains.txt").write_text(
                "".join(f"d{n}.example.tr\n" for n in range(80)), encoding="utf-8"
            )
            with self.assertRaisesRegex(RuntimeError, "tr-regional-domains"):
                check_release(previous, current)

    def test_optional_first_publication_and_subsequent_wipeout(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path(directory) / "previous"
            current = Path(directory) / "current"
            content = "".join(f"d{n}.example.org\n" for n in range(100))
            for filename in CHECKED_FILES + OPTIONAL_FILES:
                path = current / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            for filename in CHECKED_FILES:
                path = previous / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            check_release(previous, current)
            for filename in OPTIONAL_FILES:
                path = previous / filename
                path.write_text(content, encoding="utf-8")
            (current / OPTIONAL_FILES[0]).write_text(
                "".join(f"d{n}.example.org\n" for n in range(80)), encoding="utf-8"
            )
            with self.assertRaisesRegex(RuntimeError, "osfilter-security-domains"):
                check_release(previous, current)

    def test_first_turkish_ads_import_allows_only_source_domain_additions(self):
        with tempfile.TemporaryDirectory() as directory:
            previous, current = Path(directory) / "previous", Path(directory) / "current"
            base = {f"d{n}.example.tr" for n in range(100)}
            additions = {f"ad{n}.example.com" for n in range(40)}
            for filename in CHECKED_FILES + OPTIONAL_FILES:
                for root in (previous, current):
                    path = root / filename
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("\n".join(sorted(base)) + "\n", encoding="utf-8")
            for filename in ("lists/osfilter-tr-regional-domains.txt",
                             "lists/osfilter-tr-regional-ultra-domains.txt"):
                (current / filename).write_text("\n".join(sorted(base | additions)) + "\n",
                                                encoding="utf-8")
            artifact = current / "artifacts/turk-adfilter-lite-domains.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("\n".join(sorted(additions)) + "\n", encoding="utf-8")
            (previous / "upstream-lock.json").write_text(json.dumps({"sources": {}}))
            (current / "upstream-lock.json").write_text(json.dumps({
                "sources": {"turk_adfilter_lite": {"entries": 40}}
            }))
            check_release(previous, current)
            (current / "lists/osfilter-tr-regional-domains.txt").write_text(
                "\n".join(sorted(base | additions | {
                    f"other{n}.example.com" for n in range(11)
                })) + "\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(RuntimeError, "tr-regional-domains"):
                check_release(previous, current)
            (current / "lists/osfilter-tr-regional-domains.txt").write_text(
                "\n".join(sorted(base | additions)) + "\n", encoding="utf-8"
            )
            (previous / "upstream-lock.json").write_text(json.dumps({
                "sources": {"turk_adfilter_lite": {"entries": 40}}
            }))
            with self.assertRaisesRegex(RuntimeError, "tr-regional-domains"):
                check_release(previous, current)
