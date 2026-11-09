"""Contract tests for Preview profile data and optional background audio."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ProfileAndAudioContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = (ROOT / "js/data.js").read_text(encoding="utf-8")
        cls.main = (ROOT / "js/main.js").read_text(encoding="utf-8")
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "css/improvements.css").read_text(encoding="utf-8")

    def test_education_contains_three_supplied_schools(self):
        block = self.data.split("education: [", 1)[1].split("],", 1)[0]
        for school in ("SD Negeri 1 Tlagayasa", "SMP Negeri 1 Karangreja", "SMK Ma'arif NU Bobotsari"):
            self.assertIn(school, block)
        self.assertEqual(block.count("',"), 2)

    def test_work_history_and_owner_roles_are_exact(self):
        block = self.data.split("workExperience: [", 1)[1].split("\n    ]", 1)[0]
        for period, company in (("2010–2016", "CV Kompo Motor"), ("2016–2020", "PT Yamaha Mataram Sakti"), ("2020–2024", "Bengkel Asta Jaya Motor"), ("2024–Sekarang", "Bi One Net")):
            self.assertIn(period, block)
            self.assertIn(company, block)
        self.assertEqual(block.count("role: 'Owner'"), 2)
        self.assertIn("Penyedia Layanan Internet Desa", block)

    def test_audio_has_no_autoplay_or_source_until_licensed_asset_exists(self):
        audio_tag = self.html.split("<audio", 1)[1].split(">", 1)[0]
        self.assertNotIn("autoplay", audio_tag.lower())
        self.assertNotIn("src=", audio_tag.lower())
        self.assertIn("const BACKGROUND_AUDIO_SOURCE = '';", self.main)

    def test_audio_controls_and_failure_handling_exist(self):
        for element_id in ("audio-toggle", "audio-mute", "audio-volume", "audio-status"):
            self.assertIn('id="' + element_id + '"', self.html)
        self.assertIn("backgroundAudio.play()", self.main)
        self.assertIn("backgroundAudio.pause()", self.main)
        self.assertIn("addEventListener('error'", self.main)
        self.assertIn("visibilitychange", self.main)
        self.assertIn('role="status"', self.html)
        self.assertIn("prefers-reduced-motion:reduce", self.css)

    def test_profile_renderer_uses_structured_history(self):
        self.assertIn("profile.education.map", self.main)
        self.assertIn("profile.workExperience.map", self.main)
        self.assertIn("Riwayat Pendidikan", self.main)
        self.assertIn("Riwayat Pekerjaan", self.main)

if __name__ == "__main__":
    unittest.main(verbosity=2)
