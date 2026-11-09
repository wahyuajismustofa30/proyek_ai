# Ruang Kerja Proyek

Folder ini hanya digunakan untuk proyek internal yang benar-benar dipelihara di repository.
Saat ini terdapat dua proyek aktif: `preview/` dan `testing/`.

Di tingkat root `projects/`, hanya README ini yang boleh disimpan selain direktori
proyek. Jangan menaruh fixture, arsip, backup, file sementara, cache, dependency,
log, hasil build, laporan, atau artefak pengujian di sini. Gunakan direktori
sementara sistem/CI untuk kebutuhan pengujian dan output yang dapat dibuat ulang.

Setiap proyek aktif berada tepat satu tingkat di bawah `projects/` dan memakai
nama slug huruf kecil, angka, serta tanda hubung. Jangan membuat direktori proyek
tersembunyi seperti `.draft/`, `.archive/`, atau `.internal/`. Direktori
konfigurasi tersembunyi di dalam proyek, seperti `.github/` atau `.config/`,
tetap diperbolehkan.

Setiap proyek dimulai dari template resmi dan mengikuti [aturan struktur proyek](../docs/PROJECT_STRUCTURE.md).
Buat proyek baru secara eksplisit melalui bootstrap:

```bash
python scripts/bootstrap_project.py --name "Nama Proyek"
```

Bootstrap menolak output yang bersarang di dalam proyek lain. Untuk fixture CI,
gunakan direktori sementara di luar repository; script fixture juga menolak lokasi
output di dalam repository. Baca [panduan bootstrap](../docs/PROJECT_BOOTSTRAP.md)
dan [indeks proyek](../docs/PROJECT_INDEX.md) sebelum memulai.
