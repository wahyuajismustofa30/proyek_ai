/**
 * Utilitas reusable untuk state pemuatan komponen.
 * Gunakan aria-busy hanya selama pekerjaan berlangsung dan sediakan status teks
 * terpisah melalui [data-ui-loading-status] untuk pengumuman yang aksesibel.
 */

function resolveContainer(target) {
  if (typeof target === "string") return document.querySelector(target);
  return target instanceof HTMLElement ? target : null;
}

/**
 * Mengubah state loading sebuah container.
 * Container dapat menyediakan:
 * - [data-ui-loading-indicator] untuk skeleton/spinner.
 * - [data-ui-loading-content] untuk konten setelah proses selesai.
 * - [data-ui-loading-status] untuk pesan status aria-live.
 *
 * @param {HTMLElement|string} target Elemen atau selector CSS.
 * @param {boolean} loading Apakah proses sedang berjalan.
 * @param {{statusText?: string}} options Pesan status opsional.
 * @returns {boolean} false jika container tidak ditemukan.
 */
export function setLoadingState(target, loading, { statusText } = {}) {
  const container = resolveContainer(target);
  if (!container || typeof loading !== "boolean") return false;

  container.setAttribute("aria-busy", String(loading));

  const indicator = container.querySelector("[data-ui-loading-indicator]");
  const content = container.querySelector("[data-ui-loading-content]");
  const status = container.querySelector("[data-ui-loading-status]");

  if (indicator) indicator.hidden = !loading;
  if (content) content.hidden = loading;
  if (status && typeof statusText === "string") status.textContent = statusText;

  return true;
}

/**
 * Menjalankan pekerjaan asynchronous sambil mengelola aria-busy dan indikator.
 * State selalu dikembalikan ke idle, termasuk ketika task melempar error.
 *
 * @param {HTMLElement|string} target Elemen atau selector CSS.
 * @param {() => Promise<*>} task Pekerjaan asynchronous yang dijalankan.
 * @param {{loadingText?: string, doneText?: string}} options Pesan status.
 * @returns {Promise<*>} Hasil task.
 */
export async function runWithLoadingState(target, task, {
  loadingText = "Sedang memuat konten.",
  doneText = "Pemuatan selesai."
} = {}) {
  if (typeof task !== "function") throw new TypeError("task harus berupa fungsi.");

  const container = resolveContainer(target);
  if (!container) throw new TypeError("Container loading tidak ditemukan.");

  setLoadingState(container, true, { statusText: loadingText });
  try {
    return await task();
  } finally {
    setLoadingState(container, false, { statusText: doneText });
  }
}
