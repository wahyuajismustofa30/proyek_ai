'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { createBridgeServer, readConfig, verifySignature } = require('../index');
const { SECRET, OWNER_JID, DEVICE_ID, sign, payload, deferred } = require('./helpers');

function quietLogger() {
  return { log() {}, error() {} };
}

async function withServer(t, options = {}) {
  const calls = [];
  const server = createBridgeServer({
    secret: SECRET,
    ownerJid: OWNER_JID,
    deviceId: DEVICE_ID,
    generateReply: async input => { calls.push(input); return 'Balasan uji'; },
    logger: quietLogger(),
    ...options
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  t.after(() => new Promise(resolve => server.close(resolve)));

  const baseUrl = \`http://127.0.0.1:\${server.address().port}\`;
  async function request({ method = 'POST', path = '/webhook', body = '', signature, headers = {} } = {}) {
    const raw = Buffer.isBuffer(body) ? body : Buffer.from(body);
    const response = await fetch(\`\${baseUrl}\${path}\`, {
      method,
      headers: {
        ...(method === 'POST' ? { 'content-type': 'application/json' } : {}),
        ...(signature ? { 'x-hub-signature-256': signature } : {}),
        ...headers
      },
      body: method === 'GET' || method === 'HEAD' ? undefined : raw
    });
    const text = await response.text();
    let data;
    try { data = JSON.parse(text); } catch { data = text; }
    return { status: response.status, data, text };
  }
  async function post(data, opts = {}) {
    const body = typeof data === 'string' ? data : JSON.stringify(data);
    return request({ body, signature: sign(body), ...opts });
  }
  return { request, post, calls };
}

test('konfigurasi bridge memvalidasi host, port, secret, OWNER_JID, dan GOWA_DEVICE_ID', () => {
  const valid = readConfig({
    BRIDGE_HOST: '127.0.0.1', BRIDGE_PORT: '3001',
    WEBHOOK_SECRET: SECRET, OWNER_JID, GOWA_DEVICE_ID: DEVICE_ID
  });
  assert.equal(valid.port, 3001);
  assert.equal(valid.ownerJid, OWNER_JID);
  assert.equal(valid.deviceId, DEVICE_ID);
  assert.throws(() => readConfig({ BRIDGE_HOST: '0.0.0.0' }), /BRIDGE_HOST/);
  assert.throws(() => readConfig({ BRIDGE_PORT: '0' }), /BRIDGE_PORT/);
  assert.throws(() => readConfig({ WEBHOOK_SECRET: 'short' }), /WEBHOOK_SECRET/);
  assert.throws(() => readConfig({
    WEBHOOK_SECRET: SECRET, OWNER_JID: 'bukan-jid', GOWA_DEVICE_ID: DEVICE_ID
  }), /OWNER_JID/);
  assert.throws(() => readConfig({ WEBHOOK_SECRET: SECRET, OWNER_JID }), /GOWA_DEVICE_ID/);
});

test('HMAC valid diterima; signature salah, malformed, dan tidak ada ditolak', () => {
  const body = Buffer.from('{"event":"message"}');
  assert.equal(verifySignature(body, sign(body), SECRET), true);
  assert.equal(verifySignature(body, sign(body), 'b'.repeat(64)), false);
  assert.equal(verifySignature(body, 'sha256=xyz', SECRET), false);
  assert.equal(verifySignature(body, undefined, SECRET), false);
  assert.equal(verifySignature(body, sign(Buffer.from('lain')), SECRET), false);
});

test('health check, route tidak dikenal, signature, dan JSON invalid', async t => {
  const app = await withServer(t);
  assert.deepEqual((await app.request({ method: 'GET', path: '/health' })).data,
    { ok: true, mode: 'dry-run' });
  assert.equal((await app.request({ method: 'GET', path: '/unknown' })).status, 404);
  assert.equal((await app.request({ method: 'PUT', path: '/webhook' })).status, 404);

  const body = JSON.stringify(payload());
  assert.equal((await app.request({ body })).status, 401);
  assert.equal((await app.request({ body, signature: \`sha256=\${'0'.repeat(64)}\` })).status, 401);
  const invalidJson = '{not-json';
  const badJson = await app.request({ body: invalidJson, signature: sign(invalidJson) });
  assert.equal(badJson.status, 400);
  assert.equal(badJson.data.error, 'invalid_json');
  assert.equal(app.calls.length, 0);
});

test('payload null/array, device/event tidak cocok, dan payload message invalid tidak diproses', async t => {
  const app = await withServer(t);
  assert.equal((await app.post(null)).status, 200);
  assert.equal((await app.post(null)).data.result, 'invalid_payload');
  assert.equal((await app.post([])).data.result, 'invalid_payload');
  assert.equal((await app.post({ ...payload(), device_id: 'wrong-device' })).data.result, 'ignored_device');
  assert.equal((await app.post({ ...payload(), event: 'presence' })).data.result, 'ignored_event');
  assert.equal((await app.post({ device_id: OWNER_JID, event: 'message', payload: null })).data.result, 'invalid_message');
  assert.equal(app.calls.length, 0);
});

test('pesan outgoing non-self, grup, kosong, dan tanpa ID diabaikan', async t => {
  const app = await withServer(t);
  assert.equal((await app.post(payload({ chat_id: '123@g.us', is_from_me: true }))).data.result, 'ignored_outgoing');
  assert.equal((await app.post(payload({ chat_id: '123@g.us', is_from_me: false }))).data.result, 'ignored_non_private');
  assert.equal((await app.post(payload({ body: '   ', id: 'empty' }))).data.result, 'ignored_empty_message');
  assert.equal((await app.post(payload({ id: '' }))).data.result, 'ignored_missing_id');
  assert.equal(app.calls.length, 0);
});

test('routing CUSTOMER dan OWNER self-chat terpisah', async t => {
  const app = await withServer(t);
  const customer = await app.post(payload({ id: 'customer-1', body: 'Tanya website' }));
  assert.equal(customer.data.result, 'accepted_dry_run');
  const owner = await app.post(payload({
    id: 'owner-1', chat_id: OWNER_JID, from: OWNER_JID,
    is_from_me: true, body: 'Catat tugas'
  }));
  assert.equal(owner.data.result, 'accepted_dry_run');
  assert.deepEqual(app.calls.map(call => call.route), ['CUSTOMER', 'OWNER']);
  assert.equal(app.calls[0].chatId, '6281111111111@s.whatsapp.net');
  assert.equal(app.calls[1].chatId, OWNER_JID);
});

test('deduplikasi mencegah pesan sukses diproses ulang', async t => {
  const app = await withServer(t);
  assert.equal((await app.post(payload({ id: 'same-id' }))).data.result, 'accepted_dry_run');
  assert.equal((await app.post(payload({ id: 'same-id' }))).data.result, 'duplicate');
  assert.equal(app.calls.length, 1);
});

test('pesan dengan ID sama yang masih diproses tidak menggandakan panggilan Gemini', async t => {
  const gate = deferred();
  const app = await withServer(t, {
    generateReply: async input => {
      app.calls.push(input);
      await gate.promise;
      return 'selesai';
    }
  });
  const first = app.post(payload({ id: 'in-flight' }));
  while (app.calls.length === 0) await new Promise(resolve => setImmediate(resolve));
  assert.equal((await app.post(payload({ id: 'in-flight' }))).data.result, 'duplicate');
  gate.resolve();
  assert.equal((await first).data.result, 'accepted_dry_run');
  assert.equal(app.calls.length, 1);
});

test('Gemini gagal menghasilkan 503 dan ID dapat dicoba ulang', async t => {
  let fail = true;
  const app = await withServer(t, {
    generateReply: async input => {
      app.calls.push(input);
      if (fail) throw new Error('provider_unavailable');
      return 'pulih';
    }
  });
  const first = await app.post(payload({ id: 'retry-id' }));
  assert.equal(first.status, 503);
  assert.equal(first.data.result, 'gemini_failed_dry_run');
  fail = false;
  assert.equal((await app.post(payload({ id: 'retry-id' }))).data.result, 'accepted_dry_run');
  assert.equal(app.calls.length, 2);
});

test('body melebihi batas mendapat HTTP 413', async t => {
  const app = await withServer(t, { maxBody: 128 });
  const body = 'x'.repeat(1024);
  const result = await app.request({ body, signature: sign(body) });
  assert.equal(result.status, 413);
  assert.equal(result.data.error, 'body_too_large');
  assert.equal(app.calls.length, 0);
});

test('log tidak mencatat isi pesan pribadi', async t => {
  const logs = [];
  const app = await withServer(t, {
    logger: { log: value => logs.push(String(value)), error() {} }
  });
  const privateText = 'ISI-PESAN-RAHASIA-TEST';
  await app.post(payload({ id: 'privacy-id', body: privateText }));
  assert.equal(logs.some(line => line.includes(privateText)), false);
});
