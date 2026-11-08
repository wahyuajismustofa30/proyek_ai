# Standar Testing untuk Setiap Proyek

Dokumen ini wajib menjadi acuan semua proyek aktif di `projects/` dan semua proyek baru yang dibuat dari `templates/ai-project/`. Setiap proyek harus memiliki strategi testing yang sesuai risiko dan teknologinya; jangan memaksakan framework yang tidak relevan.

## Prinsip wajib

1. **Test perilaku, bukan sekadar implementasi.** Verifikasi hasil yang terlihat oleh pengguna dan kontrak antarbagian.
2. **Uji perubahan dan regresi.** Setiap bug yang diperbaiki idealnya mendapat test yang gagal sebelum perbaikan dan lulus sesudahnya.
3. **Otomatisasi yang dapat diulang.** Test harus dapat dijalankan dari instruksi tertulis, tanpa bergantung pada mesin developer tertentu.
4. **Isolasi.** Gunakan data dummy/factory dan environment test. Jangan memakai data, akun, kredensial, atau layanan produksi.
5. **Deterministik.** Hindari test yang bergantung pada waktu, jaringan eksternal, urutan eksekusi, atau state bersama tanpa kontrol.
6. **Jujur dalam pelaporan.** Bedakan PASS, FAIL, BLOCKED, dan NOT RUN. Jangan menyebut test lulus jika tidak dijalankan.
7. **Proporsional terhadap risiko.** Area autentikasi, pembayaran, data pribadi, upload, hak akses, dan operasi destruktif memerlukan pengujian lebih ketat.

## Artefak yang wajib ada pada setiap proyek

- `tests/`: test otomatis atau pemeriksaan terstruktur yang sesuai jenis proyek. Untuk proyek non-kode, isi dengan checklist/pemeriksaan aset dan tautkan dokumentasinya.
- `docs/TESTING.md`: strategi, prasyarat, perintah, cakupan, data test, dan prosedur verifikasi manual proyek.
- README: perintah singkat untuk menjalankan test dan tautan ke `docs/TESTING.md`.
- CI workflow: jalankan pemeriksaan otomatis yang relevan pada Pull Request dan push ke branch utama, jika proyek sudah memiliki implementasi yang dapat diuji.

Jika suatu artefak tidak relevan, jelaskan alasan dan alternatifnya di `docs/TESTING.md`; jangan menghapus kewajiban dokumentasi tanpa alasan.

## Tingkatan testing

Pilih lapisan yang relevan; tidak semua proyek memerlukan semua lapisan.

| Lapisan | Tujuan | Contoh |
|---|---|---|
| Static / lint | Menemukan masalah sebelum runtime | formatter, linter, type check, validasi JSON/YAML |
| Unit | Memeriksa fungsi/komponen terkecil secara terisolasi | utilitas, validasi, kalkulasi, formatter |
| Integration | Memeriksa kerja sama beberapa komponen | API + database test, service + repository |
| Contract / API | Menjaga bentuk request, response, dan kompatibilitas | schema, status code, auth policy |
| End-to-end (E2E) | Memeriksa alur pengguna utama | registrasi, checkout, RSVP, form kontak |
| Visual / accessibility | Memeriksa tampilan dan aksesibilitas | responsive screenshot, keyboard, contrast, semantic HTML |
| Security | Memeriksa risiko keamanan yang relevan | dependency audit, authz, input validation, upload |
| Manual acceptance | Memastikan hasil sesuai kebutuhan | checklist skenario pengguna dan perangkat |

## Minimum coverage berdasarkan jenis proyek

### Aplikasi web / website bisnis
- Unit test untuk logika bisnis, validasi, helper, dan komponen yang memiliki perilaku.
- Integration test untuk API, database, autentikasi, dan pengiriman form.
- E2E untuk halaman/arus utama: navigasi, form, error state, dan tampilan mobile.
- Periksa responsive pada viewport mobile dan desktop, link, metadata dasar, serta aksesibilitas keyboard.
- Uji loading, empty, success, dan error state.

