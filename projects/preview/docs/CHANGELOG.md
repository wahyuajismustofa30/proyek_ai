# Changelog — Preview

Perubahan dicatat ringkas dan kronologis. Gunakan tanggal ISO (`YYYY-MM-DD`) dan tautkan PR bila tersedia.

## Unreleased

- Menerapkan satu percobaan autoplay backsound dengan fallback interaksi awal satu kali jika autoplay ditolak; listener fallback dilepas setelah playback berhasil atau pengguna mengambil keputusan manual. Pause lifecycle dibedakan dari pause manual dan audio tidak resume saat tab aktif kembali.
- Menambahkan riwayat pendidikan dan pekerjaan kandidat dari data yang diberikan.
- Mengganti tombol Back to Top dan panel audio dengan satu tombol musik mengambang untuk Play, mute, dan unmute; mempertahankan aset `assets/mp3/music.mp3`, volume awal 18%, tanpa autoplay.

- Dokumentasi konteks proyek, arsitektur, aset, panduan AI, dan testing ditambahkan untuk memudahkan pekerjaan lanjutan.
- Mempertahankan penghentian audio saat tab tidak aktif/halaman ditinggalkan serta memperbarui regression test dan checklist manual.
