# Standar Repository

## Prinsip umum
- Utamakan perubahan kecil, terarah, dan dapat ditinjau.
- Jangan mengubah branch `main` secara langsung; gunakan branch dan pull request.
- Jangan menyimpan secret, token, password, atau data pribadi sensitif.
- Jangan mengubah arsip historis.
- Jalankan validasi yang relevan sebelum mengajukan pull request.

## Pengelolaan proyek
- Folder `projects/` adalah ruang kerja proyek aktif dan saat ini sengaja kosong.
- Proyek baru wajib dibuat dari `templates/ai-project/` melalui bootstrap resmi.
- Setiap proyek harus memiliki brief, instruksi AI, dokumentasi keputusan, dan strategi pengujian.
- Pisahkan source setiap proyek; jangan menggabungkan aset atau konfigurasi tanpa alasan yang terdokumentasi.
- Direktori `archives/` saat ini hanya mempertahankan `archives/README.md`; jangan menganggap baseline DEKEKU lama masih tersedia di repository.

## Kualitas perubahan
- Perbarui dokumentasi saat struktur, workflow, atau perilaku tooling berubah.
- Tambahkan atau perbarui pengujian untuk perubahan script.
- Pastikan link internal, format Markdown, JSON, Python, dan whitespace lolos pemeriksaan CI.
