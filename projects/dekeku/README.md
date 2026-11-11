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

Data katalog referensi telah dipindahkan ke `data/produk.json`. Katalog, keranjang, dan formulir pemesanan WhatsApp menggunakan JavaScript native dan penyimpanan lokal browser.


## Menjalankan lokal

Website bersifat statis dan tidak memerlukan build maupun dependency tambahan.

Dari direktori `projects/dekeku/`, jalankan:

```sh
python -m http.server 8000
```

Lalu buka `http://localhost:8000`.

## Status implementasi halaman

- **Homepage:** `index.html` — layanan, keunggulan, ringkasan harga, proses, dan FAQ.
- **Produk:** `pages/produk.html` — katalog dinamis dengan data `data/produk.json`, filter, pencarian, pagination, dan pilihan paket.
- **Paket & harga:** `pages/paket.html` — rincian paket dan FAQ.
- **Tentang:** `pages/tentang.html` — profil dan perjalanan DEKEKU.
- **Kontak:** `pages/kontak.html` — kanal WhatsApp dan lokasi Arto Printing.
- **Keranjang:** `pages/keranjang.html` — jumlah, hapus item, subtotal, dan total.
- **Pemesanan:** `pages/order.html` — validasi data pelanggan, ringkasan, penyusunan pesan WhatsApp, dan riwayat lokal.
- **Status situs:** `404.html`, `500.html`, dan `maintenance.html`.
- **Referensi desain:** `pages/reference/index.html` — dokumen referensi Master Theme, bukan halaman publik.

### Batas integrasi pembayaran

Integrasi Midtrans belum diaktifkan. Repository referensi hanya memperlihatkan pemanggilan endpoint Cloudflare Worker dari frontend; kode backend, validasi harga di server, dan mekanisme verifikasi notifikasi pembayaran tidak tersedia untuk diaudit dari repository ini. Karena itu, alur saat ini menyiapkan permintaan pesanan melalui WhatsApp dan tidak mengklaim pembayaran atau pesanan telah terkonfirmasi. Catatan pesanan disimpan lokal di browser pengguna, bukan di server.


## Catatan konten

Harga ringkas pada homepage dan rincian paket lokal harus dijaga konsisten dengan halaman referensi aktif DEKEKU. Periksa kembali harga dan ketentuan sebelum publikasi jika informasi website aktif berubah.

Nomor WhatsApp dan informasi lokasi pada halaman kontak mengikuti informasi yang tersedia pada repository referensi DEKEKU. Periksa kembali sebelum publikasi jika informasi kontak berubah.

## Aset

- `assets/logos/`: logo horizontal dan compact.
- `assets/icons/`: favicon, ikon, dan ikon PWA.
- `manifest.webmanifest`: metadata PWA.
- `docs/head-snippet.html`: contoh metadata head untuk integrasi.
