# Quality Checklist

Gunakan checklist ini sebelum menyatakan pekerjaan selesai. Item yang tidak relevan boleh ditandai N/A dengan alasan.

## Sebelum perubahan

- [ ] Proyek dan folder target sudah benar.
- [ ] README dan instruksi lokal sudah dibaca.
- [ ] Source baseline dan arsip tidak akan tertimpa.
- [ ] Dampak terhadap dependency, konfigurasi, dan kompatibilitas sudah dipahami.

## Implementasi

- [ ] Perubahan sesuai kebutuhan dan tidak melebar.
- [ ] Tidak ada placeholder yang disajikan sebagai data nyata.
- [ ] Tidak ada secret atau kredensial di source/diff.
- [ ] Nama, path, dan kontrak API yang sudah dipakai tetap kompatibel atau perubahan breaking dijelaskan.
- [ ] Error handling dan validasi input ditangani sesuai kebutuhan.

## Testing

- [ ] Strategi proyek tersedia di `docs/TESTING.md` dan sesuai [standar testing](TESTING_STANDARDS.md).
- [ ] Test untuk perilaku baru dan regresi bug ditambahkan.
- [ ] Data dan environment test terisolasi dari produksi.
- [ ] Test/lint/build relevan dijalankan; hasil PASS/FAIL/BLOCKED/NOT RUN dilaporkan.
- [ ] Pengecualian lapisan test dijelaskan beserta alternatifnya.

## Verifikasi

- [ ] JSON/YAML/config yang berubah tervalidasi.
- [ ] Lint/test/build relevan dijalankan.
- [ ] Pemeriksaan manual dilakukan untuk area yang tidak tercakup test.
- [ ] Diff diperiksa untuk perubahan tak sengaja.
- [ ] Hasil test dilaporkan secara jujur; test yang tidak dijalankan disebutkan.

## Dokumentasi dan serah terima

- [ ] README/CHANGELOG diperbarui jika diperlukan.
- [ ] PROJECT_INDEX diperbarui jika struktur/status proyek berubah.
- [ ] DECISIONS diperbarui untuk keputusan arsitektur penting.
- [ ] Ringkasan file, verifikasi, risiko, dan pekerjaan tersisa disampaikan.
