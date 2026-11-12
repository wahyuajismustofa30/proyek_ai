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

/** Angka dengan pemisah ribuan Indonesia. */
export function angka(n) {
  return Number(n).toLocaleString('id-ID');
}
