# Website Arto Printing

Situs katalog dan profil **Arto Printing** (percetakan di Bobotsari, Purbalingga):
katalog 960 desain dan 18 layanan dari `assets/data/produk.json`, detail produk + pesan lewat WhatsApp,
halaman layanan, cara pesan, testimoni, kontak, artikel blog, dan alat pembuat link tamu undangan.

- **Teknologi:** HTML statis, CSS, dan JavaScript modul (ES modules) bawaan browser. Situs utama tanpa framework/build; CSS generator undangan merupakan hasil kompilasi Tailwind yang sumber build-nya belum tersedia di repository.
- **Hosting:** GitHub Pages dengan domain `www.artoprintingpbg.com`.
- **Data:** file JSON di `assets/data/`.

---

## Halaman & alamat

Semua alamat memakai **huruf kecil**. Halaman selain beranda, `post/`, dan `tamu-undangan/` ada di folder `laman/`.

| Halaman | Alamat | File |
|---|---|---|
| Beranda | `/` (hero, jenis produk, layanan ringkas, keunggulan, cara pesan, ulasan, lokasi) | `index.html` |
| Katalog | `/laman/katalog/` (parameter: `?produk=`, `&kategori=`, `&status=ready\|pre-order`, `&cari=`) | `laman/katalog/index.html` |
| Layanan | `/laman/layanan/` | `laman/layanan/index.html` |
| Cara pesan | `/laman/cara-pesan/` | `laman/cara-pesan/index.html` |
| Testimoni | `/laman/testimoni/` | `laman/testimoni/index.html` |
| Kontak | `/laman/kontak/` | `laman/kontak/index.html` |
| Detail produk | `/laman/produk/?p=<slug>&id=<id>` (mis. `?p=undangan-cetak&id=5`) | `laman/produk/index.html` |
| Blog | `/blog/` | `blog/index.html` |
| Artikel | `/post/percetakan-murah-purbalingga.html` | `post/...` |
| Tamu undangan | `/tamu-undangan/`, `/tamu-undangan/generator.html` | `tamu-undangan/...` |
| Tidak ditemukan | (otomatis) | `404.html` (wajib di root untuk GitHub Pages) |

Setiap halaman berupa folder berisi `index.html`, jadi `/laman/katalog` (tanpa garis miring akhir)
otomatis dibuka sebagai `/laman/katalog/`.

**Pengalihan otomatis (alamat lama & alamat pendek tetap jalan):**

| Dibuka | Diarahkan ke | Oleh |
|---|---|---|
| `/?produk=mug&kategori=...` | `/laman/katalog/?produk=mug&kategori=...` | `core/redirect-lama.js` (di beranda) |
| `/#katalog-section`, `#layanan-section`, `#cara-pesan`, `#testimoni-section`, `#tentang-section` | halaman masing-masing | `core/redirect-lama.js` |
| `/produk.html?p=Mug&id=3` (format di `produk.json` & link lama) | `/laman/produk/?p=mug&id=3` | `produk.html` + `core/redirect-produk.js` |
| `/katalog`, `/Katalog`, `/KONTAK`, `/cara-pesan`, `/Cara Pesan`, `/Laman/Katalog`, `/produk`, `/beranda` | alamat resmi huruf kecil | `404.html` + `core/alias-404.js` (hanya di hosting yang memakai 404.html, mis. GitHub Pages) |

`produk.json` **tidak diubah** dan masih menulis `/produk.html?p=Undangan_Cetak&id=1`.
Saat ditampilkan, link itu langsung diubah ke `/laman/produk/?p=undangan-cetak&id=1`
(`components/product-card.js → linkProduk()`), jadi pengunjung tidak melewati pengalihan.
Halaman detail menerima `?p=undangan-cetak` maupun `?p=Undangan_Cetak`.

`sitemap.xml` dan `robots.txt` berisi daftar halaman untuk mesin pencari.

---

## Struktur folder

