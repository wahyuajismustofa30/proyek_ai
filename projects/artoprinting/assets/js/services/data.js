// data.js — mengambil file JSON situs. Setiap file hanya diambil sekali per halaman.

import { CONFIG } from '../config.js';
import { rapikanTeks, slug } from '../utils/teks.js';

const cache = new Map();

function ambilJSON(url) {
  if (!cache.has(url)) {
    const p = fetch(url).then((res) => {
      if (!res.ok) throw new Error(`Gagal memuat ${url} (HTTP ${res.status})`);
      return res.json();
    });
    // jangan simpan kegagalan, supaya tombol "coba lagi" benar-benar mengambil ulang
    p.catch(() => cache.delete(url));
    cache.set(url, p);
  }
  return cache.get(url);
}

/**
 * Data produk: { Undangan_Cetak: [...], Mug: [...], ..., updated: "..." }
 * Mengembalikan { daftar: {kunci: array}, updated }
 */
export async function getProduk() {
  const raw = await ambilJSON(CONFIG.dataUrl.produk);
  const daftar = {};
  Object.keys(raw).forEach((k) => { if (Array.isArray(raw[k])) daftar[k] = raw[k]; });
  return { daftar, updated: raw.updated };
}

/** setting.json; bila gagal dimuat, katalog tetap jalan tanpa deskripsi. */
export function getSetting() {
  return ambilJSON(CONFIG.dataUrl.setting).catch(() => null);
}

/** ulasan.json -> array ulasan */
export async function getUlasan() {
  const data = await ambilJSON(CONFIG.dataUrl.ulasan);
  return data.ulasan || [];
}

/** Urutkan kunci produk sesuai CONFIG.urutanProduk. */
export function urutkanProduk(keys) {
  const urutan = CONFIG.urutanProduk;
  const ada = keys.filter((k) => urutan.includes(k)).sort((a, b) => urutan.indexOf(a) - urutan.indexOf(b));
  return ada.concat(keys.filter((k) => !urutan.includes(k)));
}

/** Deskripsi kategori: pengganti di CONFIG, atau dari setting.json (katalog[].data === slug). */
export function deskripsiProduk(key, setting) {
  const s = slug(key);
  if (CONFIG.deskripsiKhusus[s]) return CONFIG.deskripsiKhusus[s];
  const item = ((setting && setting.katalog) || []).find((k) => k.data === s);
  return item ? rapikanTeks(item.deskripsi) : '';
}
