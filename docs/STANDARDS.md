# Standar Repository

## Prinsip umum

- Utamakan perubahan kecil, terarah, dan dapat ditinjau.
- Jangan mengubah branch main secara langsung; gunakan branch dan pull request.
- Jangan menyimpan secret, token, password, atau data pribadi sensitif.
- Jangan mengubah arsip historis.
- Jalankan validasi relevan sebelum mengajukan pull request.

## Pengelolaan proyek

- projects/ adalah ruang kerja proyek; indeks dibuat otomatis dari direktori aktual.
- Setiap proyek berada di projects/<slug>/ dan menggunakan nama direktori yang konsisten.
- Struktur internal fleksibel; tidak ada template, bootstrap, metadata, README, atau susunan direktori yang diwajibkan.
- Baca dokumentasi dan instruksi yang tersedia. Jika tidak ada, pahami kebutuhan dari source, konfigurasi, dan konteks pengguna.
- Pisahkan source setiap proyek.
- Teknologi tanpa adapter CI tetap dapat disimpan dan ditemukan; jangan mengklaim telah diuji otomatis.
- archives/ hanya mempertahankan archives/README.md; lihat docs/DECISIONS.md.

## Kualitas perubahan

- Perbarui dokumentasi saat struktur, workflow, atau perilaku tooling berubah.
- Tambahkan atau perbarui pengujian untuk perubahan script.
- Pastikan link internal, format Markdown, JSON, Python, dan whitespace lolos CI.
