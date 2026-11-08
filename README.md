# proyek_ai

Repository pusat untuk dokumentasi, source code, aset, dan pengembangan proyek dengan bantuan AI.

## Mulai dari sini
1. Baca [AGENTS.md](AGENTS.md) sebelum mengubah apa pun.
2. Baca [indeks proyek](docs/PROJECT_INDEX.md) dan pilih proyek yang diminta.
3. Baca README serta instruksi lokal proyek tersebut.
4. Periksa file dan riwayat terkait sebelum mengedit.
5. Jalankan pemeriksaan yang relevan dan laporkan hasilnya.

## Membuat proyek baru

Gunakan bootstrap otomatis (Python 3.10+):

```bash
python scripts/bootstrap_project.py --name "Nama Proyek"
```

Folder proyek akan dibuat di `projects/<slug-nama>/` dari template standar,
tanpa menimpa folder yang sudah ada. Panduan lengkap: [Bootstrap Proyek](docs/PROJECT_BOOTSTRAP.md).

## Struktur utama
- `.github/workflows/`: validasi otomatis repository.
- `docs/`: standar, workflow, indeks, keputusan, checklist kualitas, [kebijakan Dependabot](docs/DEPENDABOT.md), [validasi Markdown](docs/MARKDOWN_VALIDATION.md), dan [panduan bootstrap](docs/PROJECT_BOOTSTRAP.md).
- `projects/`: seluruh proyek aktif, masing-masing terisolasi.
- `templates/ai-project/`: template untuk memulai proyek AI baru.
- `archives/`: paket arsip asli yang tidak diedit.

## Proyek DEKEKU
- [Ringkasan DEKEKU](projects/dekeku/README.md)
- [Brand System](projects/dekeku/brand-system/README.md)
- [Business Website](projects/dekeku/business-website/README.md)
- [Online Invitation](projects/dekeku/online-invitation/README.md)

## Prinsip repository
- Satu lokasi kanonis untuk setiap source.
- Arsip baseline tidak ditimpa.
- Website bisnis dan undangan online berbagi identitas brand, tetapi diperlakukan sebagai produk dengan kebutuhan UX berbeda.
- Jangan mengarang data bisnis, harga, testimoni, kontak, atau klaim produk.
- Jangan menyimpan secret atau kredensial di Git.
