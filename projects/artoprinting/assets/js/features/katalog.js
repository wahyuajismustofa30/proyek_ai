// katalog.js — halaman Katalog: tab jenis produk, filter kategori & ketersediaan,
// pencarian (lintas jenis), grid, "tampilkan lagi", dan bantuan pesan lewat WhatsApp.
//
// Parameter URL (semua opsional, huruf kecil):
//   ?produk=undangan-cetak   jenis produk (tab)
//   &kategori=avis           kategori/model
//   &status=ready            ketersediaan: ready | pre-order
//   &cari=101                kata pencarian

import { CONFIG } from '../config.js';
import { esc, label, slug, angka } from '../utils/teks.js';
import { deskripsiProduk } from '../services/data.js';
import { cardHTML, emptyHTML, statusOf, pasangFallbackGambar } from '../components/product-card.js';

const PER_HALAMAN = CONFIG.katalog.perHalaman;
const STATUS = {
  ready: { label: 'Ready', cocok: (s) => /^ready$/i.test(s) },
  'pre-order': { label: 'Pre Order', cocok: (s) => /^pre order$/i.test(s) },
};

/** "ready" | "pre-order" | "" untuk satu produk. */
function statusKey(p) {
  const s = statusOf(p);
  if (STATUS.ready.cocok(s)) return 'ready';
  if (STATUS['pre-order'].cocok(s)) return 'pre-order';
  return '';
}

function satuan(key) {
  return key === 'Layanan' ? 'layanan' : 'desain';
}

function cocokCari(p, q) {
  return `${p.nama} ${p.kategori || ''} ${p.kode || ''}`.toLowerCase().includes(q);
}

