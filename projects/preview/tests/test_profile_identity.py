import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = (ROOT / "js/data.js").read_text(encoding="utf-8")
MAIN = (ROOT / "js/main.js").read_text(encoding="utf-8")
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "css/improvements.css").read_text(encoding="utf-8")


class CandidateIdentityTests(unittest.TestCase):
    def test_full_name_is_defined_in_candidate_data(self):
        self.assertIn("fullName: 'Slamet Purwanto'", DATA)
        self.assertEqual(DATA.count("fullName: 'Slamet Purwanto'"), 1)

    def test_campaign_brand_remains_slamet(self):
        self.assertIn("name: 'SLAMET'", DATA)
        self.assertIn("Sing Penting SLAMET", HTML)
        self.assertIn('<h1 id="hero-title">SLA<span>MET</span></h1>', HTML)

    def test_profile_renderer_uses_candidate_full_name(self):
        self.assertIn("campaignData.candidate.fullName || profile.name", MAIN)
        self.assertIn("textContent = fullName", MAIN)
        self.assertIn("fullName}</span>", MAIN)

    def test_full_name_is_present_in_public_identity_and_metadata(self):
        self.assertIn("Slamet Purwanto", HTML)
        self.assertIn('name="author" content="Slamet Purwanto (SLAMET)"', HTML)
        self.assertIn('class="candidate-full-name">Slamet Purwanto</p>', HTML)

    def test_full_name_hero_style_exists(self):
        self.assertIn(".candidate-full-name", CSS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
