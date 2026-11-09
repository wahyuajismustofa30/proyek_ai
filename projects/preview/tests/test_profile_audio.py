"""Contract tests for Preview profile data and the single background-audio control."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PageControlsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.audio = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "button":
            self.buttons.append(attributes)
        if tag == "audio":
            self.audio.append(attributes)


class ProfileAndAudioContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = (ROOT / "js/data.js").read_text(encoding="utf-8")
        cls.main = (ROOT / "js/main.js").read_text(encoding="utf-8")
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "css/improvements.css").read_text(encoding="utf-8")
        cls.style = (ROOT / "css/style.css").read_text(encoding="utf-8")
        cls.parser = PageControlsParser()
        cls.parser.feed(cls.html)

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

    def test_audio_uses_existing_mp3_without_autoplay(self):
        self.assertEqual(len(self.parser.audio), 1)
        self.assertNotIn("autoplay", self.parser.audio[0])
        self.assertIn("preload", self.parser.audio[0])
        self.assertIn("const BACKGROUND_AUDIO_SOURCE = 'assets/mp3/music.mp3';", self.main)
        self.assertTrue((ROOT / "assets/mp3/music.mp3").is_file())

    def test_exactly_one_floating_music_button_and_no_extra_controls(self):
        audio_buttons = [button for button in self.parser.buttons if button.get("id") == "audio-toggle"]
        self.assertEqual(len(audio_buttons), 1)
        self.assertIn("audio-toggle", audio_buttons[0].get("class", "").split())
        self.assertEqual(sum("audio-toggle" in button.get("class", "").split() for button in self.parser.buttons), 1)
        self.assertNotIn('id="audio-mute"', self.html)
        self.assertNotIn('id="audio-volume"', self.html)
        self.assertNotIn('type="range"', self.html)
        self.assertNotIn("audio-player", self.html)
        self.assertNotIn("audio-mute", self.main)
        self.assertNotIn("audio-volume", self.main)
        self.assertNotIn("audio-player", self.css)

    def test_single_handler_starts_then_toggles_mute_without_pausing(self):
        handler_start = self.main.index("audioToggle.addEventListener('click'")
        handler_end = self.main.index("backgroundAudio.addEventListener('play'", handler_start)
        handler = self.main[handler_start:handler_end]
        self.assertEqual(self.main.count("audioToggle.addEventListener('click'"), 1)
        self.assertIn("await backgroundAudio.play()", handler)
        self.assertIn("backgroundAudio.muted = !backgroundAudio.muted", handler)
        self.assertIn("updateAudioState()", handler)
        self.assertNotIn("backgroundAudio.pause()", handler)
        self.assertIn("backgroundAudio.volume = 0.18", self.main)

    def test_audio_button_state_and_failure_are_accessible(self):
        self.assertIn("aria-label", self.html)
        self.assertIn("title=", self.html)
        self.assertIn('id="audio-status"', self.html)
        self.assertIn('role="status"', self.html)
        self.assertIn("aria-live=\"polite\"", self.html)
        self.assertIn("audioToggle.setAttribute('aria-label', label)", self.main)
        self.assertIn("audioToggle.setAttribute('title', label)", self.main)
        self.assertIn("audioToggle.setAttribute('aria-pressed', String(playing && muted))", self.main)
        self.assertIn("audioIcons.play", self.main)
        self.assertIn("audioIcons.playing", self.main)
        self.assertIn("audioIcons.muted", self.main)
        self.assertIn("Musik gagal diputar", self.main)
        self.assertIn("addEventListener('error'", self.main)

    def test_audio_stops_when_tab_is_hidden_or_page_is_left(self):
        self.assertIn("visibilitychange", self.main)
        self.assertIn("document.hidden", self.main)
        self.assertIn("backgroundAudio.pause()", self.main)
        self.assertIn("addEventListener('pagehide'", self.main)

    def test_back_to_top_is_removed_but_scroll_features_remain(self):
        self.assertNotIn("back-to-top", self.html.lower())
        self.assertNotIn("back-to-top", self.main.lower())
        self.assertNotIn("topButton", self.main)
        self.assertNotIn("scrollTo({ top: 0", self.main)
        self.assertNotIn(".back-to-top", self.style)
        self.assertIn("scroll-progress", self.html)
        self.assertIn("progress.style.width", self.main)
        self.assertIn("header.classList.toggle('sticky'", self.main)

    def test_profile_renderer_uses_structured_history(self):
        self.assertIn("profile.education.map", self.main)
        self.assertIn("profile.workExperience.map", self.main)
        self.assertIn("Riwayat Pendidikan", self.main)
        self.assertIn("Riwayat Pekerjaan", self.main)


if __name__ == "__main__":
    unittest.main(verbosity=2)
