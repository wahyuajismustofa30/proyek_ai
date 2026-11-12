// product-card.js — markup kartu produk (dipakai katalog beranda dan "produk terkait").

import { CONFIG } from '../config.js';
import { esc, label, slug } from '../utils/teks.js';

/** "Ready" / "Pre Order" dari field status atau keterangan; selain itu kosong. */
export function statusOf(p) {
  const s = (p.status || p.keterangan || '').trim();
  return /^(ready|pre order)$/i.test(s) ? s : '';
}

export function isExternal(url) {
  return /^https?:\/\//i.test(url || '');
}

/**
 * Link produk dari data. produk.json masih menyimpan "/produk.html?p=..&id=.." (data tidak diubah);
 * di sini diarahkan langsung ke halaman barunya "/laman/produk/?p=..&id=..".
 * Link eksternal (Undangan Web) dibiarkan apa adanya.
 */
export function linkProduk(p) {
  const link = p.link_produk || '#';
  if (!link.startsWith('/produk.html')) return link;
  // ?p=Undangan_Cetak&id=5  ->  ?p=undangan-cetak&id=5  (semua huruf kecil)
  const q = new URLSearchParams(link.split('?')[1] || '');
  if (q.has('p')) q.set('p', slug(q.get('p')));
  return `${CONFIG.halaman.produk}?${q.toString()}`;
}

export function waLink(text) {
  return `https://wa.me/${CONFIG.waAdmin}?text=${encodeURIComponent(text)}`;
}

/**
 * Label di pojok foto. Hanya "Ready" yang ditandai (lengkap dengan stok bila ada, mis. "Ready 300 pcs"),
 * karena hampir semua desain lain berstatus Pre Order; info itu ada di teks pengantar katalog.
 */
export function badgeHTML(p) {
  if (!/^ready$/i.test(statusOf(p))) return '';
  const ket = String(p.keterangan || '').trim();
  const teks = /^ready\b/i.test(ket) ? ket : (p.stok ? `Ready ${p.stok} pcs` : 'Ready');
  return `<span class="badge ready">${esc(teks)}</span>`;
}

/**
 * Ganti foto yang gagal dimuat dengan logo, supaya tidak tampil ikon gambar rusak.
 * Dipasang sekali pada wadah (grid); berlaku juga untuk kartu yang ditambahkan kemudian.
 */
export function pasangFallbackGambar(wadah) {
  if (!wadah || wadah.dataset.fallbackGambar) return;
  wadah.dataset.fallbackGambar = '1';
  wadah.addEventListener('error', (e) => {
    const img = e.target;
    if (img.tagName !== 'IMG' || img.dataset.fallback) return;
    img.dataset.fallback = '1';
    img.classList.add('img-fallback');
    img.src = CONFIG.img.fallbackProduk;
  }, true);
}

export function cardHTML(p, key) {
  const link = linkProduk(p);
  const ext = isExternal(link);
  const sub = p.kategori || label(key);
  return `
      <a class="card" href="${esc(link)}"${ext ? ' target="_blank" rel="noopener"' : ''}>
        <div class="card-media">
          ${badgeHTML(p)}
          <img src="${esc(p.img)}" alt="${esc(p.nama)}" loading="lazy" decoding="async">
        </div>
        <p class="card-title">${esc(p.nama)}</p>
        <p class="card-sub">${esc(sub)}</p>
        ${ext ? '<span class="card-ext">Buka demo</span>' : ''}
      </a>`;
}

/** Kotak "kosong"/"gagal" dengan maskot kecil. `isiHTML` sudah harus aman (escaped). */
export function emptyHTML(isiHTML) {
  return `<div class="empty"><img class="empty-mascot" src="${CONFIG.img.maskot}" alt="">${isiHTML}</div>`;
}
