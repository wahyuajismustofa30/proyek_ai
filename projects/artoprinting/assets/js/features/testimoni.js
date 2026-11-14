// testimoni.js — ulasan Google dari ulasan.json.
// Halaman Testimoni: 9 tampil dulu, sisanya lewat tombol. Beranda: cuplikan 3 ulasan.

import { CONFIG } from '../config.js';
import { esc, angka, urlAman } from '../utils/teks.js';
import { getUlasan } from '../services/data.js';

const TONES = ['tone-c', 'tone-m', 'tone-y', '', '', ''];

/** Data Google Maps sering diakhiri " …" (teks terpotong); dibuang supaya rapi. */
function bersihkan(t) {
  return String(t || '').replace(/\s*…\s*$/, '').trim();
}

function avatarFallback(nama) {
  const span = document.createElement('span');
  span.className = 'avatar-fallback';
  span.textContent = (nama || '?').trim().charAt(0).toUpperCase();
  return span;
}

/**
 * @param {{awal?: number}} [opsi]  awal = jumlah ulasan yang tampil sebelum tombol "Baca ... lainnya"
 */
export async function initTestimoni(opsi = {}) {
  const box = document.getElementById('testimoni-list');
  const more = document.getElementById('testimoni-more');
  if (!box) return;

  let ulasan = [];
  let tampil = opsi.awal || CONFIG.testimoniAwal;

  function render() {
    box.setAttribute('aria-busy', 'false');
    box.innerHTML = ulasan.slice(0, tampil).map((u, i) => {
      const inisial = esc((u.nama || '?').trim().charAt(0).toUpperCase());
      const avatar = urlAman(u.img);
      return `
        <figure class="review ${TONES[i % TONES.length]}">
          <blockquote>${esc(bersihkan(u.ulasan)).replace(/\n/g, '<br>')}</blockquote>
          <figcaption>
            ${avatar ? `<img src="${esc(avatar)}" alt="" loading="lazy" referrerpolicy="no-referrer" data-nama="${esc(u.nama)}">`
                      : `<span class="avatar-fallback">${inisial}</span>`}
            ${esc(u.nama)}
          </figcaption>
        </figure>`;
    }).join('');

    // foto profil Google kadang kedaluwarsa: ganti dengan inisial
    box.querySelectorAll('figcaption img').forEach((img) => {
      img.addEventListener('error', () => img.replaceWith(avatarFallback(img.dataset.nama)), { once: true });
    });

    const sisa = ulasan.length - tampil;
    if (more) {
      more.classList.toggle('hidden', sisa <= 0);
      more.textContent = `Baca ${sisa} ulasan lainnya`;
    }
  }

  if (more) more.addEventListener('click', () => { tampil = ulasan.length; render(); });

  try {
    ulasan = (await getUlasan()).filter((u) => bersihkan(u.ulasan).length > 0);
  } catch (err) {
    console.error(err);
    box.setAttribute('aria-busy', 'false');
    box.innerHTML = '<p class="empty">Ulasan belum bisa dimuat. Lihat langsung di <a href="https://maps.app.goo.gl/rnVR4BhCsxXkcZiE7" target="_blank" rel="noopener">Google Maps</a>.</p>';
    return;
  }
  const stat = document.getElementById('stat-ulasan');
  if (stat) stat.textContent = angka(ulasan.length);
  render();
}
