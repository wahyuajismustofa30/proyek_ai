// kategori-ringkas.js — kartu "jenis produk" di Beranda.
// Satu kartu per kunci produk.json: foto pertama, nama, jumlah desain,
// menuju /laman/katalog/?produk=<slug>. Kunci "Layanan" menuju halaman /laman/layanan/.

import { CONFIG } from '../config.js';
import { esc, label, slug, angka, urlAman } from '../utils/teks.js';
import { pasangFallbackGambar } from '../components/product-card.js';

export function renderKategoriRingkas(daftar, produkList) {
  const box = document.getElementById('kategori-ringkas');
  if (!box) return;
  pasangFallbackGambar(box);
  box.setAttribute('aria-busy', 'false');
  box.innerHTML = produkList.map((k) => {
    const list = daftar[k] || [];
    const contoh = list.find((p) => p.img) || {};
    const img = urlAman(contoh.img) || urlAman(CONFIG.img.fallbackProduk);
    const isLayanan = k === 'Layanan';
    const href = isLayanan ? CONFIG.halaman.layanan : `${CONFIG.halaman.katalog}?produk=${slug(k)}`;
    return `
      <a class="card" href="${esc(href)}">
        <div class="card-media">
          <img src="${esc(img)}" alt="" loading="lazy" decoding="async">
        </div>
        <p class="card-title">${esc(label(k))}</p>
        <p class="card-sub"><b>${angka(list.length)}</b> ${isLayanan ? 'layanan' : 'desain'}</p>
      </a>`;
  }).join('');
}
