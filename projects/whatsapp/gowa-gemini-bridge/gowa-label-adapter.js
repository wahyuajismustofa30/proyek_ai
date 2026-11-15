'use strict';

/**
 * Fail-closed adapter contract.
 *
 * The installed GoWA label endpoints and payload schema must be verified against
 * the deployed GoWA source before implementing these operations. No guessed
 * endpoint is called by this adapter.
 */
function createGoWaLabelAdapter({ readLabels, addLabel, dryRun = true } = {}) {
  return Object.freeze({
    async getLabels(chatId) {
      if (typeof chatId !== 'string' || !chatId) throw new Error('INVALID_CHAT_ID');
      if (dryRun) return { supported: false, labels: [], simulated: true };
      if (typeof readLabels !== 'function') throw new Error('GOWA_LABEL_READ_NOT_CONFIGURED');
      const labels = await readLabels(chatId);
      if (!Array.isArray(labels)) throw new Error('GOWA_LABEL_READ_INVALID_RESPONSE');
      return { supported: true, labels, simulated: false };
    },

    async addLabels(chatId, labels) {
      if (typeof chatId !== 'string' || !chatId) throw new Error('INVALID_CHAT_ID');
      if (!Array.isArray(labels) || labels.some(label => typeof label !== 'string' || !label.trim())) {
        throw new Error('INVALID_LABELS');
      }
      if (dryRun) return { applied: false, simulated: true, labels: [...new Set(labels)] };
      if (typeof addLabel !== 'function') throw new Error('GOWA_LABEL_WRITE_NOT_CONFIGURED');
      // Additive operation only: the adapter contract never replaces the full label set.
      return addLabel(chatId, [...new Set(labels)]);
    }
  });
}

module.exports = { createGoWaLabelAdapter };
