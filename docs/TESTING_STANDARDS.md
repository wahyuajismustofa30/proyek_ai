# Standar Testing untuk Proyek

Dokumen ini memberi panduan memilih pemeriksaan sesuai risiko dan teknologi proyek. Dokumen ini tidak mewajibkan struktur folder, test runner, README, atau direktori tests/ tertentu.

## Prinsip

- Uji perilaku dan kontrak yang terlihat.
- Tambahkan regression test untuk bug dan perubahan berisiko.
- Test harus deterministik, terisolasi, dan dapat dijalankan dari instruksi tertulis.
- Gunakan fixture sintetis; jangan gunakan data, akun, credential, atau layanan produksi.
- Hindari ketergantungan jaringan eksternal, waktu, urutan test, dan state bersama.
- Laporkan hasil jujur: PASS, FAIL, BLOCKED, atau NOT RUN.
- Perketat test untuk autentikasi, pembayaran, data pribadi, upload, otorisasi, dan operasi destruktif.

## Pilihan lapisan test

| Lapisan | Tujuan |
|---|---|
| Static/lint/type check | Format, tipe, schema, dan kesalahan sebelum runtime |
| Unit | Fungsi/komponen kecil dan logika bisnis |
| Integration | Interaksi API, database, service, dan filesystem |
| Contract/API | Bentuk request/response, status, dan kebijakan auth |
| End-to-end | Alur pengguna utama |
| Visual/accessibility | Responsive, keyboard, kontras, dan semantic HTML |
| Security | Dependency, otorisasi, input, upload, dan secret |
| Manual acceptance | Kesesuaian terhadap acceptance criteria |

Pilih kombinasi relevan; tidak semua proyek memerlukan seluruh lapisan. Untuk proyek non-kode, gunakan checklist atau pemeriksaan aset yang sesuai.

## Kualitas dan pelaporan

- Satu test fokus pada satu perilaku.
- Sertakan kasus normal, batas, input invalid, dan failure path untuk fungsi kritis.
- Mock hanya batas eksternal.
- Bersihkan file, proses, database, dan resource test.
- Jangan menurunkan assertion atau cakupan demi membuat CI hijau.
- Fixture harus kecil, sintetis, dan bebas data pribadi.

Sebutkan perintah yang dijalankan, status tiap pemeriksaan, cakupan, pemeriksaan manual, risiko, dan area yang belum diuji. Jika stack belum memiliki adapter CI, jelaskan bahwa test otomatis aplikasi belum tersedia.
