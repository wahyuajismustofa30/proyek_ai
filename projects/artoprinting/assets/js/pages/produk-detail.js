// produk-detail.js — titik masuk halaman detail produk (/laman/produk/).
// Parameter: ?p=<slug-produk>&id=<id>  (mis. ?p=undangan-cetak&id=5; ?p=Undangan_Cetak juga diterima)
// Alamat lama /produk.html?p=..&id=.. (masih tertulis di produk.json) dialihkan oleh /produk.html.

import '../core/site.js';
import { CONFIG } from '../config.js';
import { esc, label, slug } from '../utils/teks.js';
import { getProduk } from '../services/data.js';
import { cardHTML, statusOf, waLink, pasangFallbackGambar } from '../components/product-card.js';

const DESKRIPSI_DEFAULT = 'Ukuran, bahan, jumlah, dan isi teks bisa disesuaikan. Tanyakan detailnya ke admin sebelum produksi.';

function getQueryParam(param) {
  return new URLSearchParams(window.location.search).get(param);
}

function renderKosong(container) {
  container.setAttribute('aria-busy', 'false');
  container.innerHTML = `
      <div class="empty">
        <p>Produk ini tidak ditemukan. Mungkin sudah tidak tersedia atau link-nya berubah.</p>
        <a class="btn btn-ink btn-sm" href="${CONFIG.halaman.katalog}">Kembali ke katalog</a>
      </div>`;
}

function renderGagal(container) {
  container.setAttribute('aria-busy', 'false');
  container.innerHTML = `
      <div class="empty">
        <p>Data produk belum bisa dimuat. Periksa koneksi internet, lalu coba lagi.</p>
        <button class="btn btn-ink btn-sm" type="button" id="muat-ulang-produk">Coba lagi</button>
      </div>`;
  document.getElementById('muat-ulang-produk').addEventListener('click', main);
}

/** Meta SEO & berbagi untuk produk yang sedang dibuka (halaman ini dirender oleh JavaScript). */
function perbaruiMeta(produk, sheet) {
  const url = `${location.origin}${CONFIG.halaman.produk}?p=${slug(sheet)}&id=${encodeURIComponent(produk.id)}`;
  const desk = `${produk.nama} (${label(sheet)}${produk.kategori ? ', ' + produk.kategori : ''}) dari Arto Printing, Bobotsari, Purbalingga. Pesan atau tanya detailnya lewat WhatsApp.`;
  const set = (sel, attr, val) => { const el = document.querySelector(sel); if (el) el.setAttribute(attr, val); };
  set('meta[name="description"]', 'content', desk);
  set('meta[property="og:title"]', 'content', document.title);
  set('meta[property="og:description"]', 'content', desk);
  set('meta[property="og:url"]', 'content', url);
  set('link[rel="canonical"]', 'href', url);
}

