# Standar Repository dan Pengembangan

## Struktur
- Folder root hanya untuk entrypoint, instruksi global, konfigurasi repository, dokumentasi bersama, proyek, template, dan arsip.
- Setiap proyek memiliki README sendiri.
- Proyek DEKEKU dipisahkan menjadi brand-system, business-website, dan online-invitation.
- Hindari menyimpan source yang sama di beberapa lokasi aktif. Tentukan satu lokasi kanonis.
- Folder arsip bersifat immutable: jangan diedit atau ditimpa.

## Penamaan
- Gunakan nama folder dan file huruf kecil dengan kebab-case bila memungkinkan.
- Pertahankan nama file dari paket baseline ketika perubahan nama dapat merusak referensi.
- Gunakan versi semantik `MAJOR.MINOR.PATCH` untuk rilis aplikasi/library jika sesuai.
- Jangan mengubah label versi baseline tanpa bukti dan persetujuan.

## Kode dan dependency
- Ikuti formatter, linter, runtime, dan pola dependency yang sudah dipakai proyek.
- Jangan menambah dependency hanya untuk tugas sederhana.
- Kunci versi dependency melalui lockfile bila ekosistem mendukungnya.
- Jangan commit hasil build kecuali memang menjadi artefak distribusi yang diperlukan.

## Git dan perubahan
- Gunakan commit yang menjelaskan maksud perubahan.
- Satu commit sebaiknya memiliki satu tujuan yang jelas.
- Periksa diff dan status file sebelum commit.
- Jangan force-push atau menghapus riwayat tanpa instruksi eksplisit.

## Keamanan
- Jangan commit password, token, private key, cookie, atau file `.env` nyata.
- Sediakan `.env.example` dengan nilai dummy yang jelas.
- Validasi input dan batasi akses sesuai kebutuhan aplikasi.
- Tinjau dependency dan permission sebelum deployment.

## Dokumentasi
- README menjelaskan tujuan, status, cara menjalankan, dan konteks penting.
- CHANGELOG mencatat perubahan yang berdampak pada pengguna atau developer.
- DECISIONS mencatat keputusan arsitektur jangka panjang.
- Dokumentasi harus membedakan fakta, asumsi, placeholder, dan hal yang belum diverifikasi.

## Testing
- Setiap proyek wajib memiliki `docs/TESTING.md` dan direktori `tests/` atau alternatif terdokumentasi untuk proyek non-kode.
- Ikuti [Standar Testing](TESTING_STANDARDS.md) untuk lapisan test, data, CI, dan pelaporan.
- Strategi spesifik proyek harus menjelaskan skenario kritis, perintah test, dan pengecualian.
