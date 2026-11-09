# Changelog — Preview

Perubahan dicatat ringkas dan kronologis. Gunakan tanggal ISO (`YYYY-MM-DD`) dan tautkan PR bila tersedia.

## Unreleased

- Menginvalidasi percobaan `play()` yang masih tertunda saat tab/halaman tidak aktif, memanggil `pause()` untuk membatalkan pending playback, mencegah event media dan Promise lama mengubah keputusan terbaru, serta menambahkan simulasi runtime untuk refresh, lifecycle, dan retry gesture.

- Memperbaiki fallback gesture audio agar listener aktif sebelum percobaan autoplay, mendukung `pointerdown` dan `touchstart`, dapat mencoba kembali setelah penolakan gesture, serta hanya menandai audio terinisialisasi setelah playback berhasil; volume default dinaikkan dari 18% menjadi 30%.
- Memperbaiki URL ikon monokrom pada CSS mask agar diselesaikan dari direktori `css/` menuju aset SVG di `assets/icons/monochrome/`; menambahkan tes regresi validasi path aset.
- Membedakan error autoplay yang ditolak browser dari kegagalan sumber/format, pembatalan, dan error media; fallback interaksi hanya aktif untuk `NotAllowedError` saat autoplay awal.
- Mempertahankan alasan pause lifecycle melalui event `pause` dan mengabaikan event pause tertunda ketika playback baru sudah berjalan kembali.
- Memperluas regression test untuk klasifikasi error, fallback, urutan percobaan playback, serta sinkronisasi alasan pause.

- Menerapkan satu percobaan autoplay backsound dengan fallback interaksi awal satu kali jika autoplay ditolak; listener fallback dilepas setelah playback berhasil atau pengguna mengambil keputusan manual. Pause lifecycle dibedakan dari pause manual dan audio tidak resume saat tab aktif kembali.
- Menambahkan riwayat pendidikan dan pekerjaan kandidat dari data yang diberikan.
- Mengganti tombol Back to Top dan panel audio dengan satu tombol musik mengambang untuk Play, mute, dan unmute; mempertahankan aset `assets/mp3/music.mp3`, volume awal 18%, tanpa autoplay.

- Dokumentasi konteks proyek, arsitektur, aset, panduan AI, dan testing ditambahkan untuk memudahkan pekerjaan lanjutan.
- Mempertahankan penghentian audio saat tab tidak aktif/halaman ditinggalkan serta memperbarui regression test dan checklist manual.
