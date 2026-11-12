// beranda.js — titik masuk halaman Beranda (/).
// Hero, ringkasan jenis produk, dan cuplikan testimoni.

import '../core/site.js';
import { CONFIG } from '../config.js';
import { getProduk, urutkanProduk } from '../services/data.js';
import { renderHero } from '../features/hero.js';
import { renderKategoriRingkas } from '../features/kategori-ringkas.js';
import { initTestimoni } from '../features/testimoni.js';
import { renderLayananRingkas } from '../features/layanan.js';

async function muat() {
  try {
    const { daftar, updated } = await getProduk();
    if (updated) window.updated = updated;
    const produkList = urutkanProduk(Object.keys(daftar));
    renderHero(daftar, produkList);
    renderKategoriRingkas(daftar, produkList);
    renderLayananRingkas(daftar.Layanan);
  } catch (err) {
    console.error(err);
    const box = document.getElementById('kategori-ringkas');
    if (box) box.innerHTML = `<p class="empty">Daftar produk belum bisa dimuat. <a href="${CONFIG.halaman.katalog}">Buka katalog</a></p>`;
  }
}

muat();
initTestimoni({ awal: CONFIG.testimoniBeranda });
