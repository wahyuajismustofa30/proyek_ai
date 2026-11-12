// site-menu.js — tombol "Menu" pada layar kecil (header bersama).

export function initSiteMenu() {
  const btn = document.querySelector('.menu-btn');
  const nav = document.getElementById('site-nav');
  if (!btn || !nav) return;

  const tutup = () => {
    nav.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  };

  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', tutup));
  // Esc menutup menu dan mengembalikan fokus ke tombol; klik di luar menu juga menutup
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('open')) { tutup(); btn.focus(); }
  });
  document.addEventListener('click', (e) => {
    if (nav.classList.contains('open') && !nav.contains(e.target) && !btn.contains(e.target)) tutup();
  });
  tandaiHalamanAktif(nav);
}

/** Beri aria-current="page" pada menu yang sesuai alamat sekarang (/laman/katalog/ = /Katalog). */
function tandaiHalamanAktif(nav) {
  const rapikan = (p) => p.replace(/index\.html$/, '').replace(/\/+$/, '').toLowerCase() || '/';
  const sekarang = rapikan(window.location.pathname);
  nav.querySelectorAll('a').forEach((a) => {
    const tujuan = rapikan(new URL(a.getAttribute('href'), window.location.origin).pathname);
    if (tujuan !== '/' && tujuan === sekarang) a.setAttribute('aria-current', 'page');
  });
}
