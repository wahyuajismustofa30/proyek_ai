// layanan.js — titik masuk halaman Layanan (/laman/layanan/).

import '../core/site.js';
import { getProduk } from '../services/data.js';
import { renderLayanan } from '../features/layanan.js';

async function muat() {
  const box = document.getElementById('layanan-list');
  try {
    const { daftar } = await getProduk();
    renderLayanan(daftar.Layanan);
  } catch (err) {
    console.error(err);
    if (box) {
      box.innerHTML = '<p class="empty">Daftar layanan belum bisa dimuat. <button class="btn btn-line btn-sm" type="button" id="muat-ulang-layanan">Coba lagi</button></p>';
      document.getElementById('muat-ulang-layanan').addEventListener('click', muat);
    }
  }
}

muat();
