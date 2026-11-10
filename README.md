# proyek_ai

Repository pusat untuk menerima, mengelola, dan mengembangkan proyek dengan bantuan AI. Source dapat disiapkan di luar repository, termasuk melalui Termux, lalu diunggah ke projects/<slug>/.

## Mulai dari sini

1. Baca AGENTS.md sebelum mengubah repository.
2. Lihat docs/PROJECT_INDEX.md untuk menemukan proyek yang tersedia.
3. Siapkan atau unggah proyek ke projects/<slug>/. Tidak ada template atau bootstrap wajib.
4. Minta AI mempelajari dokumentasi, konfigurasi, dan source yang benar-benar tersedia.
5. Kembangkan pada branch terpisah, jalankan validasi relevan, lalu ajukan pull request.

## Sinkronisasi GitHub dari Termux

Gunakan docs/GITHUB_SYNC_TERMUX.md untuk alur branch, review, commit, dan push yang aman. Tool tidak push langsung ke main atau force-push. Jika isi projects/ berubah, indeks proyek diperbarui otomatis sebelum staging.

## Struktur proyek

Setiap proyek berada satu tingkat di bawah projects/ dengan nama slug huruf kecil, angka, dan tanda hubung. Struktur internal fleksibel; tidak ada README, metadata, manifest, atau susunan folder tertentu yang wajib.

Indeks dibuat dari direktori aktual oleh scripts/update_project_index.py. Jalankan manual: python3 scripts/update_project_index.py --write. CI memeriksa kesesuaiannya dengan --check.

Proyek dengan stack yang dikenali mendapat adapter test Node.js, Python, PHP, atau static website. Proyek dengan teknologi lain tetap ditemukan, tetapi memerlukan pemeriksaan manual atau adapter CI sebelum test aplikasi dapat dinyatakan otomatis.

## CI dan keamanan

CI menjalankan validasi repository, adapter test yang tersedia, smoke test website statis, validasi HTML/CSS/aset, Gitleaks, dan OSV-Scanner. Baca docs/MONOREPO_CI.md dan docs/PROJECT_STRUCTURE.md.

## Struktur utama

- .github/: workflow CI, Dependabot, template issue dan pull request.
- docs/: standar, workflow, indeks, keputusan, checklist kualitas, dan panduan.
- projects/: source proyek dengan struktur internal sesuai kebutuhan masing-masing.
- scripts/: discovery, pembaruan indeks, validasi, dan GitHub Sync Termux.
- archives/: arsip historis yang saat ini hanya berisi README penjelas.

## Referensi DEKEKU

Arsip DEKEKU sebelumnya telah dikosongkan. Paket master tema, paket logo, dan salinan Brand System tidak lagi disimpan di repository ini. Lokasi sumber kanonis DEKEKU Master Theme belum ditetapkan.

## Prinsip repository

- Satu lokasi kanonis untuk setiap source aktif.
- Arsip baseline tidak ditimpa atau diedit.
- Jangan mengarang data bisnis, harga, testimoni, kontak, atau klaim produk.
- Jangan menyimpan secret atau kredensial di Git.

## Lisensi

Repository ini dilisensikan berdasarkan GNU General Public License v3.0 only (GPL-3.0-only). Penggunaan, modifikasi, dan distribusi harus mematuhi ketentuan GPL-3.0. Komponen, model AI, dataset, dan aset pihak ketiga dapat memiliki ketentuan lisensi tersendiri.
