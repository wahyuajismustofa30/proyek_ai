# Testing — Web Page Lab

> Proyek latihan untuk membuat, menjalankan, dan memeriksa halaman web statis dengan HTML, CSS, dan JavaScript.

Status: **Active — Test Project**
Versi: **0.1.0**
Pemilik: **Wahyu**
Diperbarui: **2026-11-09**

## Tujuan

Menyediakan proyek nyata di dalam monorepo untuk menguji alur pembuatan halaman web dari brief sampai halaman dapat dijalankan. Contoh halaman menggunakan konten sintetis dan tidak mewakili bisnis atau layanan nyata.

## Fitur demo

- Halaman landing responsif berbahasa Indonesia.
- Struktur semantik HTML dan navigasi yang dapat digunakan dengan keyboard.
- Menu navigasi mobile.
- Formulir interaktif yang hanya melakukan simulasi validasi di browser; tidak mengirim atau menyimpan data.
- Aset SVG lokal tanpa ketergantungan CDN.

## Teknologi

- Platform: Web statis
- Bahasa: HTML5, CSS, JavaScript ES modules
- Runtime pengujian: Node.js 22+ (built-in test runner)
- Framework: Tidak digunakan
- Database/API: Tidak ada
- Deployment: Belum ditentukan; jalankan secara lokal untuk pengujian.

## Menjalankan proyek

Jalankan server statis dari root proyek:

```bash
python -m http.server 8080 --directory src
```

Buka `http://localhost:8080` di browser.

## Pengujian

```bash
npm test
```

CI monorepo juga menjalankan validasi HTML, CSS, SVG, dan referensi aset lokal. Pengujian Node memeriksa kontrak halaman, aset, responsivitas, dan helper validasi email. Pemeriksaan visual lintas-browser dan accessibility audit penuh belum termasuk.

## Struktur

- `src/`: halaman dan source browser.
- `assets/`: aset SVG lokal.
- `tests/`: pengujian otomatis.
- `docs/`: brief, arsitektur, keputusan, dan strategi testing.

## Batasan

- Tidak ada backend, autentikasi, database, analytics, atau pengiriman formulir.
- Jangan memasukkan data pribadi, kredensial, atau konten bisnis nyata ke demo.
- Jangan menambahkan framework atau dependency tanpa kebutuhan dan keputusan terdokumentasi.
