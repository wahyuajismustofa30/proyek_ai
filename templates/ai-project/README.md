# [NAMA PROYEK]

> [Deskripsi singkat proyek dalam satu atau dua kalimat.]

Status: **Planning**  
Versi: **0.1.0**  
Pemilik: **[Nama/Tim]**  
Diperbarui: **[YYYY-MM-DD]**

## Tujuan
[Jelaskan masalah yang ingin diselesaikan dan hasil yang diharapkan.]

## Mulai bekerja dengan AI
1. Baca `AGENTS.md`.
2. Lengkapi `docs/PROJECT_BRIEF.md`.
3. Periksa `docs/ARCHITECTURE.md` dan `docs/TASKS.md`.
4. Sepakati scope sebelum implementasi.
5. Kerjakan satu task dalam satu waktu dan verifikasi hasilnya.

## Fitur utama
- [ ] [Fitur 1]
- [ ] [Fitur 2]
- [ ] [Fitur 3]

## Teknologi
- Platform: [Web / Mobile / API / CLI / lainnya]
- Bahasa: [Isi]
- Framework: [Isi]
- Database: [Isi atau Tidak ada]
- Deployment: [Isi]

## Struktur
```text
.
├── AGENTS.md
├── README.md
├── docs/
│   ├── PROJECT_BRIEF.md
│   ├── ARCHITECTURE.md
│   ├── TASKS.md
│   ├── DECISIONS.md
│   └── CHANGELOG.md
├── src/
├── tests/
├── assets/
└── .gitignore
```

Sesuaikan struktur dengan stack; jangan membuat folder atau dependency yang tidak diperlukan.

## Menjalankan proyek
[Isi perintah instalasi, konfigurasi, development, build, dan test setelah stack dipilih.]

## Testing
- Wajib lengkapi `docs/TESTING.md` berdasarkan [template strategi testing](docs/TESTING.md).
- Ikuti [standar testing repository](../../docs/TESTING_STANDARDS.md).
- Cantumkan perintah test pada bagian ini setelah stack ditentukan.

## Konfigurasi dan keamanan
- Salin contoh konfigurasi dari `.env.example` jika diperlukan.
- Jangan commit secret, token, password, private key, atau data pribadi.
- Dokumentasikan variabel environment tanpa mengisi nilai rahasia.

## Kriteria selesai
- Kebutuhan dan acceptance criteria terpenuhi.
- Pemeriksaan/test yang relevan lulus.
- Tidak ada secret atau data sensitif di repository.
- Dokumentasi dan changelog diperbarui.

## CI (GitHub Actions)

Template workflow tersedia di `.github/workflows/ci.yml`. Setelah folder template disalin ke root repository proyek baru, GitHub Actions menjalankan pemeriksaan pada setiap push, pull request, dan secara manual. Pemeriksaan dasar mencakup seluruh file pada commit pertama maupun commit berikutnya, keberadaan dokumen inti proyek, dan validitas semua JSON yang dilacak Git.

Setelah stack dipilih, tambahkan langkah instalasi dependency, lint, test, dan build yang benar-benar digunakan proyek. Jangan membiarkan contoh stack sebagai pemeriksaan aktif; sesuaikan perintah CI dengan `docs/TESTING.md` dan bagian Menjalankan proyek di README. Pastikan workflow berada di `.github/workflows/ci.yml` pada root proyek baru agar GitHub Actions mendeteksinya.