### Undangan online
- Uji rendering detail acara, zona waktu/tanggal, nama tamu dan parameter URL.
- Uji RSVP: validasi, submit sukses, submit gagal, duplikasi, dan batas akses.
- Uji media, audio, galeri, dan performa halaman bila fitur tersebut digunakan.
- Pastikan data tamu tidak bocor melalui URL, log, source map, atau endpoint publik.
- E2E minimal untuk membuka undangan dan menyelesaikan RSVP pada mobile.

### Brand system / design system / aset
- Validasi struktur dan parse token JSON/CSS.
- Pastikan nama token, referensi warna, font, ukuran, dan varian konsisten.
- Validasi aset: file ada, format dapat dibaca, dimensi/rasio sesuai spesifikasi, dan tautan dokumentasi valid.
- Lakukan visual review untuk light/dark, ukuran layar, kontras, dan konsistensi komponen.
- Catat pemeriksaan manual visual karena screenshot comparison tidak selalu stabil.

### API / backend / CLI
- Unit test logika dan validasi input.
- Integration test untuk database, filesystem, jaringan, dan proses eksternal menggunakan stub/container test.
- Uji permission, error handling, timeout, retry, dan exit code.
- Jangan menjalankan test yang mengubah data produksi.

### Proyek dokumentasi / non-kode
- Validasi tautan internal, struktur, format, dan contoh konfigurasi.
- Periksa instruksi langkah demi langkah dan konsistensi antarhalaman.
- Gunakan checklist review sebagai test yang terdokumentasi.

## Aturan kualitas test

- Nama test menjelaskan kondisi dan hasil yang diharapkan.
- Satu test fokus pada satu perilaku utama.
- Sertakan kasus normal, batas (boundary), input tidak valid, dan kegagalan untuk fungsi kritis.
- Mock hanya batas eksternal; jangan mock logika yang justru ingin diverifikasi.
- Test tidak boleh saling bergantung atau mengandalkan urutan tertentu.
- Bersihkan file, database, proses, dan resource yang dibuat test.
- Jangan menonaktifkan assertion atau mengurangi cakupan hanya untuk membuat CI hijau.
- Hindari target coverage 100% sebagai tujuan kosong. Tetapkan ambang coverage per proyek jika alatnya tersedia; prioritaskan seluruh jalur kritis dan perubahan baru.
- Simpan fixture kecil, sintetis, dan bebas data pribadi.

## Kapan test wajib dijalankan

| Perubahan | Pemeriksaan minimum |
|---|---|
| Perubahan kode | test terkait + lint/type check yang tersedia |
| Perubahan API / schema / database | unit + integration/contract + migrasi pada database test |
| Perubahan UI / CSS | test komponen terkait + visual/responsive review |
| Perubahan autentikasi / hak akses | positive dan negative authorization tests |
| Perbaikan bug | regression test + test suite terkait |
| Perubahan dependency | test suite + dependency/security scan |
| Perubahan dokumentasi / konfigurasi | link, format, schema, dan contoh perintah terkait |

Sebelum merge ke branch utama, seluruh pemeriksaan wajib pada CI harus lulus. Jika test tidak dapat dijalankan karena blocker eksternal, tandai BLOCKED, jelaskan penyebab dan risiko, serta jangan menyamarkannya sebagai PASS.

## Laporan hasil testing

Setiap penyelesaian task harus menyebutkan:
- Perintah test/lint/build yang dijalankan.
- Hasil masing-masing: PASS / FAIL / BLOCKED / NOT RUN.
- Cakupan atau skenario penting yang diverifikasi.
- Test manual yang dilakukan dan perangkat/viewport jika relevan.
- Risiko dan area yang belum diuji.

## Penambahan stack baru

Saat memilih bahasa/framework, tentukan test runner dan perintah standar lebih awal. Simpan versi dependency di manifest/lockfile. Tambahkan perintah yang konsisten, misalnya `test`, `lint`, `typecheck`, dan `build` pada package manager yang digunakan. CI harus menjalankan perintah proyek tersebut; jangan menebak perintah atau menginstal framework testing tanpa persetujuan dan alasan teknis.
