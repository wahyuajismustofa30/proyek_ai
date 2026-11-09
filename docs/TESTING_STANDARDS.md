# Standar Testing untuk Setiap Proyek

Gunakan dokumen ini untuk proyek aktif di `projects/` dan scaffold dari
`templates/ai-project/`. Pilih lapisan test sesuai stack, kebutuhan, dan risiko;
jangan menambah framework yang tidak diperlukan.

## Prinsip wajib

- Uji perilaku dan kontrak yang terlihat, bukan hanya detail implementasi.
- Tambahkan regression test untuk bug dan perubahan berisiko.
- Test harus dapat diulang, deterministik, terisolasi, dan dijalankan dari instruksi tertulis.
- Gunakan fixture sintetis; jangan gunakan data, akun, credential, atau layanan produksi.
- Hindari ketergantungan jaringan eksternal, waktu, urutan test, dan state bersama.
- Laporkan hasil secara jujur: PASS, FAIL, BLOCKED, atau NOT RUN.
- Perketat test untuk autentikasi, pembayaran, data pribadi, upload, otorisasi, dan operasi destruktif.

## Artefak proyek

Setiap proyek menyediakan:

- `tests/`: test otomatis atau pemeriksaan terstruktur yang sesuai.
- `docs/TESTING.md`: strategi, prasyarat, perintah, cakupan, fixture, dan verifikasi manual.
- README: ringkasan perintah test dan tautan ke `docs/TESTING.md`.
- CI: pemeriksaan otomatis relevan pada PR/push jika implementasi sudah dapat diuji.

Untuk proyek non-kode, jelaskan alternatif checklist/pemeriksaan aset di
`docs/TESTING.md`. Jangan menghapus dokumentasi wajib tanpa alasan.

## Lapisan test

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

Pilih kombinasi yang relevan; tidak semua proyek memerlukan seluruh lapisan.

## Fokus menurut jenis proyek

- **Web/website:** unit untuk logika, integration untuk API/form, E2E alur utama,
  responsive mobile/desktop, link, metadata, keyboard, dan loading/empty/success/error.
- **Undangan online:** tanggal/zona waktu, nama tamu dan URL, RSVP normal/gagal/duplikat,
  media, serta perlindungan data tamu dari URL, log, source map, dan endpoint publik.
- **Design system/aset:** parse token JSON/CSS, konsistensi token, keberadaan dan format
  aset, dimensi/rasio, kontras, light/dark, dan visual review manual.
- **API/backend/CLI:** input valid/tidak valid, permission, exit code, error, timeout,
  retry, dan integrasi eksternal melalui stub/container test.
- **Dokumentasi/non-kode:** tautan internal, struktur, format, instruksi, contoh konfigurasi,
  dan checklist review.

## Kualitas dan kapan menjalankan

- Satu test fokus pada satu perilaku; nama test menjelaskan kondisi dan hasil.
- Sertakan kasus normal, batas, input invalid, dan failure path untuk fungsi kritis.
- Mock hanya batas eksternal; jangan mock logika yang sedang diuji.
- Bersihkan file, proses, database, dan resource test.
- Jangan menurunkan assertion atau cakupan demi membuat CI hijau; coverage 100% bukan tujuan tersendiri.
- Fixture harus kecil, sintetis, dan bebas data pribadi.

| Perubahan | Pemeriksaan minimum |
|---|---|
| Kode/bug | Test terkait, lint/type check, regression test |
| API/schema/database | Unit, integration/contract, migrasi pada database test |
| UI/CSS | Test komponen dan visual/responsive review |
| Auth/permission | Positive dan negative authorization test |
| Dependency | Suite terkait dan security scan |
| Dokumentasi/konfigurasi | Link, format, schema, dan contoh perintah |

Sebelum merge, required CI checks harus lulus. Jika ada blocker eksternal,
catat BLOCKED dan risikonya; jangan menyebutnya PASS.

## Laporan hasil

Sebutkan perintah yang dijalankan, status tiap pemeriksaan, skenario/cakupan
penting, pemeriksaan manual yang dilakukan, serta risiko dan area yang belum diuji.

## Stack baru

Tentukan test runner dan perintah standar saat stack dipilih. Pin dependency
pada manifest/lockfile dan dokumentasikan perintah seperti `test`, `lint`,
`typecheck`, dan `build`. Tambahkan adapter CI sebelum stack dianggap
teruji otomatis; jangan menebak perintah atau memasang framework tanpa alasan.
