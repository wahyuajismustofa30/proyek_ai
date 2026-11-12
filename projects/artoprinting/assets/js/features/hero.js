// hero.js — tumpukan foto undangan dan angka ringkas di hero beranda.

import { angka } from '../utils/teks.js';

function setText(id, txt) {
  const el = document.getElementById(id);
  if (el) el.textContent = txt;
}

/**
 * @param {Object<string, Array>} daftar  data produk per kunci
 * @param {string[]} produkList           kunci produk yang tampil
 */
export function renderHero(daftar, produkList) {
  const stack = document.getElementById('hero-stack');
  const undangan = daftar.Undangan_Cetak || [];

  if (stack && undangan.length) {
    // pilih 3 foto: utamakan model berstatus Ready
    const ready = undangan.filter((p) => /ready/i.test(p.status || ''));
    const pool = ready.length >= 3 ? ready : undangan;
    const pilih = [pool[Math.floor(pool.length * 0.15)], pool[Math.floor(pool.length * 0.55)], pool[0]];
    stack.querySelectorAll('.proof img').forEach((img, i) => {
      if (pilih[i]) { img.src = pilih[i].img; img.alt = pilih[i].nama; }
    });
    requestAnimationFrame(() => setTimeout(() => stack.classList.remove('is-loading'), 60));
  }

  const total = produkList.reduce((n, k) => n + daftar[k].length, 0);
  setText('stat-total', angka(total));
  setText('stat-undangan', angka(undangan.length));
  setText('stack-count', `${angka(undangan.length)} model undangan`);
  setText('stat-jenis', angka(produkList.length));
}
