# proyek_ai

Repository pusat untuk dokumentasi, standar, template, dan pengembangan proyek dengan bantuan AI.

## Mulai dari sini

1. Baca [AGENTS.md](AGENTS.md) sebelum mengubah apa pun.
2. Baca [indeks proyek](docs/PROJECT_INDEX.md) untuk melihat ruang kerja dan template yang tersedia.
3. Untuk proyek baru, gunakan bootstrap resmi; jangan membuat struktur proyek secara manual.
4. Baca instruksi template dan lengkapi brief sebelum implementasi.
5. Periksa file dan riwayat terkait, jalankan pemeriksaan yang relevan, lalu ajukan perubahan melalui PR.

## Membuat proyek baru

Gunakan bootstrap otomatis (Python 3.10+):

    python scripts/bootstrap_project.py --name "Nama Proyek"

Folder proyek akan dibuat di projects/<slug-nama>/ dari template standar,
tanpa menimpa folder yang sudah ada. Panduan lengkap: [Bootstrap Proyek](docs/PROJECT_BOOTSTRAP.md).

## CI dan keamanan monorepo

CI dijalankan dari root repository. Workflow [project matrix](.github/workflows/project-matrix.yml)
hanya mendeteksi direktori proyek tingkat pertama di `projects/<slug>/` dengan nama
slug huruf kecil, angka, dan tanda hubung. Direktori tersembunyi pada tingkat tersebut
ditolak; direktori konfigurasi tersembunyi di dalam proyek diperbolehkan. Baca
[aturan struktur proyek](docs/PROJECT_STRUCTURE.md) sebelum menambah proyek.
Workflow menjalankan adapter Node.js, Python, atau PHP. OSV-Scanner memindai dependency
secara rekursif.

Baca [arsitektur CI monorepo](docs/MONOREPO_CI.md) untuk aturan penambahan stack,
manifest, lockfile, dan test.

## Struktur utama

- .github/: workflow CI, konfigurasi Dependabot, serta template pull request dan issue.
- .github/workflows/: validasi repository, orkestrasi test proyek, dan keamanan dependency.
- docs/: standar, workflow, indeks, keputusan, checklist kualitas, dan panduan bootstrap.
- projects/: ruang kerja proyek; saat ini sengaja kosong.
- templates/ai-project/: template standar untuk memulai proyek AI baru.
- archives/: direktori arsip historis yang saat ini hanya berisi README penjelas.

## Referensi DEKEKU

Arsip DEKEKU sebelumnya telah dikosongkan. Paket master tema, paket logo, dan
salinan Brand System tidak lagi disimpan di repository ini. `archives/` hanya
berisi README penjelas. Lokasi sumber kanonis DEKEKU Master Theme belum ditetapkan;
pemilik repository perlu memutuskan lokasinya sebelum aset tersebut digunakan kembali.

## Prinsip repository

- Satu lokasi kanonis untuk setiap source aktif.
- Arsip baseline tidak ditimpa atau diedit.
- Proyek baru dimulai dari template dan diisolasi di bawah projects/.
- Jangan mengarang data bisnis, harga, testimoni, kontak, atau klaim produk.
- Jangan menyimpan secret atau kredensial di Git.
