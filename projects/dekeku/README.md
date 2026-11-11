# DEKEKU — Website & Master Theme

Proyek ini berisi homepage DEKEKU, aset identitas brand, dan halaman referensi Master Theme v1.6.

## Struktur

```text
.
├── index.html                  # Homepage bisnis DEKEKU
├── pages/
│   ├── paket.html              # Harga, rincian paket, dan FAQ
│   └── reference/index.html    # Referensi Master Theme v1.6
├── assets/
│   ├── icons/
│   └── logos/
├── css/
│   ├── main.css                # Fondasi bersama
│   ├── home.css                # Tampilan homepage
│   └── tokens.css              # Token dasar brand
├── js/main.js                  # Navigasi dan pengaturan tema
├── docs/head-snippet.html
└── manifest.webmanifest
```

## Menjalankan lokal

Website bersifat statis dan tidak memerlukan build maupun dependency tambahan.

Dari direktori `projects/dekeku/`, jalankan:

```sh
python -m http.server 8000
```

Lalu buka `http://localhost:8000`.

## Halaman

- **Homepage:** `index.html` — layanan, keunggulan, ringkasan harga, proses, dan FAQ singkat.
- **Paket & harga:** `pages/paket.html` — rincian paket website dan undangan digital serta FAQ lengkap.
- **Referensi desain:** `pages/reference/index.html` — dokumen referensi Master Theme v1.6, bukan halaman publikasi.

## Catatan konten

Harga ringkas pada homepage dan rincian paket lokal harus dijaga konsisten dengan halaman referensi aktif DEKEKU. Periksa kembali harga dan ketentuan sebelum publikasi jika informasi website aktif berubah.

Tautan konsultasi langsung belum dipasang karena alamat WhatsApp resmi belum diverifikasi. Tombol utama sementara diarahkan ke halaman paket.

## Aset

- `assets/logos/`: logo horizontal dan compact.
- `assets/icons/`: favicon, ikon, dan ikon PWA.
- `manifest.webmanifest`: metadata PWA.
- `docs/head-snippet.html`: contoh metadata head untuk integrasi.
