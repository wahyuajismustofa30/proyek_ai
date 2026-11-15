'use strict';

const http = require('node:http');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { generateReply } = require('./gemini');

function loadEnv() {
  const file = path.join(__dirname, '.env');
  const content = fs.readFileSync(file, 'utf8');

  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    const pos = trimmed.indexOf('=');
    if (pos < 1) continue;

    const key = trimmed.slice(0, pos).trim();
    let value = trimmed.slice(pos + 1).trim();

    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    if (process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
}

loadEnv();

const HOST = process.env.BRIDGE_HOST || '127.0.0.1';
const PORT = Number(process.env.BRIDGE_PORT || 3001);
const SECRET = process.env.WEBHOOK_SECRET || '';
const OWNER_JID = process.env.OWNER_JID || '';
const DEVICE_ID = process.env.GOWA_DEVICE_ID || '';

if (HOST !== '127.0.0.1') {
  throw new Error('Keamanan: BRIDGE_HOST harus 127.0.0.1');
}
if (!Number.isInteger(PORT) || PORT < 1 || PORT > 65535) {
  throw new Error('BRIDGE_PORT tidak valid');
}
if (!SECRET || !/^[a-f0-9]{64}$/i.test(SECRET)) {
  throw new Error('WEBHOOK_SECRET kosong atau formatnya tidak valid');
}
if (!/^\d+@s\.whatsapp\.net$/.test(OWNER_JID)) {
  throw new Error('OWNER_JID tidak valid');
}
if (!DEVICE_ID) {
  throw new Error('GOWA_DEVICE_ID belum diisi');
}

const secretBuffer = Buffer.from(SECRET, 'utf8');
const seenMessages = new Map();
const processingMessages = new Set();
const MAX_BODY = 1024 * 1024;
const MAX_DEDUP = 5000;
const DEDUP_TTL = 60 * 60 * 1000;

function reply(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    let finished = false;

    req.on('data', chunk => {
      size += chunk.length;

      if (size > MAX_BODY) {
        if (!finished) {
          finished = true;
          reject(new Error('BODY_TOO_LARGE'));
        }
        req.destroy();
        return;
      }

      chunks.push(chunk);
    });

    req.on('end', () => {
      if (finished) return;
      finished = true;
      resolve(Buffer.concat(chunks));
    });

    req.on('error', err => {
      if (!finished) {
        finished = true;
        reject(err);
      }
    });
  });
}

function verifySignature(rawBody, header) {
  if (typeof header !== 'string') return false;

  const match = /^sha256=([a-f0-9]{64})$/i.exec(header);
  if (!match) return false;

  const received = Buffer.from(match[1], 'hex');
  const expected = crypto
    .createHmac('sha256', secretBuffer)
    .update(rawBody)
    .digest();

  return received.length === expected.length &&
    crypto.timingSafeEqual(received, expected);
}

function rememberMessage(id) {
  const now = Date.now();

  for (const [key, timestamp] of seenMessages) {
    if (now - timestamp > DEDUP_TTL) seenMessages.delete(key);
  }

  if (seenMessages.has(id)) return false;

  seenMessages.set(id, now);

  while (seenMessages.size > MAX_DEDUP) {
    const oldest = seenMessages.keys().next().value;
    seenMessages.delete(oldest);
  }

  return true;
}

async function handleWebhook(data) {
  if (!data || typeof data !== 'object') return 'invalid_payload';
  if (data.device_id !== OWNER_JID) return 'ignored_device';
  if (data.event !== 'message') return 'ignored_event';
  if (!data.payload || typeof data.payload !== 'object') {
    return 'invalid_message';
  }

  const msg = data.payload;
  const chatId = typeof msg.chat_id === 'string' ? msg.chat_id : '';
  const sender = typeof msg.from === 'string' ? msg.from : '';

  const isOwnerSelfChat =
    msg.is_from_me === true &&
    chatId === OWNER_JID &&
    sender === OWNER_JID;

  if (msg.is_from_me !== false && !isOwnerSelfChat) {
    return 'ignored_outgoing';
  }

  if (!chatId.endsWith('@s.whatsapp.net')) return 'ignored_non_private';
  if (!sender.endsWith('@s.whatsapp.net')) return 'ignored_non_private';

  const body = typeof msg.body === 'string' ? msg.body.trim() : '';
  if (!body) return 'ignored_empty_message';

  const id = typeof msg.id === 'string' ? msg.id : '';
  if (!id) return 'ignored_missing_id';

  if (seenMessages.has(id) || processingMessages.has(id)) {
    return 'duplicate';
  }

  processingMessages.add(id);

  const route = isOwnerSelfChat ? 'OWNER' : 'CUSTOMER';

  try {
    const answer = await generateReply({
      route,
      chatId,
      message: body
    });

    rememberMessage(id);

    console.log(
      `[DRY-RUN] Gemini berhasil | jalur=${route} | panjang_input=${body.length} | panjang_respons=${answer.length}`
    );
    return 'accepted_dry_run';
  } catch (err) {
    console.error(
      `[DRY-RUN] Gemini gagal | jalur=${route} | alasan=${err.message}`
    );
    return 'gemini_failed_dry_run';
  } finally {
    processingMessages.delete(id);
  }
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') {
    return reply(res, 200, { ok: true, mode: 'dry-run' });
  }

  if (req.method !== 'POST' || req.url !== '/webhook') {
    return reply(res, 404, { ok: false, error: 'not_found' });
  }

  try {
    const rawBody = await readBody(req);

    if (!verifySignature(rawBody, req.headers['x-hub-signature-256'])) {
      return reply(res, 401, { ok: false, error: 'invalid_signature' });
    }

    let data;
    try {
      data = JSON.parse(rawBody.toString('utf8'));
    } catch {
      return reply(res, 400, { ok: false, error: 'invalid_json' });
    }

    const result = await handleWebhook(data);
    const msg = data && data.payload && typeof data.payload === 'object'
      ? data.payload : {};
    const event = typeof data.event === 'string'
      ? data.event.replace(/[^a-zA-Z0-9._-]/g, '').slice(0, 40)
      : 'unknown';
    const chatId = typeof msg.chat_id === 'string' ? msg.chat_id : '';
    const chatType = chatId.endsWith('@s.whatsapp.net')
      ? 'private' : 'non_private';

    const sender = typeof msg.from === 'string' ? msg.from : '';

    console.log(
      `[WEBHOOK] event=${event} | account_match=${data.device_id === OWNER_JID} | is_from_me=${String(msg.is_from_me)} | chat_is_owner=${chatId === OWNER_JID} | sender_is_owner=${sender === OWNER_JID} | chat_type=${chatType} | result=${result}`
    );

    if (result === 'gemini_failed_dry_run') {
      return reply(res, 503, { ok: false, result });
    }

    return reply(res, 200, { ok: true, result });
  } catch (err) {
    if (err.message === 'BODY_TOO_LARGE') {
      return reply(res, 413, { ok: false, error: 'body_too_large' });
    }

    console.error('[BRIDGE] Kesalahan internal:', err.message);
    return reply(res, 500, { ok: false, error: 'internal_error' });
  }
});

server.listen(PORT, HOST, () => {
  console.log(`[BRIDGE] Aktif di http://${HOST}:${PORT}`);
  console.log('[BRIDGE] Mode DRY-RUN: Gemini dan balasan WhatsApp nonaktif');
});

server.on('error', err => {
  console.error('[BRIDGE] Gagal berjalan:', err.message);
  process.exitCode = 1;
});
