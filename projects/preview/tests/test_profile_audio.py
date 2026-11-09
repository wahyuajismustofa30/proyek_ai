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

    def test_audio_uses_existing_mp3_and_attempts_autoplay_in_javascript(self):
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

    def test_single_button_starts_then_toggles_mute_without_pausing(self):
        handler_start = self.main.index("audioToggle.addEventListener('click'")
        handler_end = self.main.index("backgroundAudio.addEventListener('play'", handler_start)
        handler = self.main[handler_start:handler_end]
        self.assertEqual(self.main.count("audioToggle.addEventListener('click'"), 1)
        self.assertIn("attemptAudioPlayback('manual')", handler)
        self.assertIn("backgroundAudio.muted = !backgroundAudio.muted", handler)
        self.assertIn("updateAudioState()", handler)
        self.assertNotIn("backgroundAudio.pause()", handler)
        self.assertNotIn("audioInitialized = true", handler)
        self.assertIn("backgroundAudio.volume = 0.30", self.main)
        self.assertLess(self.main.index("backgroundAudio.volume = 0.30"), self.main.index("attemptAudioPlayback(\'autoplay\')"))

    def test_autoplay_is_attempted_once_and_rejection_activates_fallback(self):
        self.assertIn("let audioAutoplayAttempted = false", self.main)
        self.assertLess(self.main.index("activateAudioFallback();", self.main.index("// Pasang listener gesture")), self.main.index("attemptAudioPlayback('autoplay')"))
        self.assertIn("if (!audioAutoplayAttempted)", self.main)
        self.assertIn("audioAutoplayAttempted = true", self.main)
        self.assertEqual(self.main.count("attemptAudioPlayback('autoplay')"), 1)
        self.assertIn("source === 'autoplay'", self.main)
        self.assertIn("activateAudioFallback()", self.main)
        self.assertIn(".catch(error =>", self.main)

    def test_playback_errors_are_classified_by_dom_exception_name(self):
        classifier = self.main.split("function classifyAudioPlaybackError(error)", 1)[1].split(
            "function getAudioMediaErrorMessage()", 1
        )[0]
        self.assertIn("name === 'NotAllowedError'", classifier)
        self.assertIn("type: 'autoplay-blocked'", classifier)
        self.assertIn("name === 'NotSupportedError' || name === 'NotFoundError'", classifier)
        self.assertIn("type: 'source-error'", classifier)
        self.assertIn("name === 'AbortError'", classifier)
        self.assertIn("type: 'aborted'", classifier)
        self.assertIn("type: 'unknown'", classifier)

    def test_only_not_allowed_autoplay_failure_activates_fallback(self):
        attempt = self.main.split("function attemptAudioPlayback(source)", 1)[1].split(
            "function handleAudioFallbackInteraction(event)", 1
        )[0]
        self.assertIn("const failure = classifyAudioPlaybackError(error)", attempt)
        self.assertIn(
            "failure.type === 'autoplay-blocked' && ['autoplay', 'fallback', 'manual'].includes(source) && !audioInitialized && !audioUserPaused",
            attempt,
        )
        self.assertEqual(attempt.count("activateAudioFallback()"), 1)
        self.assertIn("Browser masih membatasi pemutaran musik", attempt)
        self.assertNotIn(".catch(() =>", attempt)

    def test_media_error_codes_have_distinct_user_facing_messages(self):
        media_errors = self.main.split("function getAudioMediaErrorMessage()", 1)[1].split(
            "function attemptAudioPlayback(source)", 1
        )[0]
        self.assertIn("mediaError.code === 3 || mediaError.code === 4", media_errors)
        self.assertIn("mediaError.code === 2", media_errors)
        self.assertIn("mediaError.code === 1", media_errors)
        self.assertIn("File atau format musik tidak dapat diputar", media_errors)

    def test_stale_play_attempts_cannot_overwrite_newer_audio_decisions(self):
        attempt = self.main.split("function attemptAudioPlayback(source)", 1)[1].split(
            "function handleAudioFallbackInteraction(event)", 1
        )[0]
        self.assertIn("const attemptId = ++audioPlayAttemptId", attempt)
        self.assertGreaterEqual(attempt.count("attemptId !== audioPlayAttemptId"), 2)
        self.assertIn("audioUserPaused", attempt)

    def test_pause_lifecycle_reason_survives_pause_event(self):
        pause_handler = self.main.split("backgroundAudio.addEventListener('pause'", 1)[1].split(
            "backgroundAudio.addEventListener('ended'", 1
        )[0]
        lifecycle = self.main.split("function pauseAudioForLifecycle(message)", 1)[1].split(
            "document.addEventListener('visibilitychange'", 1
        )[0]
        self.assertIn("if (!backgroundAudio.paused) return", pause_handler)
        self.assertIn("const message = audioLifecycleMessage", pause_handler)
        self.assertIn("updateAudioState(message)", pause_handler)
        self.assertNotIn("updateAudioState('Musik dijeda')", pause_handler.split("if (audioLifecyclePause)", 1)[1].split("return;", 1)[0])
        self.assertIn("audioLifecycleMessage = message", lifecycle)
        self.assertIn("audioLifecycleAttemptId = audioPlayAttemptId", lifecycle)
        self.assertIn("audioPlayAttemptId === audioLifecycleAttemptId", pause_handler)
        self.assertLess(lifecycle.index("audioLifecycleMessage = message"), lifecycle.index("backgroundAudio.pause()"))

    def test_pause_event_only_marks_manual_pause_outside_lifecycle(self):
        pause_handler = self.main.split("backgroundAudio.addEventListener('pause'", 1)[1].split(
            "backgroundAudio.addEventListener('ended'", 1
        )[0]
        self.assertIn("if (audioLifecyclePause)", pause_handler)
        self.assertIn("audioUserPaused = true", pause_handler)
        self.assertIn("++audioPlayAttemptId", pause_handler)
        self.assertIn("updateAudioState('Musik dijeda')", pause_handler)

    def test_fallback_is_one_shot_and_preserves_single_music_control(self):
        self.assertIn("let audioFallbackActive = false", self.main)
        self.assertIn("audioFallbackActive = true", self.main)
        self.assertIn("failure.type === 'autoplay-blocked' && ['autoplay', 'fallback', 'manual'].includes(source)", self.main)
        self.assertIn("removeAudioFallback()", self.main)
        self.assertIn("document.removeEventListener(type, listener, options)", self.main)
        self.assertIn("['pointerdown', 'touchstart']", self.main)
        self.assertIn("['touchstart', 'click']", self.main)
        self.assertIn('#audio-toggle, [contenteditable="true"]', self.main)
        self.assertIn("attemptAudioPlayback('fallback')", self.main)
        handler = self.main.split("function handleAudioFallbackInteraction(event)", 1)[1].split(
            "function activateAudioFallback()", 1
        )[0]
        self.assertNotIn("audioInitialized = true", handler)
        self.assertIn("removeAudioFallback()", handler)

    def test_manual_pause_is_distinct_from_lifecycle_pause(self):
        self.assertIn("let audioUserPaused = false", self.main)
        self.assertIn("let audioLifecyclePause = false", self.main)
        self.assertIn("if (audioLifecyclePause)", self.main)
        self.assertIn("audioUserPaused = true", self.main)
        self.assertIn("|| audioUserPaused", self.main)
        self.assertIn("function pauseAudioForLifecycle(message)", self.main)
        self.assertIn("++audioPlayAttemptId", self.main)

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

    def test_audio_stops_when_tab_is_hidden_or_page_is_left_without_resume(self):
        self.assertIn("visibilitychange", self.main)
        self.assertIn("document.hidden", self.main)
        self.assertIn("pauseAudioForLifecycle('Musik dihentikan saat tab tidak aktif')", self.main)
        self.assertIn("addEventListener('pagehide'", self.main)
        self.assertNotIn("document.addEventListener('visibilitychange', () => attemptAudioPlayback", self.main)
        self.assertNotIn("window.addEventListener('focus', () => attemptAudioPlayback", self.main)

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
