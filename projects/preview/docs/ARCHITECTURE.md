# Architecture — Preview

## Gambaran

Website statis tanpa framework/build pipeline yang dinyatakan. Browser membuka `index.html`; file CSS dan JavaScript lokal dirujuk langsung.

## Komponen

| File | Tanggung jawab |
|---|---|
| `index.html` | Kerangka halaman, section, metadata, elemen awal, dan fallback markup |
| `js/data.js` | Objek data profil, visi/misi, program, potensi, dan galeri |
| `js/audio.js` | Pengelolaan playback HTML5, fallback gesture, sinkronisasi state, dan lifecycle melalui satu tombol |
| `js/main.js` | Render data ke DOM dan menginisialisasi interaksi UI serta controller audio |
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
5. Listener fallback gesture dipasang sebelum percobaan autoplay agar interaksi pertama tidak terlewat ketika Promise autoplay ditolak. Fallback menangani `pointerdown` dan `touchstart` (serta `click` pada browser tanpa Pointer Events); hanya tombol musik dan area contenteditable yang dikecualikan. Percobaan fallback dipanggil langsung dari event gesture dan listener dipasang kembali jika browser tetap menolak pemutaran.
6. Fallback dilepas setelah playback benar-benar berhasil atau pengguna menekan kontrol musik. Satu tombol mengelola Play saat berhenti dan mute/unmute saat berjalan. Sumber lokal `assets/mp3/music.mp3`, volume awal 30%.
7. Error `play()` diklasifikasikan berdasarkan nama DOMException (`NotAllowedError`, `NotSupportedError`, `NotFoundError`, `AbortError`, dan error lain); hanya penolakan autoplay `NotAllowedError` yang mengaktifkan fallback interaksi. Error media juga dipetakan dari kode `HTMLMediaElement.error`.
8. Alasan pause lifecycle disimpan sebelum `pause()` dan dipakai kembali oleh event `pause`; event pause tertunda diabaikan jika playback sudah berjalan lagi. Pause lifecycle tetap dibedakan dari pause manual; audio tidak otomatis dilanjutkan saat tab/fokus kembali.

## Audio dan lifecycle

State audio hanya hidup di memori dokumen. Refresh membuat state JavaScript baru, mengulang satu percobaan autoplay, dan memasang fallback gesture sebelum percobaan tersebut; tidak ada status audio yang disimpan di storage atau cookie. Saat tab tersembunyi atau halaman ditinggalkan, percobaan `play()` yang tertunda diinvalidasi dan `pause()` tetap dipanggil meskipun `HTMLMediaElement.paused` masih `true`. Promise lama tidak boleh menimpa keputusan lifecycle atau playback baru. Event `play` hanya menyinkronkan UI; inisialisasi sukses ditetapkan setelah Promise playback yang masih berlaku selesai. Halaman yang kembali aktif tidak otomatis melanjutkan musik.

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
