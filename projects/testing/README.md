# testing

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

## Teknologi
- Platform: [Web / Mobile / API / CLI / lainnya]
- Bahasa: [Isi]
- Framework: [Isi]
- Database: [Isi atau Tidak ada]
- Deployment: [Isi]

## Menjalankan proyek
[Isi perintah instalasi, konfigurasi, development, build, dan test setelah stack dipilih.]

## Testing
Lengkapi `docs/TESTING.md` dan ikuti standar testing repository. CI mendeteksi
Node.js, Python, dan PHP berdasarkan manifest root; pastikan lockfile dan test command
tersedia sesuai stack.

## Konfigurasi dan keamanan
- Jangan commit secret, token, password, private key, atau data pribadi.
- Periksa hasil Gitleaks dan OSV-Scanner pada setiap PR.
- Dependabot template tersedia di `.github/dependabot.yml`; aktifkan hanya ecosystem
  yang memiliki manifest/lockfile pada direktori sesuai.
- Buat `SECURITY.md` khusus proyek sebelum menerima kontribusi publik.

## CI (GitHub Actions)
Workflow `.github/workflows/ci.yml` mencakup validasi struktur, JSON, Markdown,
whitespace, secret scanning, dependency scanning, dan test otomatis untuk Node.js,
Python, atau PHP. Workflow berjalan pada push ke `main`, pull request ke `main`,
jadwal mingguan, dan manual. Tambahkan job untuk stack lain.

## Kriteria selesai
- Kebutuhan dan acceptance criteria terpenuhi.
- Pemeriksaan/test relevan lulus.
- Tidak ada secret atau data sensitif di repository.
- Dokumentasi dan changelog diperbarui.
