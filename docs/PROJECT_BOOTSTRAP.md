# Bootstrap Proyek Otomatis

Gunakan script `scripts/bootstrap_project.py` untuk membuat proyek baru dari
`templates/ai-project/` tanpa menyalin folder secara manual.

## Persyaratan

- Python 3.10 atau lebih baru.
- Repository `proyek_ai` sudah di-clone.
- Jalankan perintah dari root repository atau gunakan path script yang benar.

## Penggunaan

Buat proyek dengan prompt interaktif:

```bash
python scripts/bootstrap_project.py
```

Buat proyek langsung dengan nama:

```bash
python scripts/bootstrap_project.py --name "DEKEKU Landing Page"
```

Perintah di atas membuat folder `projects/dekeku-landing-page/`. Untuk lokasi lain:

```bash
python scripts/bootstrap_project.py --name "API Internal" --output ../workspace
```

Periksa target terlebih dahulu tanpa membuat file:

```bash
python scripts/bootstrap_project.py --name "Proyek Percobaan" --dry-run
```

Lihat semua opsi:

```bash
python scripts/bootstrap_project.py --help
```

## Yang dilakukan script

1. Mengubah nama menjadi slug folder yang aman (huruf kecil, angka, dan tanda hubung).
2. Menyalin seluruh template, termasuk instruksi AI, dokumen, workflow CI, pengujian, dan konfigurasi keamanan.
3. Mengganti placeholder nama proyek pada file teks UTF-8.
4. Menolak nama kosong, template yang tidak ditemukan, serta folder tujuan yang sudah ada.
5. Tidak menimpa file/folder yang ada dan tidak menjalankan perintah Git, install dependency, atau deployment.

Script tidak membuat repository Git terpisah. Proyek baru tetap berada di dalam repository utama
agar mengikuti struktur dan tata kelola `proyek_ai`.

## Setelah bootstrap

- Lengkapi `README.md` dan `docs/PROJECT_BRIEF.md`.
- Tinjau `AGENTS.md`, arsitektur, task, keputusan, dan strategi testing.
- Pilih stack; tambahkan manifest dan lockfile yang sesuai.
- Pastikan perintah test cocok dengan workflow CI.
- Periksa secret, dependency, dan perubahan sebelum membuat PR.
- Tambahkan entri ke `docs/PROJECT_INDEX.md` setelah proyek benar-benar diterima sebagai proyek aktif.

## Pengujian bootstrap

Jalankan:

```bash
python -m unittest scripts.tests.test_bootstrap_project -v
```

Tes mencakup slug, penyalinan dan penggantian placeholder, pencegahan overwrite,
validasi nama, dan mode dry-run.
