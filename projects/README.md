# Ruang Kerja Proyek

Folder ini sengaja tidak berisi proyek aktif.

`projects/` hanya berisi direktori proyek aktif tingkat pertama dengan nama slug
huruf kecil, angka, dan tanda hubung (contoh: `web-app`). Jangan membuat direktori
proyek tersembunyi seperti `.draft/`, `.archive/`, atau `.internal/` di sini; direktori
tersebut ditolak oleh discovery CI. File biasa seperti `.gitkeep` bukan proyek dan
diabaikan. Subdirektori konfigurasi tersembunyi di dalam proyek, seperti
`projects/web-app/.github/` atau `projects/web-app/.config/`, diperbolehkan.

Setiap proyek dimulai dari template resmi dan memiliki `README.md`, `AGENTS.md`,
`.project-meta.json`, `docs/`, `src/`, `tests/`, dan `assets/`. Subfolder proyek tidak
menjadi proyek CI tersendiri. Baca [aturan struktur proyek](../docs/PROJECT_STRUCTURE.md).

Buat proyek baru setelah sistem inti repository dan brief proyek siap:

```bash
python scripts/bootstrap_project.py --name "Nama Proyek"
```

Baca [panduan bootstrap](../docs/PROJECT_BOOTSTRAP.md) dan [indeks proyek](../docs/PROJECT_INDEX.md)
sebelum memulai. Jangan menambahkan proyek secara manual atau menggunakan folder ini
sebagai tempat arsip.
