# CI terpusat untuk monorepo

## Workflow

| Workflow | Tanggung jawab |
|---|---|
| .github/workflows/validate.yml | YAML/schema Dependabot, JSON, kompilasi Python, unit test tooling, validasi katalog dan kesegaran indeks, Markdown, link internal, whitespace |
| .github/workflows/project-matrix.yml | Discovery proyek tingkat pertama, pemeriksaan aplikasi yang tersedia, smoke test website statis, validasi HTML/CSS/aset sesuai adapter |
| .github/workflows/dependency-security.yml | OSV-Scanner untuk manifest dan lockfile |

Workflow berjalan pada push ke main dan pemicu lain sesuai konfigurasi masing-masing file.

## Kebijakan main

Repository menggunakan kebijakan Direct Commit to Main: commit langsung ke main diperbolehkan dan Pull Request bersifat opsional, kecuali pengguna meminta alur berbeda. CI berjalan setelah push; periksa hasil Actions dan tangani kegagalan yang ditemukan.

## Discovery, katalog, dan indeks

Ketiganya memiliki fungsi berbeda dan tidak boleh disamakan:

- scripts/discover_projects.py menemukan proyek tingkat pertama untuk matrix CI. Saat ini discovery tersebut belum otomatis menemukan proyek di dalam kategori, seperti projects/whatsapp/gowa-gemini-bridge/.
- docs/project-catalog.json adalah daftar kurasi proyek, tooling, dan kategori. Katalog mendukung path bertingkat dan memvalidasi bahwa direktori terdaftar benar-benar ada.
- scripts/update_project_index.py merender katalog menjadi docs/PROJECT_INDEX.md. Indeks bukan bukti bahwa proyek telah dijalankan atau diuji oleh matrix CI.

Perbarui indeks setelah mengubah katalog:

```sh
python3 scripts/update_project_index.py --write
python3 scripts/update_project_index.py --check
```

## Status pemeriksaan

- **PASS:** pemeriksaan benar-benar dijalankan dan berhasil.
- **NOTICE:** pemeriksaan tidak tersedia atau tidak dikonfigurasi; bukan hasil tes lulus.
- **FAIL:** kesalahan nyata, manifest tidak valid, instalasi yang diperlukan gagal, atau tes gagal.
- **NOT RUN:** pemeriksaan belum dijalankan.
