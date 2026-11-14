# Validasi Markdown

Repository menggunakan `markdown-it-py` sebagai parser Markdown untuk memeriksa tautan internal dan anchor heading. Ini menggantikan ekstraksi tautan berbasis regular expression yang mudah keliru pada sintaks bertingkat atau format tautan kompleks.

## Cara menjalankan

Pasang dependency pemeriksaan CI, lalu jalankan:

```bash
python -m pip install -r requirements-ci.txt
python -m unittest discover -s scripts/tests -v
python scripts/check_internal_links.py
```

## Yang diperiksa

- Tautan Markdown inline dan reference-style.
- Tujuan gambar Markdown.
- URL relatif, path root repository, query, fragment, dan path dengan karakter URL-encoded.
- Link ke direktori yang memiliki `README.md` atau `index.md`.
- Anchor heading Markdown, termasuk heading duplikat dengan suffix angka.
- Anchor HTML eksplisit melalui atribut `id` dan `name`.
- Link dan image di dalam fenced code block atau inline code tidak dianggap sebagai tautan aktif.
- Target yang keluar dari root repository ditolak.

URL eksternal dengan skema seperti `https:`, `mailto:`, atau URL protokol-relatif tidak diperiksa ketersediaannya. Pemeriksaan ini juga tidak mengunduh halaman eksternal, memeriksa anchor di halaman web eksternal, atau memvalidasi anchor dalam file HTML. Tujuannya adalah memastikan referensi lokal repository konsisten tanpa bergantung pada layanan jaringan.

## Dependency

Dependency parser dikunci di `requirements-ci.txt`. Dependabot memantau ecosystem `pip` dari root repository. Perubahan versi parser harus melewati unit test, validasi seluruh dokumentasi, dan workflow CI.

## Pengujian

Unit test mencakup tautan inline/reference, gambar, kode yang harus diabaikan, path ber-encoding dan tanda kurung, anchor heading duplikat, anchor HTML, direktori README, dan pencegahan path traversal keluar repository.
