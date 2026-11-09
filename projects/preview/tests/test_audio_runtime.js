const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

class Target {
  constructor() { this.listeners = new Map(); }
  addEventListener(type, listener, options) { const list = this.listeners.get(type) || []; list.push({ listener, options }); this.listeners.set(type, list); }
  removeEventListener(type, listener) { this.listeners.set(type, (this.listeners.get(type) || []).filter(item => item.listener !== listener)); }
  dispatch(type, event = {}) { for (const item of [...(this.listeners.get(type) || [])]) item.listener({ target: event.target || this, ...event }); }
  count(type) { return (this.listeners.get(type) || []).length; }
}
class FakeAudio extends Target {
  constructor() { super(); this.paused = true; this.ended = false; this.muted = false; this.volume = 1; this.error = null; this.plays = []; this.pauseCalls = 0; }
  play() { const attempt = deferred(); this.plays.push(attempt); return attempt.promise; }
  pause() { this.pauseCalls++; this.paused = true; this.dispatch('pause'); }
}
function deferred() {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}
function createPage() {
  const document = new Target(); document.hidden = false;
  const window = new Target(); window.PointerEvent = function PointerEvent() {};
  const audio = new FakeAudio();
  const toggle = new Target(); toggle.attributes = {}; toggle.setAttribute = function (name, value) { this.attributes[name] = value; };
  const status = { textContent: '' };
  const elements = { '#background-audio': audio, '#audio-toggle': toggle, '#audio-status': status };
  const $ = selector => elements[selector];
  const source = fs.readFileSync(path.join(__dirname, '../js/main.js'), 'utf8');
  const start = source.indexOf('  // Satu tombol mengelola Play dan mute/unmute;');
  const end = source.indexOf('\n  const visionTrigger', start);
  assert.ok(start >= 0 && end > start, 'audio controller block must remain identifiable');
  const block = source.slice(start, end);
  new Function('$', 'document', 'window', 'Element', block)($, document, window, Target);
  return { document, window, audio, toggle, status };
}
const tick = () => new Promise(resolve => setImmediate(resolve));

(async () => {
  // Every page load creates fresh in-memory flags and retries autoplay once.
  const first = createPage();
  assert.equal(first.audio.volume, 0.30);
  assert.equal(first.audio.src, 'assets/mp3/music.mp3');
  assert.equal(first.audio.plays.length, 1);
  first.audio.plays[0].reject(Object.assign(new Error('blocked'), { name: 'NotAllowedError' }));
  await tick();
  assert.equal(first.document.count('pointerdown'), 1, 'fallback is active after autoplay rejection');
  const refreshed = createPage();
  assert.equal(refreshed.audio.plays.length, 1, 'refresh starts a new autoplay attempt');
  assert.equal(refreshed.audio.volume, 0.30);
  assert.equal(refreshed.document.count('pointerdown'), 1, 'fallback is installed again on reload');

  // A lifecycle event invalidates a pending play even when audio.paused is still true.
  const pendingPage = createPage();
  pendingPage.document.hidden = true;
  pendingPage.document.dispatch('visibilitychange');
  assert.equal(pendingPage.audio.pauseCalls, 1);
  pendingPage.audio.plays[0].resolve();
  await tick();
  assert.equal(pendingPage.audio.paused, true, 'late resolution is paused again');
  assert.equal(pendingPage.status.textContent, 'Musik dihentikan saat tab tidak aktif');

  // A pending rejection after lifecycle does not replace the lifecycle decision.
  const rejectedPage = createPage();
  rejectedPage.window.dispatch('pagehide');
  rejectedPage.audio.plays[0].reject(Object.assign(new Error('aborted'), { name: 'AbortError' }));
  await tick();
  assert.equal(rejectedPage.status.textContent, 'Musik dihentikan saat halaman ditinggalkan');

  // A failed gesture can be retried; successful playback removes fallback.
  const retryPage = createPage();
  retryPage.audio.plays[0].reject(Object.assign(new Error('blocked'), { name: 'NotAllowedError' }));
  await tick();
  retryPage.document.dispatch('pointerdown', { target: { closest: () => null } });
  assert.equal(retryPage.audio.plays.length, 2);
  retryPage.audio.plays[1].resolve();
  await tick();
  assert.equal(retryPage.document.count('pointerdown'), 0);
  assert.equal(retryPage.status.textContent, 'Musik sedang diputar');

  process.stdout.write('Audio lifecycle runtime tests: PASS\n');
})().catch(error => { console.error(error); process.exitCode = 1; });