```text
/
├── index.html                  Beranda: hero, jenis produk, cuplikan testimoni, ajakan kontak
├── laman/
│   ├── katalog/index.html      tab jenis produk, chip kategori, pencarian, grid
│   ├── layanan/index.html      layanan di toko (dari data "Layanan")
│   ├── cara-pesan/index.html   4 langkah pemesanan
│   ├── testimoni/index.html    semua ulasan Google
│   ├── kontak/index.html       tentang, admin WhatsApp, alamat, foto toko, peta
│   └── produk/index.html       detail produk
├── blog/index.html              indeks artikel blog
├── post/percetakan-murah-purbalingga.html
├── tamu-undangan/              alat terpisah (style.css = hasil build Tailwind; jangan diedit manual)
├── produk.html                 pengalih alamat lama -> /laman/produk/ (jangan dihapus)
├── 404.html                    halaman tidak ditemukan + pengalih alamat pendek/huruf besar
├── favicon.ico · sitemap.xml · robots.txt
│
├── assets/
│   ├── css/
│   │   ├── base.css            token warna & font (palet logo), reset, utilitas, tombol
│   │   ├── layout.css          header, navigasi, judul halaman, section, footer, WA melayang
│   │   ├── components.css      tab, chip, pencarian, kartu produk, testimoni, bagikan, alamat & peta
│   │   ├── pages/              satu file per halaman: beranda, katalog, layanan, cara-pesan,
│   │   │                       testimoni, kontak, produk, artikel
│   │   └── legacy/nordic-custom.css   tema lama, tidak dipakai (arsip)
│   ├── data/                   ⚠ path ini kontrak dengan alur data spreadsheet
│   │   ├── produk.json · setting.json · ulasan.json
│   └── js/
│       ├── config.js           SEMUA pengaturan: nomor WA, alamat halaman, path data, urutan tab
│       ├── core/
│       │   ├── analytics.js       Google Analytics                 (script biasa di <head>)
│       │   ├── redirect-www.js    paksa www + https                 (script biasa di <head>)
│       │   ├── redirect-lama.js   link lama beranda -> halaman baru (hanya index.html)
│       │   ├── redirect-produk.js /produk.html -> /laman/produk/    (hanya produk.html)
│       │   ├── alias-404.js       /katalog -> /laman/katalog/ dst.  (hanya 404.html)
│       │   └── site.js            menu (+ tanda halaman aktif) & tombol bagikan
│       ├── services/data.js    ambil produk.json / setting.json / ulasan.json (dengan cache)
│       ├── utils/teks.js       esc, label, slug, rapikanTeks, angka
│       ├── components/         product-card.js (kartu + linkProduk), site-menu.js, share-links.js
│       ├── features/           hero, katalog, kategori-ringkas, layanan, testimoni
│       └── pages/              titik masuk per halaman: beranda, katalog, layanan, testimoni, produk-detail
│
├── partials/                   SUMBER header & footer bersama
├── tools/
│   ├── sinkron-partial.py      salin partials/ ke semua halaman
│   └── cek-proyek.py           periksa tautan, aset, data, partial sebelum deploy
└── README.md
```

### Pengelolaan aset gambar

Repository tidak memiliki direktori `assets/images/`. Aset gambar yang disimpan di repository tetap berada pada lokasi aktualnya, misalnya `favicon.ico` di root. Gambar produk dan aset visual lain yang dirujuk situs menggunakan URL eksternal; referensinya antara lain terdapat pada field `img` di `assets/data/produk.json`, konfigurasi `CONFIG.img` di `assets/js/config.js`, serta markup halaman.

URL gambar eksternal yang sudah digunakan merupakan bagian dari konfigurasi konten situs. Jangan mengganti, memindahkan, atau memigrasikannya tanpa kebutuhan teknis yang jelas dan persetujuan.

Perintah `python tools/cek-proyek.py --tulis-daftar-gambar` mengumpulkan URL eksternal dari atribut `src` elemen gambar di HTML dan field `img` dalam `assets/data/produk.json`. Hasilnya adalah daftar referensi URL yang ditemukan oleh script, bukan inventaris seluruh file gambar yang tersimpan di server eksternal. Direktori `docs/` beserta file daftar tersebut dibuat otomatis saat perintah dijalankan; keduanya tidak harus tersedia di repository.

### Urutan pemuatan di setiap halaman

```html
<head>
  ... meta SEO / Open Graph / canonical ...
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/layout.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages/<halaman>.css">
  <script src="/assets/js/core/analytics.js"></script>
  <script src="/assets/js/core/redirect-www.js"></script>
</head>
<body>
  <!-- partial:header --> ... <!-- /partial:header -->
  <main> ... </main>
  <!-- partial:footer --> ... <!-- /partial:footer -->
  <script type="module" src="/assets/js/pages/<halaman>.js"></script>   (atau core/site.js)
</body>
```

Semua path diawali `/` (absolut dari root domain), jadi file HTML di dalam folder (`laman/katalog/index.html`)
memakai aset yang sama tanpa `../`.

---

## Menjalankan di komputer sendiri

Harus lewat server lokal (path absolut, `fetch()` JSON, modul JavaScript):

```bash
python -m http.server 8000        # Windows: py -m http.server 8000
```

Buka <http://localhost:8000>, <http://localhost:8000/laman/katalog/>, dst.
Server lokal Python **tidak** memakai `404.html`, jadi pengalih alamat pendek (`/katalog`) hanya terlihat setelah deploy.
Pengalihan ke `www`/`https` otomatis mati di localhost.

