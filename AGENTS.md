# Instruksi Repository

Aturan ini berlaku untuk seluruh repository. Ikuti instruksi platform terlebih dahulu, lalu aturan ini, kemudian instruksi lokal yang relevan di proyek target.

## Aturan inti

- Proyek berada langsung di `projects/<slug>/`; gunakan nama lowercase dengan huruf ASCII, angka, dan tanda hubung.
- Struktur internal proyek bebas. README, manifest, lockfile, `src/`, `tests/`, dokumentasi, dan konfigurasi AI tidak wajib.
- Jangan mengasumsikan file atau dokumentasi tersedia. Periksa source, konfigurasi, dependensi, riwayat, dan dokumentasi yang benar-benar ada.
- Kerjakan hanya ruang lingkup yang diminta. Untuk perbaikan sistem repository, jangan mengubah isi `projects/`; untuk tugas proyek, ubah hanya proyek yang diminta. Jangan melakukan refactor yang tidak relevan.
- Pertahankan data, aset, arsip, dan pekerjaan pengguna. Jangan menghapus, menimpa, atau memindahkan file tanpa alasan dan izin yang jelas.
- Jangan menyimpan secret, token, password, private key, credential, atau data pribadi sensitif di Git.
- Hindari dependency baru jika solusi bawaan sudah memadai. Jangan mengubah deployment atau layanan produksi tanpa instruksi eksplisit.
- Jika perubahan berisiko kehilangan data, mengubah keamanan, menyentuh produksi, atau melampaui ruang lingkup, jelaskan dampaknya dan minta persetujuan terlebih dahulu.

## Alur kerja

1. Periksa branch, commit dasar, status perubahan, riwayat, dan PR terkait.
2. Pahami proyek dari file yang tersedia; jangan membuat asumsi tentang struktur atau teknologi.
3. Implementasikan perubahan sekecil mungkin yang memenuhi permintaan.
4. Tambahkan atau perbarui regression test bila perilaku berubah dan tes relevan dapat dibuat.
5. Jalankan validasi yang tersedia dan relevan. Jangan mengklaim tes lulus jika tidak dijalankan.
6. Tinjau diff, file sensitif, dependensi, whitespace, dan perubahan yang tidak disengaja.
7. Kerjakan pada branch selain `main`, buat commit terfokus, dan ajukan PR ke `main`.

## GitHub dan validasi

- Jangan bekerja langsung pada `main`, force-push, atau melakukan operasi Git destruktif.
- Pertahankan perubahan pengguna yang belum di-commit atau belum di-stage.
- Jangan menggabungkan PR, menyetujui review, atau mengubah aturan branch tanpa persetujuan eksplisit.
- Bedakan hasil pemeriksaan: **PASS** (dijalankan dan berhasil), **NOTICE** (tidak tersedia/tidak dikonfigurasi), **FAIL** (kesalahan nyata), dan **NOT RUN** (tidak dijalankan).
- Jika pemeriksaan terhalang, laporkan hambatan dan dampaknya.

## Pelaporan

Laporkan ringkasan, file yang diubah, alasan, perintah dan hasil validasi, risiko atau pekerjaan tersisa, serta branch/commit/PR bila ada. Bedakan fakta terverifikasi dari asumsi. Jangan mengklaim tindakan berhasil sebelum hasilnya dikonfirmasi.
