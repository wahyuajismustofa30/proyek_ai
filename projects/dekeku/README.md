# DEKEKU — Static Website & Design Reference

Repository ini menyimpan aset brand dan halaman referensi desain DEKEKU.

## Struktur

```
.
├── index.html
├── pages/reference/index.html
├── assets/
│   ├── icons/
│   └── logos/
├── css/
│   ├── main.css
│   └── tokens.css
├── js/main.js
├── docs/head-snippet.html
├── manifest.webmanifest
└── manifest.webmanifest
```

## Menjalankan lokal

Website ini statis dan tidak memerlukan build atau dependency:
- buka `index.html` langsung, atau
- jalankan server statis dari direktori ini (contoh: `python -m http.server 8000`).

## Halaman

- **Beranda:** `index.html`
- **Referensi tema:** `pages/reference/index.html`

## Aset

- `assets/logos/`: logo horizontal/compact, varian putih.
- `assets/icons/`: ikon, favicon, dan ikon PWA.
- `manifest.webmanifest`: metadata PWA.
- `docs/head-snippet.html`: contoh metadata head untuk integrasi.

Path aset pada halaman referensi menggunakan path relatif sesuai struktur folder.
