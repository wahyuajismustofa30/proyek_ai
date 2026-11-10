# Aturan Direktori dan Struktur Proyek

Dokumen ini menjelaskan batas minimal monorepo. Struktur internal setiap proyek fleksibel dan mengikuti teknologi serta kebutuhannya.

## Batas proyek

- Setiap proyek berada satu tingkat langsung di bawah projects/<slug>/.
- Nama direktori menggunakan slug huruf kecil ASCII, angka, dan tanda hubung: [a-z0-9]+(?:-[a-z0-9]+)*.
- Contoh valid: website, web-app, api-v2, dekeku.
- Symlink langsung di dalam projects/ ditolak agar discovery CI tetap aman.
- Hanya projects/README.md yang boleh menjadi file langsung di root projects/; proyek lainnya berupa direktori.

## Struktur internal fleksibel

Tidak ada scaffold atau susunan folder wajib. Proyek boleh menggunakan struktur sesuai stack dan kebutuhan masing-masing: website statis, aplikasi Node.js/Python/PHP/Go/Rust, proyek desain, aset, dokumentasi, konfigurasi, atau gabungan beberapa stack.

Tidak diwajibkan memiliki README.md, AGENTS.md, .project-meta.json, src/, tests/, docs/, assets/, manifest, lockfile, atau file konfigurasi tertentu.

README dan dokumentasi disarankan. Jika tersedia, AI membacanya sebagai konteks awal. Jika tidak tersedia, pahami proyek dari struktur, konfigurasi, source, dan artefak yang benar-benar ada; jangan mengarang informasi.

## Discovery dan validasi

scripts/discover_projects.py menemukan direktori proyek tingkat pertama. Manifest yang dikenali memperoleh adapter CI. Proyek dengan teknologi yang belum memiliki adapter tetap terdaftar dan tidak diblokir hanya karena tidak dikenali. Status ini berarti pengujian aplikasi otomatis belum tersedia.

Validasi HTML, CSS, aset lokal, secret, dan dependency tetap dijalankan workflow repository sesuai cakupannya. Jangan menyimpan credential, private key, atau data sensitif di Git.

## Indeks proyek

docs/PROJECT_INDEX.md dihasilkan dari direktori aktual oleh scripts/update_project_index.py. Jangan mengedit tabel indeks secara manual.

- Sinkronisasi Termux memperbarui indeks otomatis saat ada perubahan di projects/.
- Untuk alur lain, jalankan python3 scripts/update_project_index.py --write.
- CI menjalankan --check untuk mendeteksi indeks yang belum diperbarui.

## Alur kerja

1. Siapkan proyek melalui workflow lokal pilihan Anda, termasuk Termux.
2. Unggah sebagai projects/<slug>/.
3. Biarkan discovery dan pembaruan indeks mengidentifikasi proyek.
4. Minta AI mempelajari dokumentasi, konfigurasi, dan source yang tersedia.
5. Kembangkan pada branch terpisah dan ajukan pull request.

Template issue dan pull request di root repository tetap digunakan; penghapusannya tidak termasuk kebijakan ini.