export function createKatalog() {
  const el = {
    tabs: document.getElementById('produk-tabs'),
    chips: document.getElementById('kategori-chips'),
    rowKategori: document.getElementById('filter-kategori'),
    statusChips: document.getElementById('status-chips'),
    rowStatus: document.getElementById('filter-status'),
    grid: document.getElementById('produk-list'),
    loadMore: document.getElementById('load-more'),
    cari: document.getElementById('cari'),
    hapusCari: document.getElementById('hapus-cari'),
    intro: document.getElementById('katalog-intro'),
    meta: document.getElementById('result-meta'),
    saran: document.getElementById('cari-lain'),
    bantuan: document.getElementById('katalog-bantuan'),
    bantuanTeks: document.getElementById('katalog-bantuan-teks'),
    bantuanWa: document.getElementById('katalog-bantuan-wa'),
  };

  let daftar = {};
  let setting = null;
  let produkList = [];
  const state = { produk: CONFIG.katalog.produkAwal, kategori: '', status: '', q: '' };
  let currentList = [];
  let currentIndex = 0;

  pasangFallbackGambar(el.grid);

  // ---------- pencarian & tombol (dipasang sebelum data datang) ----------
  function setCari(nilai, fokus) {
    if (el.cari) el.cari.value = nilai;
    state.q = nilai.trim();
    if (el.hapusCari) el.hapusCari.hidden = !nilai;
    renderProduk(true);
    updateURL();
    if (fokus && el.cari) el.cari.focus();
  }
  if (el.cari) {
    let t;
    el.cari.addEventListener('input', () => {
      if (el.hapusCari) el.hapusCari.hidden = !el.cari.value;
      clearTimeout(t);
      t = setTimeout(() => setCari(el.cari.value, false), CONFIG.katalog.jedaCariMs);
    });
    el.cari.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && el.cari.value) { e.preventDefault(); setCari('', true); }
    });
  }
  if (el.hapusCari) el.hapusCari.addEventListener('click', () => setCari('', true));
  if (el.loadMore) el.loadMore.addEventListener('click', () => renderProduk(false));

  // ---------- data per jenis ----------
  function kategoriDari(key) {
    const hitung = new Map();
    (daftar[key] || []).forEach((p) => { if (p.kategori) hitung.set(p.kategori, (hitung.get(p.kategori) || 0) + 1); });
    return hitung; // Map<kategori, jumlah>, urutan sesuai data
  }

  function statusDari(key) {
    const hitung = { ready: 0, 'pre-order': 0, lain: 0 };
    (daftar[key] || []).forEach((p) => { hitung[statusKey(p) || 'lain'] += 1; });
    return hitung;
  }

  // ---------- URL ----------
  function readURL() {
    const params = new URLSearchParams(window.location.search);
    const p = (params.get('produk') || '').toLowerCase();
    const k = (params.get('kategori') || '').toLowerCase();
    const s = (params.get('status') || '').toLowerCase();
    const found = produkList.find((x) => slug(x) === p);
    state.produk = found || (daftar[CONFIG.katalog.produkAwal] ? CONFIG.katalog.produkAwal : produkList[0]);
    if (k) {
      const kat = [...kategoriDari(state.produk).keys()].find((x) => x.toLowerCase() === k);
      if (kat) state.kategori = kat;
    }
    if (STATUS[s]) state.status = s;
    state.q = (params.get('cari') || '').trim();
    if (el.cari) el.cari.value = state.q;
    if (el.hapusCari) el.hapusCari.hidden = !state.q;
  }

  function updateURL() {
    const params = new URLSearchParams(window.location.search);
    const atur = (k, v) => (v ? params.set(k, v) : params.delete(k));
    params.set('produk', slug(state.produk));
    atur('kategori', state.kategori.toLowerCase());
    atur('status', state.status);
    atur('cari', state.q);
    history.replaceState({}, '', `${window.location.pathname}?${params.toString()}${window.location.hash}`);
  }

  // ---------- tab jenis produk ----------
  function pilihTab(key, fokus) {
    state.produk = key;
    state.kategori = '';
    state.status = '';
    el.tabs.querySelectorAll('.tab').forEach((b) => {
      const aktif = b.dataset.key === key;
      b.setAttribute('aria-selected', aktif);
      b.tabIndex = aktif ? 0 : -1;
      if (aktif && fokus) b.focus();
    });
    renderFilter();
    renderProduk(true);
    updateURL();
  }

  function renderTabs() {
    if (!el.tabs) return;
    el.tabs.innerHTML = produkList.map((k) => {
      const aktif = k === state.produk;
      return `
    <button class="tab" role="tab" type="button" id="tab-${esc(slug(k))}" data-key="${esc(k)}"
      aria-selected="${aktif}" aria-controls="produk-list" tabindex="${aktif ? 0 : -1}">
      ${esc(label(k))}<span class="count">${daftar[k].length}</span>
    </button>`;
    }).join('');
    el.tabs.querySelectorAll('.tab').forEach((btn) => btn.addEventListener('click', () => pilihTab(btn.dataset.key, false)));

    // panah kiri/kanan, Home, End (pola tablist WAI-ARIA)
    el.tabs.addEventListener('keydown', (e) => {
      const tabs = [...el.tabs.querySelectorAll('.tab')];
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      const ke = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (ke === undefined) return;
      e.preventDefault();
      const t = tabs[(ke + tabs.length) % tabs.length];
      pilihTab(t.dataset.key, true);
    });

    // di HP tab bisa digeser; geser ke tab aktif dan tandai bila sudah di ujung
    const active = el.tabs.querySelector('[aria-selected="true"]');
    if (active && state.produk !== produkList[0]) el.tabs.scrollLeft = active.offsetLeft - 24;
    const tandaiUjung = () => el.tabs.classList.toggle('di-ujung', el.tabs.scrollLeft + el.tabs.clientWidth >= el.tabs.scrollWidth - 4);
    el.tabs.addEventListener('scroll', tandaiUjung, { passive: true });
    window.addEventListener('resize', tandaiUjung);
    tandaiUjung();
  }

  // ---------- filter: kategori & ketersediaan ----------
  function chipHTML(nilai, teks, jumlah, aktif, attr) {
    return `<button class="chip" type="button" ${attr}="${esc(nilai)}" aria-pressed="${aktif}">${esc(teks)}<span class="chip-count">${angka(jumlah)}</span></button>`;
  }

  function renderFilter() {
    const total = (daftar[state.produk] || []).length;

    // pengantar + catatan ketersediaan (dari data status/keterangan)
    const st = statusDari(state.produk);
    let catatan = '';
    if (st.ready && st['pre-order']) catatan = ' Desain berlabel Ready stoknya sudah tersedia; yang lain dicetak setelah dipesan (pre order).';
    else if (st['pre-order'] === total && total) catatan = ' Semua desain di sini dicetak setelah dipesan (pre order).';
    if (el.intro) el.intro.textContent = (deskripsiProduk(state.produk, setting) + catatan).trim();

    // kategori
    const kats = kategoriDari(state.produk);
    if (el.chips) {
      if (kats.size < 2) {
        el.chips.innerHTML = '';
      } else {
        el.chips.innerHTML = chipHTML('', 'Semua', total, !state.kategori, 'data-kat') +
          [...kats].map(([k, n]) => chipHTML(k, k, n, k === state.kategori, 'data-kat')).join('');
        el.chips.querySelectorAll('.chip').forEach((c) => c.addEventListener('click', () => {
          state.kategori = c.dataset.kat;
          el.chips.querySelectorAll('.chip').forEach((b) => b.setAttribute('aria-pressed', b === c));
          renderProduk(true);
          updateURL();
        }));
      }
    }
    if (el.rowKategori) el.rowKategori.hidden = kats.size < 2;

    // ketersediaan: hanya bila jenis ini punya Ready dan Pre Order sekaligus
    const adaDua = st.ready > 0 && st['pre-order'] > 0;
    if (el.rowStatus) el.rowStatus.hidden = !adaDua;
    if (el.statusChips) {
      el.statusChips.innerHTML = !adaDua ? '' :
        chipHTML('', 'Semua', total, !state.status, 'data-status') +
        Object.keys(STATUS).map((k) => chipHTML(k, STATUS[k].label, st[k], k === state.status, 'data-status')).join('');
      el.statusChips.querySelectorAll('.chip').forEach((c) => c.addEventListener('click', () => {
        state.status = c.dataset.status;
        el.statusChips.querySelectorAll('.chip').forEach((b) => b.setAttribute('aria-pressed', b === c));
        renderProduk(true);
        updateURL();
      }));
    }
    if (!adaDua) state.status = '';

    // bantuan WhatsApp sesuai jenis yang dibuka
    if (el.bantuanTeks) {
      el.bantuanTeks.textContent = state.produk === 'Layanan'
        ? 'Butuh layanan yang tidak ada di daftar? Tanyakan langsung ke admin.'
        : `Belum ketemu ${label(state.produk).toLowerCase()} yang pas? Admin bisa bantu carikan model lain atau membuat desain sesuai keinginan.`;
    }
    if (el.bantuanWa) {
      const pesan = state.produk === 'Layanan'
        ? 'Halo Arto Printing, saya mau tanya layanan.'
        : `Halo Arto Printing, saya mencari ${label(state.produk).toLowerCase()}.`;
      el.bantuanWa.href = `https://wa.me/${CONFIG.waAdmin}?text=${encodeURIComponent(pesan)}`;
    }
  }

  // ---------- grid ----------
  function saring() {
    let list = daftar[state.produk] || [];
    if (state.kategori) list = list.filter((p) => p.kategori === state.kategori);
    if (state.status) list = list.filter((p) => statusKey(p) === state.status);
    if (state.q) {
      const q = state.q.toLowerCase();
      list = list.filter((p) => cocokCari(p, q));
    }
    // yang Ready tampil lebih dulu; urutan lain mengikuti data
    return list.map((p, i) => [p, i]).sort((a, b) => (statusKey(a[0]) === 'ready' ? 0 : 1) - (statusKey(b[0]) === 'ready' ? 0 : 1) || a[1] - b[1]).map((x) => x[0]);
  }

  /** Jumlah hasil pencarian di jenis produk lain (untuk tombol "Lihat di ..."). */
  function hasilDiJenisLain() {
    if (!state.q) return [];
    const q = state.q.toLowerCase();
    return produkList
      .filter((k) => k !== state.produk)
      .map((k) => [k, daftar[k].filter((p) => cocokCari(p, q)).length])
      .filter(([, n]) => n > 0);
  }

  function renderSaran() {
    if (!el.saran) return;
    const lain = hasilDiJenisLain();
    if (!lain.length) { el.saran.innerHTML = ''; el.saran.hidden = true; return; }
    el.saran.hidden = false;
    el.saran.innerHTML = `<span>Kata "${esc(state.q)}" juga ada di:</span> ` + lain.map(([k, n]) =>
      `<button type="button" class="chip" data-ke="${esc(k)}">${esc(label(k))}<span class="chip-count">${angka(n)}</span></button>`).join('');
    el.saran.querySelectorAll('[data-ke]').forEach((b) => b.addEventListener('click', () => {
      pilihTab(b.dataset.ke, false);
      el.tabs.querySelector('[aria-selected="true"]')?.scrollIntoView({ block: 'nearest', inline: 'center' });
    }));
  }

  function renderProduk(reset) {
    if (!el.grid) return;
    const unit = satuan(state.produk);
    if (reset) {
      currentList = saring();
      currentIndex = 0;
      el.grid.innerHTML = '';
      el.grid.setAttribute('aria-busy', 'false');
      const aktif = el.tabs && el.tabs.querySelector('[aria-selected="true"]');
      if (aktif) el.grid.setAttribute('aria-labelledby', aktif.id);
    }

    if (!currentList.length && !state.q) {
      el.grid.innerHTML = emptyHTML(`<p>Belum ada ${unit} dengan pilihan ini. Coba pilih "Semua", atau tanyakan model terbarunya ke admin lewat WhatsApp.</p>`);
    } else if (!currentList.length) {
      el.grid.innerHTML = emptyHTML(`
        <p>Tidak ada ${esc(label(state.produk).toLowerCase())} dengan kata "${esc(state.q)}"${state.kategori || state.status ? ' pada filter ini' : ''}.</p>
        <p>Coba kata lain, atau tanyakan modelnya langsung ke admin.</p>
        <button class="btn btn-line btn-sm" type="button" id="reset-cari">Hapus pencarian</button>`);
      const r = document.getElementById('reset-cari');
      if (r) r.addEventListener('click', () => setCari('', true));
    } else {
      const batch = currentList.slice(currentIndex, currentIndex + PER_HALAMAN);
      el.grid.insertAdjacentHTML('beforeend', batch.map((p) => cardHTML(p, state.produk)).join(''));
      currentIndex += batch.length;
    }

    if (el.meta) {
      el.meta.textContent = currentList.length ? `Menampilkan ${angka(currentIndex)} dari ${angka(currentList.length)} ${unit}` : '';
    }
    if (el.loadMore) {
      const sisa = currentList.length - currentIndex;
      el.loadMore.classList.toggle('hidden', sisa <= 0);
      el.loadMore.textContent = `Tampilkan ${Math.min(sisa, PER_HALAMAN)} ${unit} lagi`;
    }
    if (reset) renderSaran();
  }

  /** Tampilkan pesan bila data gagal dimuat, dengan tombol coba lagi. */
  function renderGagal(onRetry) {
    if (!el.grid) return;
    el.grid.innerHTML = emptyHTML(`
      <p>Katalog belum bisa dimuat. Periksa koneksi internet, lalu coba lagi.</p>
      <button class="btn btn-line btn-sm" type="button" id="muat-ulang-katalog">Coba lagi</button>`);
    const b = document.getElementById('muat-ulang-katalog');
    if (b) b.addEventListener('click', onRetry);
    if (el.meta) el.meta.textContent = '';
  }

  /** Dipanggil setelah data siap. */
  function mulai(dataProduk, dataSetting, urutanKunci) {
    daftar = dataProduk;
    setting = dataSetting;
    produkList = urutanKunci;
    readURL();
    renderTabs();
    renderFilter();
    renderProduk(true);
    if (el.bantuan) el.bantuan.hidden = false;
  }

  return { mulai, renderGagal };
}
