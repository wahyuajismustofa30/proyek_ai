'use strict';

const DEFAULT_LABELS = Object.freeze({
  owner: 'Owner',
  personal: 'Pribadi',
  arto: 'Customer ArtoPrinting',
  dekeku: 'Customer Dekeku'
});

function normalizeLabel(value) {
  return typeof value === 'string' ? value.trim().toLocaleLowerCase('id-ID') : '';
}

function createLabelConfig(env = process.env) {
  return Object.freeze({
    owner: env.WA_LABEL_OWNER || DEFAULT_LABELS.owner,
    personal: env.WA_LABEL_PERSONAL || DEFAULT_LABELS.personal,
    arto: env.WA_LABEL_ARTOPRINTING || DEFAULT_LABELS.arto,
    dekeku: env.WA_LABEL_DEKEKU || DEFAULT_LABELS.dekeku,
    ownerJid: env.OWNER_JID || '',
    personalMode: env.PERSONAL_MODE === 'true'
  });
}

function resolveLabels(labels, config = createLabelConfig()) {
  if (!Array.isArray(labels)) throw new TypeError('LABELS_MUST_BE_ARRAY');
  const normalized = new Set(labels.map(normalizeLabel).filter(Boolean));
  const has = key => normalized.has(normalizeLabel(config[key]));
  return {
    owner: has('owner'),
    personal: has('personal'),
    arto: has('arto'),
    dekeku: has('dekeku')
  };
}

function resolveRoute({ chatId, sender, labels = [], message = '', confirmedPurposes = [] }, config = createLabelConfig()) {
  if (typeof chatId !== 'string' || !chatId || typeof sender !== 'string' || !sender) {
    return { action: 'reject', reason: 'invalid_identity', routes: [] };
  }

  // OWNER identity comes only from the configured JID, never from a contact label or claim.
  if (sender === config.ownerJid && chatId === config.ownerJid) {
    return { action: 'route', reason: 'verified_owner', routes: ['OWNER'], labelsToAdd: [] };
  }

  const found = resolveLabels(labels, config);
  if (found.owner) {
    return { action: 'hold', reason: 'owner_label_on_non_owner', routes: [], labelsToAdd: [] };
  }

  const routes = [];
  if (found.personal && config.personalMode) routes.push('PERSONAL');
  if (found.arto) routes.push('ARTOPRINTING');
  if (found.dekeku) routes.push('DEKEKU');

  if (routes.length) {
    return { action: 'route', reason: 'contact_labels', routes, labelsToAdd: [] };
  }

  const purposes = new Set(confirmedPurposes);
  const labelsToAdd = [];
  if (purposes.has('personal')) labelsToAdd.push(config.personal);
  if (purposes.has('artoprinting')) labelsToAdd.push(config.arto);
  if (purposes.has('dekeku')) labelsToAdd.push(config.dekeku);

  if (labelsToAdd.length) {
    const confirmedRoutes = [];
    if (purposes.has('personal') && config.personalMode) confirmedRoutes.push('PERSONAL');
    if (purposes.has('artoprinting')) confirmedRoutes.push('ARTOPRINTING');
    if (purposes.has('dekeku')) confirmedRoutes.push('DEKEKU');
    return {
      action: confirmedRoutes.length ? 'route' : 'hold',
      reason: confirmedRoutes.length ? 'confirmed_purpose' : 'personal_mode_disabled',
      routes: confirmedRoutes,
      labelsToAdd
    };
  }

  return {
    action: 'classify',
    reason: 'unlabeled_contact',
    routes: [],
    question: 'Halo, boleh tahu kamu menghubungi saya untuk keperluan pribadi, ArtoPrinting, DEKEKU, atau beberapa di antaranya?'
  };
}

module.exports = { DEFAULT_LABELS, createLabelConfig, resolveLabels, resolveRoute };
