# DEKEKU — Website & Master Theme

Proyek ini berisi homepage DEKEKU, aset identitas brand, dan halaman referensi Master Theme v1.6.

## Struktur halaman

- `index.html` — halaman utama.
- `pages/produk.html` — katalog jenis layanan.
- `pages/paket.html` — paket, harga, dan FAQ.
- `pages/tentang.html` — profil dan perjalanan DEKEKU.
- `pages/kontak.html` — kanal konsultasi dan lokasi.
- `404.html`, `500.html`, dan `maintenance.html` — halaman status situs.
- `pages/reference/index.html` — referensi desain, bukan halaman publik.

Data katalog referensi telah dipindahkan ke `data/produk.json`. Katalog menggunakan JavaScript native; pemesanan dilakukan langsung melalui WhatsApp tanpa keranjang atau checkout lokal.


## Menjalankan lokal

Website bersifat statis dan tidak memerlukan build maupun dependency tambahan.

Dari direktori `projects/dekeku/`, jalankan:

```sh
python -m http.server 8000
```

Lalu buka `http://localhost:8000`.

## Status implementasi halaman

- **Homepage:** `index.html` — layanan, keunggulan, ringkasan harga, proses, dan FAQ.
- **Produk:** `pages/produk.html` — katalog dinamis dengan data `data/produk.json`, filter, pencarian, pagination, preview melalui ikon mata, dan pemesanan langsung melalui ikon keranjang ke WhatsApp.
- **Paket & harga:** `pages/paket.html` — rincian paket dan FAQ.
- **Tentang:** `pages/tentang.html` — profil dan perjalanan DEKEKU.
- **Kontak:** `pages/kontak.html` — kanal WhatsApp dan lokasi Arto Printing.
- **Pemesanan:** ikon keranjang pada setiap kartu produk membuka WhatsApp dengan nama produk, pilihan paket, harga, dan tautan preview. Pelanggan memilih paket serta melanjutkan detail pesanan langsung dalam percakapan WhatsApp.
- **Status situs:** `404.html`, `500.html`, dan `maintenance.html`.
- **Referensi desain:** `pages/reference/index.html` — dokumen referensi Master Theme, bukan halaman publik.

### Alur pemesanan

Pemesanan dimulai dari kartu produk dan dilanjutkan langsung melalui WhatsApp. Pelanggan memilih paket dan menyepakati detail pesanan di percakapan dengan DEKEKU. Website tidak menggunakan keranjang, checkout lokal, riwayat pesanan, atau pembayaran otomatis.


## Catatan konten

Harga ringkas pada homepage dan rincian paket lokal harus dijaga konsisten dengan halaman referensi aktif DEKEKU. Periksa kembali harga dan ketentuan sebelum publikasi jika informasi website aktif berubah.

Nomor WhatsApp dan informasi lokasi pada halaman kontak mengikuti informasi yang tersedia pada repository referensi DEKEKU. Periksa kembali sebelum publikasi jika informasi kontak berubah.

## Aset

- `assets/logos/`: logo horizontal dan compact.
- `assets/icons/`: favicon, ikon, dan ikon PWA.
- `manifest.webmanifest`: metadata PWA.
- `docs/head-snippet.html`: contoh metadata head untuk integrasi.
