# Testing — DEKEKU Online Invitation

## Status
Proyek masih tahap persiapan; belum ada implementasi aplikasi. Test runtime belum dapat dijalankan.

## Strategi setelah implementasi
- **Unit:** format tanggal/waktu dan zona waktu, parsing parameter tamu, validasi RSVP, serta helper data undangan.
- **Integration:** penyimpanan/pengambilan RSVP, pembatasan akses, API, dan media storage jika digunakan.
- **E2E:** buka undangan melalui URL, tampilan detail acara, interaksi fitur yang disepakati, submit RSVP, dan state gagal/berhasil.
- **Responsive/visual:** mobile-first, ukuran layar berbeda, gambar, font, layout, dan fallback media.
- **Accessibility:** navigasi keyboard, label kontrol, semantic structure, kontras, dan reduced motion.
- **Security/privacy:** otorisasi RSVP, enumerasi nama tamu, kebocoran data melalui URL/log/source map, rate limit, dan validasi input.
- **Performance:** ukuran gambar/media, waktu muat, dan perilaku jaringan lambat.

## Data dan environment
Gunakan nama, alamat, nomor, dan data acara sintetis. Jangan menggunakan daftar tamu atau undangan produksi. Jangan mengirim notifikasi nyata selama test.

## Perintah
Belum ditetapkan karena stack dan fitur belum dipilih. Dokumentasikan perintah install, lint/typecheck, unit/integration, E2E, dan build setelah implementasi.

## Acceptance minimum sebelum rilis
- Tanggal dan waktu sesuai zona waktu acara.
- Parameter tamu tidak membuka data tamu lain.
- RSVP menangani input valid, invalid, duplikasi, dan kegagalan server.
- Tampilan utama diuji pada mobile dan desktop.
- Media memiliki fallback dan tidak menghambat akses konten.
- Tidak ada data pribadi atau secret dalam repository.

## Pengecualian saat ini
Unit, integration, E2E, dan build berstatus NOT APPLICABLE / NOT RUN karena belum ada source aplikasi. Status ini bukan PASS. Perbarui dokumen ketika stack dan implementasi tersedia.
