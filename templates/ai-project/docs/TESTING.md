# Strategi Testing — [NAMA PROYEK]

> Lengkapi setelah memilih stack. CI terpusat mendeteksi Node.js, Python, dan PHP.

## Risiko dan cakupan
- Alur paling kritis: [isi]
- Dampak jika gagal: [isi]
- Data test: sintetis/dummy; jangan gunakan data produksi.

## Perintah standar
| Stack | Install | Test | Build / lint |
|---|---|---|---|
| Node.js | `npm ci` (wajib `package-lock.json`) | `npm test` (wajib script `test`) | `npm run lint --if-present`, `npm run build --if-present` |
| Python | `pip install -e ".[test]"` atau `pip install -r requirements.txt` | `python -m pytest` | Tambahkan formatter/type checker pilihan |
| PHP | `composer install` (wajib `composer.lock`) | `composer run-script test` | `composer validate --strict` |

Jika menggunakan stack lain atau multi-stack, tambahkan adapter CI dan dokumentasikan perintahnya. Jangan membuat manifest kosong hanya untuk mengaktifkan job.

## Validasi web dan aset
Untuk proyek web, CI root menjalankan pemeriksaan berikut secara otomatis:
- Parse HTML dengan parser HTML5 yang strict untuk mendeteksi markup malformed.
- Parse stylesheet CSS dan mendeteksi kesalahan sintaks.
- Periksa referensi lokal HTML (`src`, `href`, `poster`, `data`) dan CSS (`url(...)`) agar file aset yang dirujuk benar-benar ada.
- Periksa `srcset` dan tolak referensi yang keluar dari direktori proyek.
- Parse SVG sebagai XML dan tolak file sumber/aset kosong (kecuali `.gitkeep`).
- Abaikan URL eksternal dan data URI; jangan gunakan URL produksi sebagai pengganti fixture lokal.

Pemeriksaan ini memvalidasi sintaks dan keberadaan referensi aset, bukan kualitas visual, rendering lintas-browser, accessibility penuh, atau keamanan runtime. Tambahkan browser-based tests (misalnya Playwright) dalam proyek bila diperlukan; sediakan script test/build yang akan dipanggil adapter stack.

## Skenario minimum
- [ ] Alur sukses utama.
- [ ] Input tidak valid dan batas nilai.
- [ ] Error dari dependency/service eksternal.
- [ ] Akses tanpa izin untuk fitur yang dilindungi.
- [ ] Regression test untuk bug yang diperbaiki.
- [ ] Responsive dan accessibility untuk UI.
- [ ] Build dapat direproduksi.
- [ ] HTML, CSS, dan semua aset lokal yang dirujuk valid.

## Keamanan
- [ ] Manifest dan lockfile dependency dikomit.
- [ ] Fixture tidak memuat secret atau data pribadi.
- [ ] Test tidak mengakses layanan produksi.
- [ ] Validasi input dan otorisasi diuji.
- [ ] Hasil Gitleaks dan OSV-Scanner ditinjau.

## CI
Workflow root `.github/workflows/project-matrix.yml` menjalankan test aplikasi Node.js,
Python, atau PHP sesuai manifest, serta validasi HTML, CSS, dan referensi aset lokal
untuk setiap folder proyek di `projects/*`. Workflow repository root juga menjalankan
validasi dokumentasi, secret scanning, dan OSV-Scanner.

## Hasil verifikasi terakhir
| Tanggal | Commit | Pemeriksaan | Status | Catatan |
|---|---|---|---|---|
| [YYYY-MM-DD] | [SHA] | [perintah / job] | [PASS/FAIL/BLOCKED/NOT RUN] | [catatan] |

Jangan menyatakan PASS untuk pemeriksaan yang tidak dijalankan. Gunakan NOT RUN atau
BLOCKED dan jelaskan alasannya.