## Sebelum deploy

1. Jalankan `python tools/cek-proyek.py --tulis-daftar-gambar` untuk membuat `docs/daftar-gambar-produk.txt`. Folder `docs/` dibuat otomatis bila belum tersedia. Daftar berisi URL gambar eksternal yang ditemukan pada atribut `src` elemen gambar di file HTML dan field `img` dalam `assets/data/produk.json`; URL dideduplikasi dan diurutkan.
2. Gunakan daftar tersebut sebagai referensi URL gambar eksternal yang ditemukan script. Daftar ini tidak mencakup seluruh file yang tersimpan di server eksternal dan tidak menjamin semua referensi gambar di CSS, JavaScript, atau layanan lain ikut tercatat.
3. Jalankan `python tools/cek-proyek.py` untuk memeriksa aset lokal dan melihat status gambar eksternal tanpa mengakses jaringan.
4. Opsional: jalankan `python tools/cek-proyek.py --cek-url-eksternal` untuk memeriksa URL gambar eksternal dengan timeout dan maksimal 8 koneksi paralel. HTTP 404/410 dilaporkan sebagai gambar hilang; gangguan jaringan dilaporkan sebagai gagal diverifikasi.
5. Push ke GitHub Pages. File `CNAME` / `.nojekyll` di repository (bila ada) jangan dihapus.

---

## Konfigurasi

| Yang ingin diubah | Tempatnya |
|---|---|
| Nomor WA admin untuk tombol pesan produk | `assets/js/config.js` → `waAdmin` |
| Alamat halaman yang dipakai JavaScript | `config.js` → `halaman` (ubah bersama nama folder, partial, `alias-404.js`, `sitemap.xml`) |
| Desain per halaman, tab awal, jeda pencarian | `config.js` → `katalog` |
| Urutan tab produk | `config.js` → `urutanProduk` |
| Deskripsi kategori yang menimpa `setting.json` | `config.js` → `deskripsiKhusus` |
| Jumlah ulasan awal (Testimoni / Beranda) | `config.js` → `testimoniAwal`, `testimoniBeranda` |
| ID Google Analytics yang dimuat | `assets/js/core/analytics.js` (konstanta di file ini; jangan disamakan otomatis dengan `setting.json`) |
| Menu & footer | `partials/*.html`, lalu `python tools/sinkron-partial.py` |
| Warna, font, radius | `assets/css/base.css` → `:root` |

## Data

- **`produk.json`** — kunci = jenis produk (`Undangan_Cetak`, `Mug`, ...), isi = array produk
  (`id`, `nama`, `kategori`, `img`, `keterangan`, `link_produk`, opsional `kode`, `status`, `stok`, `harga`).
  Kunci baru otomatis jadi tab di Katalog dan kartu di Beranda.
- **`setting.json`** — `katalog[].data` (slug) + `deskripsi` = teks pengantar tab. Field lain dipertahankan.
- **`ulasan.json`** — `ulasan[]`: `img`, `nama`, `ulasan`.

Format, nama field, dan lokasi file tidak diubah.

---

## Mengubah header / footer

1. Edit `partials/header.html` atau `partials/footer.html`.
2. Jalankan `python tools/sinkron-partial.py`.
3. Jangan edit isi di antara `<!-- partial:... -->` dan `<!-- /partial:... -->` langsung di halaman.

Menu yang sedang dibuka otomatis ditandai (`aria-current="page"`) oleh `components/site-menu.js`.

## Menambah halaman baru (contoh: `/laman/galeri/`)

1. Buat folder `laman/galeri/` lalu salin `laman/cara-pesan/index.html` ke `laman/galeri/index.html`.
2. Ganti `<title>`, meta description, `og:*`, `twitter:*`, `canonical` (`https://www.artoprintingpbg.com/laman/galeri/`),
   dan isi `<main>`. Judul halaman memakai `<h1>` di dalam `.section-head`.
3. CSS: buat `assets/css/pages/galeri.css`, ganti link `pages/cara-pesan.css` di `<head>`.
4. JavaScript: tanpa fitur khusus cukup `core/site.js`. Dengan fitur: buat `assets/js/pages/galeri.js`
   diawali `import '../core/site.js';`, dan taruh logika yang bisa dipakai ulang di `assets/js/features/`.
5. Tambahkan `"laman/galeri/index.html"` ke `HALAMAN` di `tools/sinkron-partial.py`, tambahkan menu di
   `partials/header.html` / `footer.html`, lalu jalankan `python tools/sinkron-partial.py`.
6. Tambahkan `galeri: '/laman/galeri/'` ke `config.js → halaman`, `'galeri': '/laman/galeri/'` ke `alias-404.js`,
   dan URL-nya ke `sitemap.xml`.
