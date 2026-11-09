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
- Menu navigasi mobile dengan status aksesibel.
- Formulir interaktif yang hanya melakukan simulasi validasi di browser; tidak mengirim atau menyimpan data.
- Aset SVG lokal yang disajikan dari document root.

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

Buka `http://localhost:8080` di browser. Semua file yang diminta browser, termasuk ikon SVG, berada di bawah `src/` sebagai document root.

## Pengujian

```bash
npm test
```

Test Node memeriksa metadata/landmark halaman, resolusi URL aset terhadap document root HTTP, breakpoint dan progressive enhancement CSS, validasi email, serta perilaku menu dan form melalui DOM stub tanpa dependency eksternal. CI monorepo juga menjalankan validasi HTML, CSS, dan aset lokal.

## Struktur

- `src/`: document root berisi halaman, source browser, stylesheet, dan `assets/`.
- `tests/`: pengujian otomatis.
- `docs/`: brief, arsitektur, keputusan, dan strategi testing.

## Batasan

- Tidak ada backend, autentikasi, database, analytics, atau pengiriman formulir.
- Test DOM stub tidak menggantikan browser automation, visual regression, atau audit aksesibilitas penuh.
- Jangan memasukkan data pribadi, kredensial, atau konten bisnis nyata ke demo.
- Jangan menambahkan framework atau dependency tanpa kebutuhan dan keputusan terdokumentasi.
