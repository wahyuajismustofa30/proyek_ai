// site.js — inisialisasi yang dibutuhkan semua halaman (menu & tombol bagikan).
// Diimpor oleh setiap modul halaman; halaman tanpa modul khusus memuatnya langsung:
//   <script type="module" src="/assets/js/core/site.js"></script>

import { initSiteMenu } from '../components/site-menu.js';
import { initShareLinks } from '../components/share-links.js';

let sudah = false;

export function initSite() {
  if (sudah) return;
  sudah = true;
  initSiteMenu();
  initShareLinks();
}

// Modul dijalankan setelah HTML selesai di-parse (type="module" = defer)
initSite();
