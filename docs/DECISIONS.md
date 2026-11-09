# Catatan Keputusan

## Struktur proyek

- Repository memusatkan standar, dokumentasi, template, tooling, dan proyek internal yang dipelihara.
- `projects/preview/` dan `projects/testing/` merupakan proyek aktif yang terdaftar di `docs/PROJECT_INDEX.md`.
- Root `projects/` hanya menyimpan `README.md` dan direktori proyek; fixture, cache, dependency, log, file sementara, hasil build, serta artefak harus berada di luar ruang kerja proyek.
- Proyek baru dibuat secara eksplisit dari `templates/ai-project/` menggunakan `scripts/bootstrap_project.py`; output tidak boleh bersarang di dalam proyek yang sudah ada.

## Arsip DEKEKU

- Isi direktori `archives/` telah dikosongkan berdasarkan keputusan pemeliharaan repository.
- Hanya `archives/README.md` yang dipertahankan; paket tema, paket logo, dan salinan Brand System lama tidak lagi tersedia di repository.
- Pengembangan DEKEKU berikutnya harus menggunakan aset sumber yang disetujui dan ditempatkan pada proyek aktif; jangan mengasumsikan file arsip lama masih ada.

## Sumber kanonis DEKEKU Master Theme

- Lokasi sumber kanonis DEKEKU Master Theme **BELUM DITETAPKAN**.
- Repository ini tidak menyimpan aset DEKEKU lama; `archives/` hanya berisi README penjelas.
- Pemilik repository harus memutuskan dan menyetujui lokasi sumber kanonis sebelum pekerjaan DEKEKU berikutnya bergantung padanya.

## Lisensi repository

- Repository menggunakan **GNU General Public License v3.0 only (GPL-3.0-only)**.
- Tujuan lisensi: memungkinkan penggunaan, pembelajaran, modifikasi, dan distribusi,
  termasuk penggunaan komersial, sambil mempertahankan kewajiban copyleft untuk
  karya turunan yang didistribusikan.
- Distribusi dalam bentuk non-source harus disertai atau menyediakan Corresponding
  Source sesuai ketentuan GPL-3.0.
- Penggunaan atau modifikasi untuk kebutuhan pribadi/internal tanpa distribusi
  tidak dengan sendirinya mewajibkan publikasi perubahan.
- Komponen pihak ketiga, model AI, dataset, dan aset eksternal tetap mengikuti
  lisensi atau ketentuan masing-masing; lisensi repository tidak otomatis
  melisensikan materi yang haknya tidak dimiliki kontributor.
