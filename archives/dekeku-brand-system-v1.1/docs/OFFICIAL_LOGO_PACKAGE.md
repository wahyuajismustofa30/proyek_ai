# Paket Logo Resmi DEKEKU

**Status:** acuan identitas visual resmi untuk pekerjaan DEKEKU berikutnya  
**Tagline:** YOUR DIGITAL SPACE  
**Sumber arsip resmi:** [`archives/dekeku-logo-package.zip`](../../dekeku-logo-package.zip)
**Pemilik/sumber:** paket diberikan oleh pemilik DEKEKU.

Dokumen ini menjelaskan inventaris dan aturan penggunaan paket. **File ZIP di `archives/` adalah sumber biner asli**; dokumen ini hanya panduan dan bukan pengganti aset logo. Arsip sumber dipertahankan tanpa modifikasi.

## Inventaris aset

| Folder di dalam ZIP | Isi |
|---|---|
| `01-logos/` | Logo horizontal transparan, varian terang/gelap, maskot PNG dan SVG |
| `02-icons-favicon/` | Ikon terang/gelap/transparan, favicon PNG 16–256 px, dan ICO |
| `03-social/` | Open Graph 1200×630 dalam PNG dan JPG |
| `04-guidelines/` | Panduan singkat identitas |

Nama folder di atas merujuk pada struktur **di dalam arsip ZIP**, bukan direktori yang sudah diekstrak di repository.

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

File SVG dalam paket merupakan pembungkus SVG dengan PNG tertanam, bukan vektor murni berbasis path. Untuk kebutuhan cetak besar atau pengubahan bentuk, siapkan artwork vektor final secara terpisah.

## Hubungan dengan baseline Brand System

Paket logo resmi ini menjadi acuan identitas logo untuk pekerjaan DEKEKU berikutnya. Master tema v1.1 tetap merupakan baseline historis/read-only dan tidak ditimpa oleh paket logo ini.

Jika aset dari ZIP digunakan dalam source proyek:
1. Ekstrak hanya file yang diperlukan ke direktori aset aktif pada versi pengembangan.
2. Catat nama file sumber dan asalnya dari `archives/dekeku-logo-package.zip`.
3. Jangan mengedit atau menimpa ZIP arsip.
4. Pertahankan file asli; optimasi atau konversi harus menghasilkan file turunan yang jelas diberi nama dan didokumentasikan.

Lihat [inventaris seluruh arsip](../../README.md) untuk kebijakan penyimpanan dan hubungan antar paket.
