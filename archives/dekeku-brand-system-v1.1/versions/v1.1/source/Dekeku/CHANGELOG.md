# Changelog DEKEKU Master Theme

## v1.5

**Maskot**
- Set ekspresi baru di `assets/maskot/`: senang (icon asli), oops, mikir, sukses, dan polos, masing-masing SVG hitam/putih dan PNG transparan 512 px.
- Dihasilkan oleh `scripts/build_maskot.py` dari icon asli, jadi badan dan kotak piksel identik dan hanya ekspresi yang berbeda.
- Halaman referensi: galeri ekspresi, maskot oops di contoh 404, maskot mikir di empty state. Badan maskot ditulis sekali di sprite dan dipakai ulang lewat `<use>`.

## v1.4

**Susunan folder**
- Dirapikan menjadi `tokens/`, `assets/{logo,icon,img}/`, `public/`, `referensi/`, `scripts/` (lihat README).
- `build_tokens.py` memakai jalur relatif ke akar paket, jadi bisa dijalankan dari folder mana pun.

**Logo dan icon dipakai di halaman referensi**
- Navbar dan footer memakai logo compact, hero dan empty state memakai icon/maskot, semuanya dari `assets/` sebagai `<symbol>` inline yang mengikuti tema terang/gelap.
- Tautan favicon, apple-touch-icon, dan manifest ditambahkan ke `<head>`.
- Placeholder bergaris putus (`.logo-slot`) dan teks "Logo belum diunggah" dihapus. Placeholder maskot "Oops" di contoh halaman 404 tetap karena asetnya belum ada.
- Skrip build kini juga memeriksa `<use>` yang rusak dan tautan berkas lokal yang tidak ada.

**Perbaikan kecil**
- Teks error email dan ikon toast memakai `status-error` dan `status-success` (sebelumnya warna statis yang kurang kontras di mode gelap).

## v1.3

**Sinkronisasi**
- Versi disamakan di `tokens.json`, `tokens.css`, nama file, judul, dan meta halaman referensi (semua v1.3).
- Blok token di halaman referensi dibangun ulang, sehingga `--logo` kini ikut tersedia.
- Komentar di halaman merujuk `site.webmanifest` (sebelumnya `manifest.webmanifest`).
- `build_tokens.py` memakai nama halaman `DEKEKU_ Halaman Referensi Tema v<versi>.html` secara bawaan dan kini memeriksa `var()` yang belum didefinisikan (gagal) serta warna tertanam di luar token (peringatan).

**Token baru**
- `status-success/warning/error/info`: warna status per mode untuk ikon, garis tepi, dan teks. Terang: #15803D, #B45309, #B91C1C, #1D4ED8 (min. 4,6:1 di semua permukaan). Gelap: #4ADE80, #FBBF24, #F87171, #60A5FA (min. 5,6:1).
- `danger-bg`, `danger-fg`: tombol berbahaya, lolos AA di kedua mode (terang 6,5:1, gelap 7,1:1).
- `footer-bg`, `footer-fg`, `footer-fg-muted`, `footer-link`, `footer-border`, `footer-border-strong`.
- `overlay` (latar modal), `section-spacing-tablet` (72px).

**Halaman referensi memakai token**
- Tipografi: `--fs-*` dan `--ls-*` untuk h1-h4, body, small, caption, eyebrow; aturan `h3` ditambahkan.
- Ukuran: `--control-height`, `--tap-target`, `--section-spacing-mobile`, `--section-spacing-tablet`.
- Durasi: `--duration-fast` dan `--duration-loader`.
- Warna: badge, alert, tombol danger, footer, thumb switch, dan latar modal tidak lagi memakai hex.
- Hasil visual di mode terang tidak berubah kecuali warna status (kini lebih gelap agar lolos kontras); mode gelap memakai warna status yang lebih terang.

## Aturan pemakaian warna

- **Status**: pakai `status-*` untuk ikon, garis tepi, dan teks. `success/warning/error/info` (nilai statis lama) hanya untuk elemen dekoratif besar, jangan untuk teks atau tombol.
- **Aksen**: `accent` (#6366F1, 4,47:1 di latar terang) hanya untuk elemen non-teks (fokus, switch, progress). Teks dan tautan memakai `accent-text`.
- **Palet undangan**: `inv-champagne` (2,4:1) dan `inv-sage` (4,0:1) di atas `inv-ivory` tidak boleh dipakai untuk teks. Teks memakai `inv-text` (12,9:1).
- **Breakpoint**: `@media` tidak bisa memakai `var()`. Nilai 768px dan 1024px di CSS harus sama dengan `--bp-tablet` dan `--bp-desktop`.
