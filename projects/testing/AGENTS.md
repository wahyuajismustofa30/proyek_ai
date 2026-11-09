# Konteks Khusus Proyek — Testing Web Page Lab

Berlaku sebagai tambahan terhadap instruksi induk di `/AGENTS.md`. Aturan umum tentang alur kerja, Git, pull request, keamanan, pengujian, dan pelaporan diwarisi dari instruksi induk; jangan menyalinnya ke sini.

## Stack dan batas teknis

- Proyek ini adalah demo website statis menggunakan HTML, CSS, dan JavaScript vanilla.
- Pertahankan stack tanpa framework kecuali ada keputusan baru yang disetujui dan didokumentasikan.
- Node.js 22+ dan test runner bawaan Node digunakan untuk pengujian; jalankan `npm test`.
- Document root website adalah direktori `src/`; untuk pemeriksaan lokal gunakan:
  `python -m http.server 8080 --directory src`.
- Tidak ada backend, API, database, autentikasi, atau pengiriman form ke server. Jangan menambahkan perilaku tersebut tanpa perubahan brief dan persetujuan.
- Form hanya boleh melakukan simulasi/validasi sisi klien. Jangan mengirim atau menyimpan data pengguna.
- Jangan menambahkan dependency bila fitur bawaan Node.js/browser sudah cukup.

## Dokumentasi proyek

Untuk memahami kebutuhan dan keputusan proyek, gunakan dokumen berikut sesuai relevansi:
- `README.md`
- `docs/PROJECT_BRIEF.md`
- `docs/ARCHITECTURE.md`
- `docs/TASKS.md`
- `docs/TESTING.md`
- `docs/DECISIONS.md`
- `docs/CHANGELOG.md`

## Batas verifikasi

- Tes DOM berbasis stub bukan pengganti browser automation, visual regression, atau audit aksesibilitas penuh.
- Pemeriksaan manual keyboard, screen reader, dan tampilan desktop/mobile tetap perlu dicatat sebagai belum dilakukan sampai benar-benar dijalankan.
- Jangan mengklaim website siap produksi atau telah diaudit aksesibilitas hanya berdasarkan `npm test`.
