# DEKEKU Icon Assets (perbaikan)

Dibuat ulang dari paket logo `dekeku_logo_package.zip`.

## Isi

| File | Fungsi |
|---|---|
| `dekeku-icon.svg`, `dekeku-icon-white.svg` | Icon vektor asli (hitam `#0C0C0C` / putih), menggantikan `dekeku-mascot.svg` (icon dan maskot memakai gambar yang sama) |
| `dekeku-logo-horizontal(.svg / -white.svg)` | Logo horizontal dengan tagline, vektor asli |
| `dekeku-logo-compact(.svg / -white.svg)` | Icon + wordmark tanpa tagline, untuk navbar dan lebar < 200 px |
| `favicon.svg` | Favicon adaptif (hitam di tema terang, putih di tema gelap), tanpa kotak piksel |
| `favicon.ico` | Multi-ukuran 16/32/48 px, kotak membulat gelap + icon putih, tanpa kotak piksel |
| `favicon-16/32/48.png` | Versi PNG favicon |
| `apple-touch-icon.png` | 180 px, tanpa transparansi |
| `dekeku-icon-dark-192/512.png`, `dekeku-icon-light-512.png` | Icon dengan background (glyph 70%, tengah) |
| `dekeku-icon-maskable-512.png` | PWA maskable (glyph di dalam safe zone) |
| `dekeku-icon-transparent-512.png`, `dekeku-icon-white-transparent-512.png` | Icon transparan, margin 8% |
| `site.webmanifest`, `head-snippet.html` | Konfigurasi siap tempel |

## Catatan

- SVG dihasilkan dengan trace dari PNG resolusi tertinggi (kecocokan dengan sumber sekitar 98-99%). Untuk master resmi, tetap sebaiknya diekspor dari file sumber (Illustrator/Figma).
- Warna hitam memakai `brand-black` `#0C0C0C` sesuai tema (sumber asli `#000000`).
- Favicon sengaja tanpa dua kotak piksel karena tidak terbaca di 16-48 px. Logo penuh tetap dipakai untuk ukuran lain.
- Tidak mencakup OG image; itu perlu dibuat ulang terpisah.
