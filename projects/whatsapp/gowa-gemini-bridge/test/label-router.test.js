'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { createLabelConfig, resolveLabels, resolveRoute } = require('../label-router');
const { createGoWaLabelAdapter } = require('../gowa-label-adapter');

const config = createLabelConfig({
  OWNER_JID: '6281234567890@s.whatsapp.net',
  WA_LABEL_OWNER: 'Owner',
  WA_LABEL_PERSONAL: 'Pribadi',
  WA_LABEL_ARTOPRINTING: 'Customer ArtoPrinting',
  WA_LABEL_DEKEKU: 'Customer Dekeku',
  PERSONAL_MODE: 'true'
});

test('label dapat dikonfigurasi dan pencocokan tidak sensitif kapitalisasi', () => {
  assert.deepEqual(resolveLabels(['customer dekeku', 'CUSTOMER ARTOPRINTING'], config), {
    owner: false, personal: false, arto: true, dekeku: true
  });
});

test('OWNER hanya dikenali dari JID terkonfigurasi', () => {
  assert.equal(resolveRoute({
    chatId: config.ownerJid, sender: config.ownerJid, labels: ['Customer Dekeku']
  }, config).routes[0], 'OWNER');
  assert.equal(resolveRoute({
    chatId: '6289999999999@s.whatsapp.net',
    sender: '6289999999999@s.whatsapp.net',
    labels: ['Owner']
  }, config).reason, 'owner_label_on_non_owner');
});

test('satu kontak dapat dirutekan ke dua bisnis sekaligus', () => {
  const result = resolveRoute({
    chatId: '6281111111111@s.whatsapp.net',
    sender: '6281111111111@s.whatsapp.net',
    labels: ['Customer ArtoPrinting', 'Customer Dekeku']
  }, config);
  assert.deepEqual(result.routes, ['ARTOPRINTING', 'DEKEKU']);
});

test('Pribadi hanya dirutekan ketika personal mode aktif', () => {
  const active = resolveRoute({
    chatId: '6281111111111@s.whatsapp.net',
    sender: '6281111111111@s.whatsapp.net',
    labels: ['Pribadi']
  }, config);
  assert.deepEqual(active.routes, ['PERSONAL']);

  const inactiveConfig = createLabelConfig({ OWNER_JID: config.ownerJid, PERSONAL_MODE: 'false' });
  const inactive = resolveRoute({
    chatId: '6281111111111@s.whatsapp.net',
    sender: '6281111111111@s.whatsapp.net',
    labels: ['Pribadi']
  }, inactiveConfig);
  assert.equal(inactive.action, 'classify');
});

test('kontak tanpa label masuk proses klasifikasi dan tidak diberi label otomatis', () => {
  const result = resolveRoute({
    chatId: '6281111111111@s.whatsapp.net',
    sender: '6281111111111@s.whatsapp.net'
  }, config);
  assert.equal(result.action, 'classify');
  assert.deepEqual(result.routes, []);
  assert.equal(result.labelsToAdd, undefined);
});

test('label hanya diusulkan setelah tujuan dikonfirmasi dan bersifat aditif', () => {
  const result = resolveRoute({
    chatId: '6281111111111@s.whatsapp.net',
    sender: '6281111111111@s.whatsapp.net',
    confirmedPurposes: ['artoprinting', 'dekeku']
  }, config);
  assert.deepEqual(result.labelsToAdd, ['Customer ArtoPrinting', 'Customer Dekeku']);
  assert.deepEqual(result.routes, ['ARTOPRINTING', 'DEKEKU']);
});

test('GoWA adapter DRY-RUN tidak membaca atau mengubah label aktual', async () => {
  let called = false;
  const adapter = createGoWaLabelAdapter({
    dryRun: true,
    readLabels: async () => { called = true; return []; },
    addLabel: async () => { called = true; }
  });
  assert.deepEqual(await adapter.getLabels('6281@s.whatsapp.net'), {
    supported: false, labels: [], simulated: true
  });
  assert.equal((await adapter.addLabels('6281@s.whatsapp.net', ['Customer Dekeku'])).applied, false);
  assert.equal(called, false);
});

test('GoWA adapter menolak operasi produksi tanpa implementasi endpoint terverifikasi', async () => {
  const adapter = createGoWaLabelAdapter({ dryRun: false });
  await assert.rejects(adapter.getLabels('6281@s.whatsapp.net'), /GOWA_LABEL_READ_NOT_CONFIGURED/);
  await assert.rejects(adapter.addLabels('6281@s.whatsapp.net', ['Customer Dekeku']), /GOWA_LABEL_WRITE_NOT_CONFIGURED/);
});
