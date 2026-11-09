# Arsitektur — Testing Web Page Lab

## 1. Gambaran sistem

Aplikasi adalah situs statis tanpa server aplikasi. Browser memuat HTML, CSS, JavaScript, dan SVG lokal dari direktori `src/` serta `assets/`.

## 2. Stack dan versi

| Komponen | Teknologi | Versi | Alasan |
|---|---|---|---|
| Markup | HTML | HTML Living Standard | Struktur halaman semantik |
| Styling | CSS | CSS modern | Layout responsif tanpa framework |
| Browser logic | JavaScript | ES modules | Interaksi ringan tanpa dependency |
| Test runtime | Node.js | 22+ | Built-in test runner dan tanpa dependency |

## 3. Struktur direktori

```text
projects/testing/
├── assets/testing-mark.svg
├── docs/
├── src/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/web-page.test.js
├── package.json
└── package-lock.json
```

## 4. Komponen

- `index.html`: konten dan struktur semantik.
- `styles.css`: layout, tipografi, warna, dan breakpoint.
- `app.js`: navigasi mobile dan simulasi validasi form.
- `web-page.test.js`: kontrak halaman dan helper email.

## 5. Alur request

Browser meminta `index.html`, kemudian memuat stylesheet, JavaScript module, dan SVG lokal. Form tidak melakukan request jaringan.

## 6. Data storage

Tidak ada database atau penyimpanan persisten.

## 7. Environment dan deployment

Development: `python -m http.server 8080 --directory src`.

Production: belum ditentukan; jangan deploy tanpa keputusan eksplisit.

## 8. Keamanan dan risiko

- Tidak ada endpoint server atau secret.
- Validasi email client-side hanya untuk demo.
- Jika kelak ditambahkan backend, validasi dan keamanan wajib diterapkan di sisi server.
