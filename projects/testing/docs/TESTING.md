# Strategi Testing — Testing Web Page Lab

## Risiko dan cakupan

- Risiko utama: markup rusak, aset lokal menghasilkan HTTP 404, layout tidak responsif, navigasi tidak dapat digunakan, atau interaksi form tidak berjalan.
- Data test: sintetis; tidak menggunakan data produksi.
- Dampak kegagalan: halaman demo tidak dapat digunakan atau tidak memenuhi kontrak web dasar.

## Perintah standar

```bash
npm test
python -m http.server 8080 --directory src
```

## Validasi otomatis

- Node built-in test runner memeriksa struktur HTML, landmark, viewport, dan pemetaan URL aset ke file relatif terhadap document root `src/` (pemeriksaan filesystem, bukan HTTP smoke test).
- Test CSS memeriksa breakpoint mobile dan aturan progressive enhancement agar navigasi tetap terlihat tanpa JavaScript.
- Test perilaku menggunakan DOM stub untuk menu buka/tutup, pemilihan tautan navigasi, validasi form gagal, dan submit berhasil.
- CI root memvalidasi HTML, CSS, dan aset lokal.
- Project matrix menjalankan `npm test` untuk stack Node.js.

## Skenario minimum

- [x] Kontrak halaman dan metadata dasar.
- [x] Resolusi URL aset dari document root.
- [x] CSS breakpoint dan fallback navigasi tanpa JavaScript.
- [x] Perilaku menu dan penutupan melalui tautan.
- [x] Email valid dan invalid, termasuk domain rusak.
- [x] Form menampilkan pesan error/sukses tanpa mengirim data.
- [x] Tombol submit tetap nonaktif tanpa JavaScript dan aktif setelah handler submit dipasang.
- [ ] Review keyboard dan screen reader manual.
- [ ] Review visual pada browser desktop dan mobile.
- [ ] Browser-based end-to-end test bila kebutuhan bertambah.

## Batasan

DOM stub menguji handler JavaScript tanpa dependency, tetapi tidak merender halaman dan tidak menggantikan browser automation, visual regression, pengujian lintas-browser, atau audit aksesibilitas penuh.

## Keamanan

- Tidak ada secret atau data pribadi.
- Form demo tidak mengirim data.
- Tidak ada dependency runtime pihak ketiga.

## Hasil verifikasi

Hasil CI untuk revisi perbaikan dicatat setelah workflow PR terbaru selesai. Hasil run lama tidak dianggap sebagai verifikasi revisi ini.
