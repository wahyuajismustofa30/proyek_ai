# Context Store — Penyimpanan Konteks Percakapan

Aplikasi web statis untuk menyimpan, mengelola, dan mencari konteks percakapan.
Konteks disimpan di `localStorage` browser, sehingga persisten tanpa server atau database eksternal.

## Fitur

- Tambah, edit, dan hapus entri konteks.
- Pencarian teks bebas di seluruh konteks.
- Ekspor konteks ke file JSON.
- Impor konteks dari file JSON.
- Tampilan daftar dengan highlight pada kata kunci pencarian.

## Menjalankan lokal

Website bersifat statis dan tidak memerlukan build maupun dependency tambahan.

Dari direktori `projects/context-store/`, jalankan:

```sh
python -m http.server 8000
```

Lalu buka `http://localhost:8000`.

## Catatan

- Data disimpan di `localStorage` kunci `context-store-entries`.
- Browser harus mendukung `localStorage`.
- File JSON ekspor/impor tidak diverifikasi terhadap skema; pastikan Anda memercayai sumber file yang diimpor.
