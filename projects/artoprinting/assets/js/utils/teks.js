// teks.js — fungsi kecil untuk mengolah teks. Tidak bergantung pada DOM.

/** Escape teks agar aman dimasukkan ke HTML/atribut. */
export function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/** "Undangan_Cetak" -> "Undangan Cetak" */
export function label(key) {
  return String(key).replace(/_/g, ' ');
}

/** "Undangan_Cetak" -> "undangan-cetak" (dipakai di URL ?produk=) */
export function slug(key) {
  return String(key).toLowerCase().replace(/_/g, '-');
}

/** Data dari spreadsheet kadang membawa "?" sebagai pengganti tanda pisah. */
export function rapikanTeks(t) {
  return String(t || '').replace(/\s\?\s/g, ' – ').replace(/(\w)\?(\w)/g, '$1 – $2').trim();
}

/**
 * Validasi URL dari data dinamis. Hanya URL HTTPS dan path internal yang diterima.
 * Protokol lain (mis. javascript:, data:, blob:) serta URL protocol-relative ditolak.
 */
export function urlAman(value) {
  const url = String(value == null ? '' : value).trim();
  if (!url || /[\\\u0000-\u0020\u007f]/.test(url)) return '';

  if (url.startsWith('/') && !url.startsWith('//')) return url;

  if (/^https:\/\//i.test(url)) {
    try {
      const parsed = new URL(url);
      if (parsed.protocol === 'https:' && parsed.hostname && !parsed.username && !parsed.password) return url;
    } catch {
      // URL tidak valid.
    }
  }
  return '';
}

/** Angka dengan pemisah ribuan Indonesia. */
export function angka(n) {
  return Number(n).toLocaleString('id-ID');
}
