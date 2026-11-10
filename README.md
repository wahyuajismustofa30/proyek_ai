# proyek_ai

Repository pusat untuk menerima, mengelola, dan mengembangkan proyek dengan bantuan AI. Source dapat disiapkan di luar repository, termasuk melalui Termux, lalu diunggah ke `projects/<slug>/`.

## Mulai

1. Baca [AGENTS.md](AGENTS.md).
2. Lihat [indeks proyek](docs/PROJECT_INDEX.md).
3. Tambahkan atau unggah source ke `projects/<slug>/`.
4. Minta AI mempelajari file dan dokumentasi yang benar-benar tersedia.
5. Kembangkan pada branch terpisah, jalankan validasi relevan, lalu ajukan Pull Request.

Tidak ada template, bootstrap, README, manifest, lockfile, atau struktur internal proyek yang wajib.

## Sinkronisasi Termux

Gunakan [panduan GitHub Sync](docs/GITHUB_SYNC_TERMUX.md). Tool membuat branch fitur bila diperlukan, mempertahankan perubahan pengguna, memperbarui indeks saat `projects/` berubah, dan tidak melakukan force-push atau push langsung ke `main`.

## Indeks proyek

Indeks dihasilkan dari direktori aktual oleh `scripts/update_project_index.py`.

```sh
python3 scripts/update_project_index.py --write
python3 scripts/update_project_index.py --check
```

Untuk upload melalui GitHub atau alur selain Termux, jalankan generator sebelum mengajukan PR. CI memeriksa kesegaran indeks.

## CI dan keamanan

CI memvalidasi repository, mendeteksi proyek, menjalankan pemeriksaan yang tersedia, memeriksa HTML/CSS/aset lokal, serta memindai secret dan dependency. Pengujian aplikasi yang belum dikonfigurasi menghasilkan NOTICE, bukan dianggap lulus atau otomatis menggagalkan CI. Kesalahan manifest, instalasi yang dikonfigurasi, dan tes yang benar-benar gagal tetap menggagalkan CI.

Baca [arsitektur CI](docs/MONOREPO_CI.md), [aturan struktur proyek](docs/PROJECT_STRUCTURE.md), dan [standar pengujian](docs/TESTING_STANDARDS.md).

## Struktur utama

- `.github/`: workflow, Dependabot, template issue dan pull request.
- `docs/`: aturan, panduan, indeks, dan keputusan.
- `projects/`: source proyek; struktur internal fleksibel.
- `scripts/`: discovery, indeks, validasi, dan sinkronisasi Termux.
- `archives/`: arsip historis.

## Prinsip

- Satu lokasi kanonis untuk setiap source aktif.
- Jangan mengubah proyek lain tanpa permintaan.
- Jangan menyimpan secret atau kredensial di Git.
- Jangan mengarang data bisnis, testimoni, kontak, statistik, atau klaim.

## Lisensi

Repository ini menggunakan GNU General Public License v3.0 only (GPL-3.0-only). Komponen, model AI, dataset, dan aset pihak ketiga dapat memiliki ketentuan lisensi tersendiri.
