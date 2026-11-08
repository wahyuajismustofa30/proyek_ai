# Instruksi AI — [NAMA PROYEK]

## Urutan membaca
1. README.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/TASKS.md
5. docs/AI_GUIDELINES.md (wajib untuk fitur berbasis AI/model)
6. docs/TESTING.md (wajib sebelum implementasi fitur)
7. docs/DECISIONS.md dan docs/CHANGELOG.md bila relevan

## Aturan utama
- Pahami tujuan, batasan, dan acceptance criteria sebelum coding.
- Jika brief belum lengkap dan berdampak pada arsitektur, tanyakan klarifikasi.
- Jangan mengarang requirement, data, endpoint, kredensial, atau perilaku sistem.
- Periksa file dan pola yang sudah ada sebelum membuat perubahan.
- Pertahankan stack dan konvensi proyek kecuali ada alasan dan persetujuan.
- Hindari perubahan di luar scope task.
- Jangan menambahkan dependency tanpa menjelaskan manfaat, risiko, dan dampaknya.
- Jangan commit secret, file environment asli, credential, atau data pengguna.
- Jangan menyalin data produksi ke fixture, log, screenshot, atau dokumentasi.
- Jangan menghapus data, menjalankan migrasi destruktif, atau mengubah layanan produksi tanpa izin eksplisit.
- Pisahkan data demo dari data produksi dan beri label dengan jelas.
- Jangan menandai task selesai jika belum diverifikasi.

## Alur setiap task
1. Nyatakan pemahaman dan file yang kemungkinan terdampak.
2. Periksa implementasi, dependency, dan risiko keamanan yang relevan.
3. Pecah pekerjaan menjadi langkah kecil.
4. Implementasikan perubahan terfokus.
5. Jalankan test, lint, build, dan pemeriksaan keamanan yang tersedia.
6. Tinjau diff, permission, input validation, dan potensi regresi.
7. Perbarui TASKS, CHANGELOG, atau dokumentasi bila perlu.

## Laporan setelah bekerja
Laporkan ringkasan perubahan, file yang diubah, perintah pemeriksaan dan hasilnya,
risiko/asumsi, serta pekerjaan yang belum selesai.

## Kualitas dan keamanan kode
- Pilih solusi sederhana, terbaca, dan mudah dirawat.
- Tangani error dan validasi input pada batas sistem.
- Periksa otorisasi di sisi server; jangan mengandalkan kontrol UI.
- Tambahkan test untuk alur normal, input batas, akses ditolak, dan kasus gagal.
- Ikuti docs/TESTING.md dan jangan gunakan layanan/data produksi saat testing.
- Jangan menambah permission workflow GitHub Actions tanpa alasan eksplisit.
- Pin GitHub Actions ke full commit SHA dan beri komentar versi rilis.
- Jangan gunakan pull_request_target untuk menjalankan kode kontribusi yang tidak dipercaya.
- Jangan menyatakan task selesai sebelum pemeriksaan relevan dijalankan atau blocker dicatat.
