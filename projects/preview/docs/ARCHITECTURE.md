# Architecture — Preview

## Gambaran

Website statis tanpa framework/build pipeline yang dinyatakan. Browser membuka `index.html`; file CSS dan JavaScript lokal dirujuk langsung.

## Komponen

| File | Tanggung jawab |
|---|---|
| `index.html` | Kerangka halaman, section, metadata, elemen awal, dan fallback markup |
| `js/data.js` | Objek data profil, visi/misi, program, potensi, dan galeri |
| `js/main.js` | Render data ke DOM dan interaksi UI |
| `css/style.css` | Gaya utama, layout, warna, tipografi, responsivitas |
| `css/improvements.css` | Lapisan peningkatan/penyesuaian tampilan |
| `css/icon-pack.css` | Gaya penggunaan ikon |
| `assets/` | Gambar kandidat/galeri dan ikon SVG |
| `CNAME` | Domain custom GitHub Pages (nilai perlu dikonfirmasi terhadap deployment aktif) |

## Alur render

1. Browser memuat HTML dan stylesheet.
2. Script data menyediakan objek konten.
3. Script utama mengisi/menginisialisasi komponen dinamis dan listener.
4. Pengguna berinteraksi dengan navigasi, panel visi, kartu misi/program, galeri/lightbox, dan kontrol scroll.

## Pola penting

- Konten dan logika dipisah sebagian melalui `js/data.js` dan `js/main.js`.
- Sebagian informasi juga berada langsung di HTML. Duplikasi data antara markup dan objek JS berpotensi drift; sebelum mengubah konten, cari seluruh pemakaian terkait.
- Render dinamis memakai interpolasi HTML. Data harus dianggap trusted/static dan tidak boleh menerima input tidak tepercaya tanpa escaping atau DOM API aman.
- Tidak ada bukti backend atau dependency runtime pihak ketiga yang diperlukan untuk fungsi inti.

## Prinsip perubahan

- Perubahan struktur section harus menyesuaikan selector/ID yang dipakai JavaScript.
- Perubahan data harus menjaga kontrak key/array yang dipakai renderer.
- Perubahan aset harus memperbarui referensi dan memeriksa path lokal.
- Jangan melakukan refactor besar hanya untuk tugas konten kecil.
