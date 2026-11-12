// layanan.js — bagian "Layanan di toko", dikelompokkan dari data "Layanan".

import { esc } from '../utils/teks.js';
import { linkProduk, pasangFallbackGambar } from '../components/product-card.js';

// Titik di depan judul kelompok memakai warna toska (lihat .service-group h3::before).

export function renderLayanan(layanan) {
  const box = document.getElementById('layanan-list');
  if (!box || !layanan) return;
  pasangFallbackGambar(box);

  const groups = {};
  layanan.forEach((p) => {
    const g = p.kategori || 'Lainnya';
    (groups[g] = groups[g] || []).push(p);
  });

  box.setAttribute('aria-busy', 'false');
  box.innerHTML = Object.keys(groups).map((g) => `
    <div class="service-group">
      <h2>${esc(g)}</h2>
      <ul class="service-list">
        ${groups[g].map((p) => `
          <li><a href="${esc(linkProduk(p))}">
            <img src="${esc(p.img)}" alt="" loading="lazy">
            <span>${esc(p.nama)}</span>
          </a></li>`).join('')}
      </ul>
    </div>`).join('');
}

/** Beranda: daftar nama layanan (tanpa gambar) dari data "Layanan". */
export function renderLayananRingkas(layanan) {
  const box = document.getElementById('layanan-ringkas');
  if (!box || !layanan) return;
  box.innerHTML = layanan.map((p) => `<li>${esc(p.nama)}</li>`).join('');
}
