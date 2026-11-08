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

```bash
python scripts/bootstrap_project.py --name "Nama Proyek"
```

Folder proyek akan dibuat di `projects/<slug-nama>/` dari template standar,
tanpa menimpa folder yang sudah ada. Panduan lengkap: [Bootstrap Proyek](docs/PROJECT_BOOTSTRAP.md).

## Struktur utama
- `.github/workflows/`: validasi otomatis repository dan keamanan dependency.
- `docs/`: standar, workflow, indeks, keputusan, checklist kualitas, dan panduan bootstrap.
- `projects/`: ruang kerja proyek; saat ini sengaja kosong.
- `templates/ai-project/`: template standar untuk memulai proyek AI baru.
- `archives/`: paket sumber dan baseline historis yang dipertahankan tanpa modifikasi.

## Referensi DEKEKU
- [DEKEKU Brand System v1.1 — arsip baseline](archives/dekeku-brand-system-v1.1/README.md)
- [Paket master tema asli](archives/Master-tema-dekeku-v1.1.zip)
- [Paket logo resmi](archives/dekeku-logo-package.zip)

## Prinsip repository
- Satu lokasi kanonis untuk setiap source aktif.
- Arsip baseline tidak ditimpa atau diedit.
- Proyek baru dimulai dari template dan diisolasi di bawah `projects/`.
- Jangan mengarang data bisnis, harga, testimoni, kontak, atau klaim produk.
- Jangan menyimpan secret atau kredensial di Git.
