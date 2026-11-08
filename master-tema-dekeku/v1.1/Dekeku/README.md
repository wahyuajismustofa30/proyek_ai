# DEKEKU Master Theme v1.5

Token desain, aset logo dan ikon, serta halaman referensi komponen untuk website DEKEKU.

## Susunan folder

| Folder | Isi |
|---|---|
| `tokens/` | `tokens.json` (sumber tunggal, ubah di sini) dan `tokens.css` (dihasilkan, jangan diedit) |
| `assets/logo/` | Logo horizontal (dengan tagline) dan compact (icon + wordmark), versi hitam `#0C0C0C` dan putih, SVG |
| `assets/icon/` | Icon/maskot SVG (hitam dan putih), PNG terang 512 dan transparan 512 |
| `assets/maskot/` | Set ekspresi maskot: `svg/` (hitam dan putih) dan `png/` (transparan 512 px) |
| `assets/img/` | Foto proyek (kosong, lihat `README.md` di dalamnya) |
| `public/` | Berkas yang disalin ke **root situs**: favicon, apple-touch-icon, ikon PWA, `site.webmanifest`, `head-snippet.html` |
| `referensi/` | Halaman referensi komponen (`.html`) dan salinan teksnya (`.md`) |
| `scripts/` | `build_tokens.py` (token dan sprite halaman), `build_maskot.py` (ekspresi maskot) |

## Alur kerja

1. Ubah warna, ukuran, atau teks token di `tokens/tokens.json`.
2. Jalankan `python3 scripts/build_tokens.py`.
3. Skrip menulis ulang `tokens/tokens.css`, menyuntik token ke halaman referensi, dan menyisipkan logo compact dan icon dari `assets/` sebagai `<symbol>` inline (warna mengikuti tema terang/gelap lewat `currentColor`).
4. Skrip juga memeriksa `var()` yang belum terdefinisi, `<use>` yang rusak, tautan berkas lokal yang tidak ada, dan warna tertanam.

Mengganti logo atau maskot: timpa berkas di `assets/logo/` atau `assets/maskot/svg/` dengan nama yang sama, lalu jalankan ulang skrip.

## Memakai logo dan icon di halaman

```html
<a href="/" class="logo" aria-label="DEKEKU, ke beranda"><svg aria-hidden="true" focusable="false"><use href="#dk-logo-compact"/></svg></a>
<svg class="brand-icon" role="img" aria-label="Maskot DEKEKU"><use href="#dk-icon"/></svg>
```

Symbol maskot: `#dk-icon` (senang), `#dk-maskot-oops`, `#dk-maskot-mikir`, `#dk-maskot-sukses`.

## Maskot

Maskot adalah icon DEKEKU: badan, lubang wajah, dan dua kotak piksel tidak diubah. Hanya ekspresi (mata dan mulut) yang berbeda, digambar mengikuti kemiringan kepala asli.

| Ekspresi | Berkas | Dipakai untuk |
|---|---|---|
| Senang | `maskot-senang` | Beranda, sambutan, default (sama dengan icon) |
| Oops | `maskot-oops` | Halaman 404, error |
| Mikir | `maskot-mikir` | Kosong, memuat, mencari |
| Sukses | `maskot-sukses` | Pesan terkirim, pesanan selesai |
| Polos | `maskot-polos` | Badan tanpa ekspresi, bahan membuat ekspresi baru |

Setiap ekspresi ada versi hitam (`#0C0C0C`) dan putih (`-white`). Ukuran tampil 96-280 px. Ekspresi baru: tambahkan di `scripts/build_maskot.py`, jalankan `python3 scripts/build_maskot.py --png` (butuh playwright untuk PNG), lalu daftarkan di `MASKOT` pada `scripts/build_tokens.py`.

Warna logo `var(--logo)` (hitam di terang, putih di gelap). Di footer dan blok gelap permanen memakai `var(--footer-fg)`. Logo horizontal dan versi putih di `assets/logo/` dipakai sebagai berkas terpisah (`<img>`) untuk OG image, email, dan dokumen.

## Aset ikon

| Berkas | Fungsi |
|---|---|
| `public/favicon.svg` | Favicon adaptif (hitam di tema terang, putih di tema gelap), tanpa kotak piksel |
| `public/favicon.ico`, `favicon-16/32/48.png` | Favicon multi-ukuran, kotak membulat gelap + icon putih |
| `public/apple-touch-icon.png` | 180 px, tanpa transparansi |
| `public/dekeku-icon-dark-192/512.png` | Ikon PWA dengan latar gelap (glyph 70%) |
| `public/dekeku-icon-maskable-512.png` | PWA maskable (glyph di dalam safe zone) |
| `assets/icon/dekeku-icon-light-512.png` | Ikon latar terang |
| `assets/icon/dekeku-icon-transparent-512.png`, `-white-transparent-512.png` | Ikon transparan, margin 8% |

## Catatan

- SVG dihasilkan dengan trace dari PNG resolusi tertinggi (kecocokan sekitar 98-99%). Untuk master resmi, sebaiknya diekspor dari file sumber (Illustrator/Figma).
- Warna hitam memakai `brand-black` `#0C0C0C` (sumber asli `#000000`).
- Favicon sengaja tanpa dua kotak piksel karena tidak terbaca di 16-48 px.
- Belum ada: OG image dan foto. Ekspresi maskot adalah rancangan awal, sebaiknya ditinjau desainer sebelum dipakai sebagai master resmi.
- Aturan pemakaian warna dan riwayat perubahan ada di `CHANGELOG.md`.
