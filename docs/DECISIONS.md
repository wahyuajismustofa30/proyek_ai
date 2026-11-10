# Catatan Keputusan

## Pengelolaan proyek

- Repository berfungsi sebagai tempat menerima, mengelola, dan mengembangkan proyek dengan bantuan AI; source dapat disiapkan di luar repository, termasuk melalui Termux.
- Proyek aktif disimpan langsung di bawah projects/<slug>/.
- Struktur internal fleksibel. Tidak ada template proyek, bootstrap, metadata, README, atau struktur folder tertentu yang diwajibkan.
- docs/PROJECT_INDEX.md dihasilkan dari direktori aktual melalui scripts/update_project_index.py; sinkronisasi Termux memperbarui indeks ketika projects/ berubah.
- Discovery CI hanya memerlukan direktori tingkat pertama dengan nama slug valid. Stack tanpa adapter tetap ditemukan dan tidak diblokir hanya karena tidak dikenali.
- Issue/PR templates, validasi keamanan, pemindaian dependency, dan pemeriksaan kualitas repository tetap dipertahankan.

## Arsip DEKEKU

- Isi archives/ telah dikosongkan berdasarkan keputusan pemeliharaan repository.
- Hanya archives/README.md yang dipertahankan; paket tema, paket logo, dan salinan Brand System lama tidak lagi tersedia.
- Pengembangan DEKEKU berikutnya harus menggunakan aset sumber yang disetujui; jangan mengasumsikan file arsip lama masih ada.

## Sumber kanonis DEKEKU Master Theme

- Lokasi sumber kanonis DEKEKU Master Theme BELUM DITETAPKAN.
- Repository ini tidak menyimpan aset DEKEKU lama; archives/ hanya berisi README penjelas.
- Pemilik repository harus menyetujui lokasi sumber kanonis sebelum pekerjaan DEKEKU berikutnya bergantung padanya.

## Lisensi repository

- Repository menggunakan GNU General Public License v3.0 only (GPL-3.0-only).
- Distribusi turunan harus mematuhi kewajiban copyleft dan menyediakan Corresponding Source sesuai GPL-3.0.
- Penggunaan atau modifikasi internal tanpa distribusi tidak dengan sendirinya mewajibkan publikasi perubahan.
- Komponen pihak ketiga, model AI, dataset, dan aset eksternal mengikuti lisensi masing-masing.
