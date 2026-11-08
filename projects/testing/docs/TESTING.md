# Strategi Testing — testing

> Lengkapi setelah memilih stack. CI mendeteksi Node.js, Python, dan PHP dari manifest root.

## Risiko dan cakupan
- Alur paling kritis: [isi]
- Dampak jika gagal: [isi]
- Data test: sintetis/dummy; jangan gunakan data produksi.

## Perintah standar
| Stack | Install | Test | Build / lint |
|---|---|---|---|
| Node.js | \`npm ci\` (wajib \`package-lock.json\`) | \`npm test\` (wajib script \`test\`) | \`npm run lint --if-present\`, \`npm run build --if-present\` |
| Python | \`pip install -e ".[test]"\` atau \`pip install -r requirements.txt\` | \`python -m pytest\` | Tambahkan formatter/type checker pilihan |
| PHP | \`composer install\` (wajib \`composer.lock\`) | \`composer run-script test\` | \`composer validate --strict\` |

Jika menggunakan stack lain atau multi-stack, tambahkan job CI yang sesuai dan dokumentasikan perintahnya. Jangan membuat manifest kosong hanya untuk mengaktifkan job.

## Skenario minimum
- [ ] Alur sukses utama.
- [ ] Input tidak valid dan batas nilai.
- [ ] Error dari dependency/service eksternal.
- [ ] Akses tanpa izin untuk fitur yang dilindungi.
- [ ] Regression test untuk bug yang diperbaiki.
- [ ] Responsive dan accessibility untuk UI.
- [ ] Build dapat direproduksi.

## Keamanan
- [ ] Manifest dan lockfile dependency dikomit.
- [ ] Fixture tidak memuat secret atau data pribadi.
- [ ] Test tidak mengakses layanan produksi.
- [ ] Validasi input dan otorisasi diuji.
- [ ] Hasil Gitleaks dan OSV-Scanner ditinjau.

## CI
Workflow \`.github/workflows/ci.yml\` menjalankan validasi struktur, JSON, Markdown,
whitespace, secret scanning, OSV-Scanner, serta test otomatis untuk Node.js, Python,
atau PHP bila manifest ditemukan.

## Hasil verifikasi terakhir
| Tanggal | Commit | Pemeriksaan | Status | Catatan |
|---|---|---|---|---|
| [YYYY-MM-DD] | [SHA] | [perintah / job] | [PASS/FAIL/BLOCKED/NOT RUN] | [catatan] |

Jangan menyatakan PASS untuk pemeriksaan yang tidak dijalankan. Gunakan NOT RUN atau
BLOCKED dan jelaskan alasannya.
