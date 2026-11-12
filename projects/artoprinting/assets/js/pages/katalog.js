// katalog.js — titik masuk halaman Katalog (/laman/katalog/).
// Kontrak URL: /laman/katalog/?produk=undangan-cetak&kategori=avis

import '../core/site.js';
import { getProduk, getSetting, urutkanProduk } from '../services/data.js';
import { createKatalog } from '../features/katalog.js';

const katalog = createKatalog();

async function muat() {
  try {
    const [{ daftar, updated }, setting] = await Promise.all([getProduk(), getSetting()]);
    if (updated) window.updated = updated;
    katalog.mulai(daftar, setting, urutkanProduk(Object.keys(daftar)));
  } catch (err) {
    console.error(err);
    katalog.renderGagal(muat);
  }
}

muat();
