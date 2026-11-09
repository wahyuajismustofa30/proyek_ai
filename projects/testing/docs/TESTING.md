# Strategi Testing — Testing Web Page Lab

## Risiko dan cakupan

- Risiko utama: markup rusak, aset lokal hilang, layout tidak responsif, atau interaksi form/menu tidak berjalan.
- Data test: sintetis; tidak menggunakan data produksi.
- Dampak kegagalan: halaman demo tidak dapat digunakan atau tidak memenuhi kontrak web dasar.

## Perintah standar

```bash
npm test
python -m http.server 8080 --directory src
```

## Validasi otomatis

- Node built-in test runner memeriksa struktur HTML, landmark, viewport, aset lokal, breakpoint CSS, dan fungsi validasi email.
- CI root memvalidasi HTML, CSS, SVG, serta referensi aset lokal.
- Project matrix menjalankan `npm test` untuk stack Node.js.

## Skenario minimum

- [x] Kontrak halaman dan metadata dasar.
- [x] Referensi aset lokal tersedia.
- [x] CSS memiliki breakpoint mobile.
- [x] Email valid dan tidak valid.
- [ ] Review keyboard dan screen reader manual.
- [ ] Review visual pada browser desktop dan mobile.
- [ ] Browser-based end-to-end test bila kebutuhan bertambah.

## Batasan

Test Node saat ini tidak merender DOM dan tidak menggantikan browser automation, visual regression, atau audit aksesibilitas penuh.

## Keamanan

- Tidak ada secret atau data pribadi.
- Form demo tidak mengirim data.
- Tidak ada dependency runtime pihak ketiga.

## Hasil verifikasi terakhir

| Tanggal | Commit | Pemeriksaan | Status | Catatan |
|---|---|---|---|---|
| 2026-11-09 | 795b5db | `npm ci` + `npm test` | PASS | Job `projects/testing / node` berhasil. |
| 2026-11-09 | 795b5db | Discovery + HTML/CSS/aset | PASS | Discovery dan web validation berhasil. |
| 2026-11-09 | 795b5db | OSV-Scanner | PASS | Pemindaian dependency berhasil. |
| 2026-11-09 | 795b5db | Markdown lint | FAIL | Run awal menemukan format Markdown; sudah diperbaiki di commit berikutnya, tetapi revisi akhir belum diuji ulang. |
