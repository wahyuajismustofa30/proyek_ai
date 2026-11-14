# Asset Catalog — Preview

## Struktur

- `assets/images/slamet-profile.png`: gambar profil yang dirujuk README; isi saat ini perlu diverifikasi apakah placeholder.
- `assets/images/gallery/gallery-01.jpg` sampai `gallery-08.jpg`: delapan slot galeri.
- `assets/icons/color/`: ikon konten berwarna.
- `assets/icons/monochrome/`: ikon aksi/ikon yang dapat mengikuti warna melalui CSS.

## Konvensi

- URL SVG monokrom pada CSS mask diselesaikan dari direktori stylesheet `css/`; referensi dinamis di `js/main.js` menggunakan `../assets/icons/monochrome/` agar menuju aset pada root Preview.
- Validasi path ikon dijalankan melalui `python3 projects/preview/tests/test_asset_paths.py`.

- Pertahankan nama file slot galeri agar data dan renderer tetap kompatibel.
- Jangan mengganti aset dengan gambar generatif/stock seolah dokumentasi faktual kandidat atau desa.
- Gunakan aset yang disediakan/diotorisasi pemilik dan pastikan hak penggunaan.
- Optimalkan ukuran/format tanpa mengubah substansi visual; cek kualitas pada desktop dan mobile.
- Jika aset diganti, periksa alt text, dimensi, crop, kontras, serta referensi CSS/JS.

## Belum diverifikasi

- Identitas, sumber, lisensi, dan status final setiap foto.
- Kesesuaian isi ZIP `LandingPage Kampanye - Slamet Tlagayasa.zip` dengan source aktif.
- Apakah semua gambar galeri merupakan placeholder atau dokumentasi asli.

## Checklist aset

- [ ] Sumber dan izin penggunaan jelas.
- [ ] Nama/path cocok dengan referensi kode.
- [ ] Tidak ada metadata sensitif yang tidak perlu.
- [ ] Alt text menjelaskan gambar secara relevan.
- [ ] Ukuran file wajar dan tampilan responsif diperiksa.

## Audio latar

- File musik latar yang digunakan: `assets/mp3/music.mp3` (632.466 byte pada commit dasar yang diperiksa).
- `js/main.js` merujuk file tersebut melalui `BACKGROUND_AUDIO_SOURCE`; jangan mengganti atau mengunduh aset lain sebagai bagian dari perubahan kontrol UI.
- Sumber/pembuat/lisensi file harus tetap dicatat dan diverifikasi oleh pemilik aset sebelum distribusi publik.
