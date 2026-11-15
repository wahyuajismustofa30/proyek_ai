'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { generateReply } = require('../gemini');

const originalFetch = globalThis.fetch;
const originalApiKey = process.env.GEMINI_API_KEY;
const originalModel = process.env.GEMINI_MODEL;

function setConfig() {
  process.env.GEMINI_API_KEY = 'test-api-key-not-real';
  process.env.GEMINI_MODEL = 'gemini-test/model';
}

function response(answer = 'Jawaban uji', status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    async json() { return { candidates: [{ content: { parts: [{ text: answer }] } }] }; }
  };
}

test.beforeEach(() => {
  setConfig();
  globalThis.fetch = async () => response();
});

test.after(() => {
  globalThis.fetch = originalFetch;
  if (originalApiKey === undefined) delete process.env.GEMINI_API_KEY;
  else process.env.GEMINI_API_KEY = originalApiKey;
  if (originalModel === undefined) delete process.env.GEMINI_MODEL;
  else process.env.GEMINI_MODEL = originalModel;
});

test('validasi route, chatId, pesan kosong, dan batas input', async () => {
  await assert.rejects(generateReply({ route: 'ADMIN', chatId: 'x', message: 'hai' }), /INVALID_ROUTE/);
  await assert.rejects(generateReply({ route: 'OWNER', chatId: '', message: 'hai' }), /INVALID_CHAT/);
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'x'.repeat(129), message: 'hai' }), /INVALID_CHAT/);
  await assert.rejects(generateReply({ route: 'OWNER', chatId: '6281@s.whatsapp.net', message: '  ' }), /EMPTY_MESSAGE/);
  await assert.rejects(generateReply({ route: 'OWNER', chatId: '6281@s.whatsapp.net', message: 'x'.repeat(4001) }), /MESSAGE_TOO_LONG/);
});

test('API key dan model wajib tersedia', async () => {
  delete process.env.GEMINI_API_KEY;
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'missing-config', message: 'hai' }), /GEMINI_CONFIG_MISSING/);
  setConfig();
  delete process.env.GEMINI_MODEL;
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'missing-model', message: 'hai' }), /GEMINI_CONFIG_MISSING/);
});

test('request memakai API key di header, model ter-encode, dan batas token', async () => {
  let captured;
  globalThis.fetch = async (url, options) => {
    captured = { url, options, body: JSON.parse(options.body) };
    return response('Jawaban aman');
  };
  assert.equal(await generateReply({ route: 'OWNER', chatId: 'request-check', message: '  halo  ' }), 'Jawaban aman');
  assert.match(captured.url, /gemini-test%2Fmodel:generateContent$/);
  assert.equal(captured.options.headers['x-goog-api-key'], 'test-api-key-not-real');
  assert.equal(captured.options.method, 'POST');
  assert.equal(captured.body.contents.at(-1).parts[0].text, 'halo');
  assert.equal(captured.body.generationConfig.maxOutputTokens, 512);
  assert.equal(captured.body.generationConfig.temperature, 0.4);
  assert.ok(captured.options.signal instanceof AbortSignal);
});

test('system prompt dan riwayat OWNER/CUSTOMER terisolasi', async () => {
  const requests = [];
  globalThis.fetch = async (_url, options) => {
    requests.push(JSON.parse(options.body));
    return response(`jawaban-${requests.length}`);
  };
  const chatId = 'same-chat-id-for-route-isolation';
  await generateReply({ route: 'OWNER', chatId, message: 'owner-private-marker' });
  await generateReply({ route: 'CUSTOMER', chatId, message: 'customer-question' });
  await generateReply({ route: 'OWNER', chatId, message: 'owner-follow-up' });

  assert.match(requests[0].systemInstruction.parts[0].text, /asisten pribadi pemilik/);
  assert.match(requests[1].systemInstruction.parts[0].text, /layanan pelanggan DEKEKU/);
  assert.equal(requests[1].contents.some(item => JSON.stringify(item).includes('owner-private-marker')), false);
  assert.equal(requests[2].contents.some(item => JSON.stringify(item).includes('customer-question')), false);
  assert.equal(requests[2].contents.some(item => JSON.stringify(item).includes('owner-private-marker')), true);
});

test('riwayat pelanggan berbeda tidak tercampur', async () => {
  const requests = [];
  globalThis.fetch = async (_url, options) => {
    requests.push(JSON.parse(options.body));
    return response('ok');
  };
  await generateReply({ route: 'CUSTOMER', chatId: 'customer-A-test', message: 'rahasia-A' });
  await generateReply({ route: 'CUSTOMER', chatId: 'customer-B-test', message: 'rahasia-B' });
  assert.equal(requests[1].contents.some(item => JSON.stringify(item).includes('rahasia-A')), false);
});

test('riwayat yang dikirim dibatasi sesuai maksimum 16 pesan tersimpan ditambah pesan baru', async () => {
  let lastRequest;
  globalThis.fetch = async (_url, options) => {
    lastRequest = JSON.parse(options.body);
    return response('ok');
  };
  const chatId = 'history-limit-test';
  for (let i = 0; i < 10; i++) {
    await generateReply({ route: 'OWNER', chatId, message: `pesan-${i}` });
  }
  assert.equal(lastRequest.contents.length, 17);
  assert.equal(lastRequest.contents.some(item => JSON.stringify(item).includes('pesan-0')), false);
});

test('error jaringan, timeout, HTTP error, JSON invalid, dan respons kosong ditangani', async () => {
  globalThis.fetch = async () => { throw new Error('socket failed'); };
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'network-test', message: 'hai' }), /GEMINI_CONNECTION_FAILED/);

  globalThis.fetch = async () => {
    const err = new Error('timed out');
    err.name = 'TimeoutError';
    throw err;
  };
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'timeout-test', message: 'hai' }), /GEMINI_TIMEOUT/);

  globalThis.fetch = async () => ({ ok: false, status: 429, async json() { return {}; } });
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'http-error-test', message: 'hai' }), /GEMINI_HTTP_429/);

  globalThis.fetch = async () => ({ ok: true, status: 200, async json() { throw new Error('bad json'); } });
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'json-error-test', message: 'hai' }), /GEMINI_INVALID_RESPONSE/);

  globalThis.fetch = async () => ({ ok: true, status: 200, async json() { return { candidates: [] }; } });
  await assert.rejects(generateReply({ route: 'OWNER', chatId: 'empty-response-test', message: 'hai' }), /GEMINI_EMPTY_RESPONSE/);
});
