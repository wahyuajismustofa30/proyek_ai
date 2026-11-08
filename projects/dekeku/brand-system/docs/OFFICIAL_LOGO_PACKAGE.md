# Paket Logo Resmi DEKEKU

**Status:** acuan identitas visual resmi untuk pekerjaan DEKEKU berikutnya  
**Tagline:** YOUR DIGITAL SPACE  
**Sumber paket:** `dekeku-logo-package.zip` yang diberikan pemilik

Dokumen ini mencatat aturan penggunaan paket logo. Arsip sumber berisi aset raster dan pembungkus SVG; jangan menganggap SVG di dalam paket sebagai artwork path vektor.

## Inventaris aset

| Folder | Isi |
|---|---|
| `01-logos/` | Logo horizontal transparan, varian terang/gelap, maskot PNG dan SVG |
| `02-icons-favicon/` | Ikon terang/gelap/transparan, favicon PNG 16–256 px, dan ICO |
| `03-social/` | Open Graph 1200×630 dalam PNG dan JPG |
| `04-guidelines/` | Panduan singkat identitas |

## Aturan penggunaan

- Latar terang: gunakan logo gelap/hitam.
- Latar gelap: gunakan logo terang/putih.
- Header website: prioritaskan `dekeku-logo-horizontal-transparent.png`.
- Favicon ukuran kecil: gunakan ikon maskot saja, tanpa wordmark atau tagline.
- Avatar GitHub: gunakan ikon terang atau gelap sesuai latar.
- Preview media sosial: gunakan `og-image-1200x630.jpg`.
- Pertahankan proporsi, orientasi, bentuk, dan ruang kosong di sekitar logo. Jangan meregangkan, memiringkan, memberi bevel, atau mengubah bentuk maskot.

## Warna identitas

- Hitam: `#000000`
- Putih: `#FFFFFF`
- Abu-abu pendukung: `#777777`

## Open Graph

Gambar OG disiapkan pada ukuran 1200×630 (rasio 1.91:1). Saat diterapkan, ganti URL placeholder dengan URL aset yang benar-benar telah dipublikasikan.

```html
<meta property="og:type" content="website">
<meta property="og:title" content="DEKEKU — YOUR DIGITAL SPACE">
<meta property="og:description" content="Web development and digital solutions.">
<meta property="og:image" content="https://YOUR-DOMAIN/og-image-1200x630.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
```

## Catatan teknis

File SVG dalam paket merupakan pembungkus SVG dengan PNG tertanam, bukan vektor murni. Untuk kebutuhan cetak besar atau pengubahan bentuk, siapkan artwork vektor final secara terpisah.

## Hubungan dengan baseline brand system

Paket logo ini menjadi acuan identitas logo untuk pekerjaan baru. Jangan menimpa source baseline master theme v1.1 atau mengubah arsip versi terdahulu secara diam-diam. Integrasikan aset biner ke folder aset aktif pada commit terpisah ketika proses transfer file tersedia; dokumen ini sendiri bukan pengganti file logo.