function renderDetail(container, produk, sheet) {
  const status = statusOf(produk);
  const katalogURL = `${CONFIG.halaman.katalog}?produk=${slug(sheet)}${produk.kategori ? '&kategori=' + encodeURIComponent(produk.kategori.toLowerCase()) : ''}`;
  const pesan = `Halo Arto Printing, saya ingin pesan ${produk.nama}` +
    `${produk.kategori ? ' (' + produk.kategori + ')' : ''}.\n${window.location.href}`;

  document.title = `${produk.nama} - Arto Printing`;
  perbaruiMeta(produk, sheet);
  const crumbs = document.getElementById('crumbs');
  if (crumbs) {
    crumbs.innerHTML = `<a href="/">Beranda</a> / <a href="${esc(katalogURL)}">${esc(label(sheet))}</a> / <span>${esc(produk.nama)}</span>`;
  }

  // "Ready"/"Pre Order" sudah tampil sebagai Ketersediaan, jadi tidak diulang sebagai deskripsi
  container.setAttribute('aria-busy', 'false');
  const ket = (produk.keterangan && !/^(ready|pre order)$/i.test(produk.keterangan)) ? produk.keterangan : '';
  container.innerHTML = `
      <div class="detail-media">
        <img src="${esc(produk.img || CONFIG.img.fallbackProduk)}" alt="${esc(produk.nama)}">
      </div>
      <div class="detail-info">
        <h1>${esc(produk.nama || '-')}</h1>
        <p class="desc">${esc(ket || DESKRIPSI_DEFAULT)}</p>
        <dl class="specs">
          <div><dt>Produk</dt><dd>${esc(label(sheet))}</dd></div>
          ${produk.kategori ? `<div><dt>Kategori</dt><dd>${esc(produk.kategori)}</dd></div>` : ''}
          ${status ? `<div><dt>Ketersediaan</dt><dd>${esc(status)}</dd></div>` : ''}
          ${produk.stok ? `<div><dt>Stok</dt><dd>${esc(produk.stok)}</dd></div>` : ''}
          ${produk.harga ? `<div><dt>Harga</dt><dd>Rp${Number(produk.harga).toLocaleString('id-ID')}</dd></div>` : ''}
        </dl>
        <div class="detail-actions">
          <a class="btn btn-wa" href="${esc(waLink(pesan))}" target="_blank" rel="noopener">Pesan lewat WhatsApp</a>
          <a class="btn btn-line" href="${esc(katalogURL)}">Kembali ke katalog</a>
        </div>
        <p class="detail-note">Pesan WhatsApp sudah berisi nama produk dan link halaman ini, jadi admin langsung tahu model yang kamu maksud. <a class="link-more" href="${CONFIG.halaman.caraPesan}">Lihat cara pesan</a></p>
      </div>`;

  return katalogURL;
}

/** Maksimal 8 desain lain dari kategori yang sama, dimulai dari posisi produk ini. */
function renderTerkait(list, produk, sheet, katalogURL) {
  const box = document.getElementById('terkait-list');
  const wrap = document.getElementById('produk-terkait');
  if (!box || !wrap) return;
  const sama = list.filter((p) => String(p.id) !== String(produk.id) && (p.kategori || '') === (produk.kategori || ''));
  if (!sama.length) return;
  const idx = Math.max(0, list.indexOf(produk));
  const urut = sama.slice(idx % sama.length).concat(sama.slice(0, idx % sama.length)).slice(0, 8);
  box.innerHTML = urut.map((p) => cardHTML(p, sheet)).join('');
  const semua = document.getElementById('terkait-semua');
  if (semua) semua.href = katalogURL;
  wrap.classList.remove('hidden');
}

async function main() {
  const container = document.getElementById('produk-detail');
  pasangFallbackGambar(container);
  pasangFallbackGambar(document.getElementById('terkait-list'));
  const sheet = getQueryParam('p');
  const id = getQueryParam('id');
  if (!sheet || !id) return renderKosong(container);

  let daftar;
  try {
    ({ daftar } = await getProduk());
  } catch (err) {
    console.error(err);
    return renderGagal(container);
  }
  // ?p= menerima slug huruf kecil (undangan-cetak) maupun kunci data lama (Undangan_Cetak)
  const kunci = Object.keys(daftar).find((k) => k === sheet || slug(k) === slug(sheet));
  const list = kunci ? daftar[kunci] : [];
  const produk = list.find((p) => String(p.id) === String(id));
  if (!produk) return renderKosong(container);
  // rapikan alamat lama (?p=Undangan_Cetak) jadi huruf kecil, supaya link yang dibagikan seragam
  if (sheet !== slug(kunci)) {
    const q = new URLSearchParams(window.location.search);
    q.set('p', slug(kunci));
    history.replaceState({}, '', `${window.location.pathname}?${q.toString()}${window.location.hash}`);
  }
  const katalogURL = renderDetail(container, produk, kunci);
  renderTerkait(list, produk, kunci, katalogURL);
}

main();
