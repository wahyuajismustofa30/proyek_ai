'use strict';

const crypto = require('node:crypto');

const SECRET = 'a'.repeat(64);
const OWNER_JID = '6285161517176@s.whatsapp.net';
const DEVICE_ID = 'test-device';

function sign(body, secret = SECRET) {
  return `sha256=${crypto.createHmac('sha256', secret).update(body).digest('hex')}`;
}

function payload(overrides = {}) {
  return {
    device_id: OWNER_JID,
    event: 'message',
    payload: {
      id: 'message-1',
      chat_id: '6281111111111@s.whatsapp.net',
      from: '6281111111111@s.whatsapp.net',
      is_from_me: false,
      body: 'Halo',
      ...overrides
    }
  };
}

function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((res, rej) => { resolve = res; reject = rej; });
  return { promise, resolve, reject };
}

module.exports = { SECRET, OWNER_JID, DEVICE_ID, sign, payload, deferred };