7. Jalankan `python tools/cek-proyek.py`.

## Konvensi

- Semua nama folder, file, dan alamat: huruf kecil, kata dipisah `-` (`laman/cara-pesan/`). Pengecualian: dokumen `README.md`.
- ID elemen yang dipakai JavaScript tidak diganti tanpa memperbarui modul terkait.
- Jangan menaruh token, private key, atau password di folder ini; semuanya publik.

---

## Pemeliharaan

### Data bisnis yang tertulis di beberapa tempat

Bila alamat, nomor WhatsApp, atau media sosial berubah, perbarui **semua** tempat berikut:

| Data | Lokasi |
|---|---|
| Alamat, WA utama | `partials/footer.html` (lalu `python tools/sinkron-partial.py`), `index.html` (bagian "Datang ke toko"), `laman/kontak/index.html`, JSON-LD `LocalBusiness` di `<head>` `index.html` dan `laman/kontak/index.html` |
| Nomor WA untuk tombol pesan | `assets/js/config.js → waAdmin`, tautan `wa.me/...` di HTML |
| 3 admin WhatsApp | `laman/kontak/index.html` |
| Instagram / TikTok | `partials/footer.html`, JSON-LD `sameAs` |
| Link Google Maps | `index.html`, `laman/kontak/index.html`, `laman/testimoni/index.html`, JSON-LD `hasMap` |

### Data terstruktur (JSON-LD)

- `LocalBusiness` di Beranda dan Kontak: nama, alamat, telepon, koordinat (dari embed Google Maps), media sosial.
  **Tidak** memuat rating, harga, atau jam buka karena datanya belum ada. Jangan menambahkannya tanpa data resmi.
- `Article` di halaman artikel: judul, tanggal terbit, gambar.
- Cek dengan <https://search.google.com/test/rich-results> setelah deploy.

### Kerangka (skeleton) & CLS

Bagian yang diisi dari JSON (katalog, layanan, testimoni, kartu beranda, detail produk) sudah berisi kerangka di HTML
supaya tata letak tidak bergeser saat data datang. Saat menambah bagian baru yang diisi JavaScript, ikuti pola yang sama:
beri isi kerangka (`.card.skeleton`, `.teks-skeleton`, `.pill-skeleton`) + `aria-busy="true"`, lalu set `aria-busy="false"` saat merender.

### `modulepreload`

Halaman Beranda, Katalog, Layanan, Testimoni, dan Detail Produk mencantumkan modul JS yang dipakainya dengan
`<link rel="modulepreload">` agar diunduh paralel. Bila menambah/menghapus `import`, sesuaikan daftar itu
(salah daftar tidak merusak fungsi, hanya mengunduh file yang tidak perlu atau kehilangan percepatan).

### Memeriksa sebelum deploy

```bash
python tools/cek-proyek.py          # validasi lokal; gambar eksternal belum diverifikasi
python tools/cek-proyek.py --cek-url-eksternal  # cek URL gambar eksternal (butuh jaringan)
python tools/sinkron-partial.py --cek
```

Pemeriksaan tambahan yang disarankan (butuh Chrome): Lighthouse di Chrome DevTools untuk tiap halaman,
dan ekstensi axe DevTools untuk aksesibilitas.

### Generator undangan: CSS dan dependensi

File `tamu-undangan/style.css` adalah hasil kompilasi Tailwind CSS 4.1.11. Repository saat ini tidak menyediakan `input.css` maupun manifest/lockfile build untuk mereproduksinya. Pertahankan file hasil kompilasi dan jangan menjalankan build ulang sampai sumber serta versi toolchain yang benar tersedia.

Generator memuat `showAlert()` dari jsDelivr pada commit immutable `72646e89a28be53dd3127c160c855085d2617b15` dan memverifikasi file dengan Subresource Integrity (SHA-384). Jika library diperbarui, verifikasi commit dan hitung ulang hash integritas dari file upstream sebelum mengubah URL.

## Layanan eksternal

| Layanan | Untuk |
|---|---|
| Google Fonts (Fredoka, Plus Jakarta Sans) | huruf |
| Google Analytics | statistik |
| Google Maps embed | peta di Kontak & artikel |
| WhatsApp (`wa.me`) | pesan & bagikan |
| Cloudinary (`res.cloudinary.com/ahwihzsc`) | gambar Open Graph/Twitter & apple-touch-icon |
| `undangan.dekeku.my.id` | demo undangan web |
| `lh3.googleusercontent.com` | foto profil pengulas |
| jsDelivr `wahyuajismustofa/berbagi-koding` | `showAlert()` di tamu-undangan (commit dipatok + SRI SHA-384) |
