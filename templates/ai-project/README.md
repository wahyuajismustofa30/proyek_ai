# [NAMA PROYEK]

> [Deskripsi singkat proyek dalam satu atau dua kalimat.]

Status: **Planning**
Versi: **0.1.0**
Pemilik: **[Nama/Tim]**
Diperbarui: **[YYYY-MM-DD]**

## Tujuan
[Jelaskan masalah yang ingin diselesaikan dan hasil yang diharapkan.]

## Mulai bekerja dengan AI
1. Baca AGENTS.md.
2. Lengkapi docs/PROJECT_BRIEF.md.
3. Periksa docs/ARCHITECTURE.md dan docs/TASKS.md.
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
Lengkapi docs/TESTING.md dan ikuti standar testing repository. CI root mendeteksi
manifest Node.js, Python, dan PHP di folder proyek. Pastikan lockfile dan test command
tersedia sesuai stack.

## Konfigurasi dan keamanan
- Jangan commit secret, token, password, private key, atau data pribadi.
- Periksa hasil Gitleaks dan OSV-Scanner pada setiap PR.
- Dependency proyek dipantau oleh Dependabot root melalui pola /projects/*.
- Buat SECURITY.md khusus proyek sebelum menerima kontribusi publik.

## CI monorepo
CI dan Dependabot dikelola oleh repository root, bukan oleh workflow di folder proyek.
Jangan menambahkan .github/workflows/ci.yml atau .github/dependabot.yml di proyek
monorepo. Workflow root .github/workflows/project-matrix.yml akan mendeteksi manifest
dan menjalankan test stack yang didukung. Baca docs/MONOREPO_CI.md di repository induk.

## Kriteria selesai
- Kebutuhan dan acceptance criteria terpenuhi.
- Pemeriksaan/test relevan lulus.
- Tidak ada secret atau data sensitif di repository.
- Dokumentasi dan changelog diperbarui.
