# Architecture — Preview

## Gambaran

Website statis tanpa framework/build pipeline yang dinyatakan. Browser membuka `index.html`; file CSS dan JavaScript lokal dirujuk langsung.

## Komponen

| File | Tanggung jawab |
|---|---|
| `index.html` | Kerangka halaman, section, metadata, elemen awal, dan fallback markup |
| `js/data.js` | Objek data profil, visi/misi, program, potensi, dan galeri |
| `js/main.js` | Render data ke DOM, interaksi UI, dan kontrol audio HTML5 melalui satu tombol mengambang |
| `css/style.css` | Gaya utama, layout, warna, tipografi, responsivitas |
| `css/improvements.css` | Lapisan peningkatan/penyesuaian tampilan |
| `css/icon-pack.css` | Gaya penggunaan ikon |
| `assets/` | Gambar kandidat/galeri dan ikon SVG |
| `CNAME` | Domain custom GitHub Pages (nilai perlu dikonfirmasi terhadap deployment aktif) |

## Alur render

1. Browser memuat HTML dan stylesheet.
2. Script data menyediakan objek konten.
3. Script utama mengisi/menginisialisasi komponen dinamis dan listener.
4. Pengguna berinteraksi dengan navigasi, panel visi, kartu misi/program, galeri/lightbox, dan kontrol scroll progress/sticky header.
5. Inisialisasi audio mencoba autoplay satu kali. Jika Promise ditolak, listener fallback sementara menunggu interaksi awal pada area konten (pointerdown, atau touchstart/click pada browser tanpa Pointer Events). Kontrol interaktif dikecualikan; tombol musik tetap dapat memulai musik secara langsung.
6. Setelah playback berhasil atau pengguna mengambil tindakan manual, fallback dilepas. Satu tombol mengelola Play saat berhenti dan mute/unmute saat berjalan. Sumber lokal `assets/mp3/music.mp3`, volume awal 18%.
7. Error `play()` diklasifikasikan berdasarkan nama DOMException (`NotAllowedError`, `NotSupportedError`, `NotFoundError`, `AbortError`, dan error lain); hanya penolakan autoplay `NotAllowedError` yang mengaktifkan fallback interaksi. Error media juga dipetakan dari kode `HTMLMediaElement.error`.
8. Alasan pause lifecycle disimpan sebelum `pause()` dan dipakai kembali oleh event `pause`; event pause tertunda diabaikan jika playback sudah berjalan lagi. Pause lifecycle tetap dibedakan dari pause manual; audio tidak otomatis dilanjutkan saat tab/fokus kembali.

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
