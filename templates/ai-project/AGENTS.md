# Instruksi AI — [NAMA PROYEK]

## Urutan membaca
1. README.md
2. docs/PROJECT_BRIEF.md
3. docs/ARCHITECTURE.md
4. docs/TASKS.md
5. docs/TESTING.md (wajib sebelum implementasi fitur)
6. docs/DECISIONS.md dan docs/CHANGELOG.md bila relevan

## Aturan utama
- Pahami tujuan, batasan, dan acceptance criteria sebelum coding.
- Jika brief belum lengkap dan berdampak pada arsitektur, tanyakan klarifikasi.
- Jangan mengarang requirement, data, endpoint, kredensial, atau perilaku sistem.
- Periksa file dan pola yang sudah ada sebelum membuat perubahan.
- Pertahankan stack dan konvensi proyek kecuali ada alasan dan persetujuan.
- Hindari perubahan di luar scope task.
- Jangan menambahkan dependency tanpa menjelaskan manfaat dan dampaknya.
- Jangan commit secret, file environment asli, credential, atau data pengguna.
- Jangan menghapus data, menjalankan migrasi destruktif, atau mengubah layanan produksi tanpa izin eksplisit.
- Pisahkan data demo dari data produksi dan beri label dengan jelas.
- Jangan menandai task selesai jika belum diverifikasi.

## Alur setiap task
1. Nyatakan pemahaman dan file yang kemungkinan terdampak.
2. Periksa implementasi dan dependensi yang relevan.
3. Pecah pekerjaan menjadi langkah kecil.
4. Implementasikan perubahan terfokus.
5. Jalankan test, lint, build, atau pemeriksaan yang tersedia.
6. Tinjau diff dan potensi regresi.
7. Perbarui TASKS, CHANGELOG, atau dokumentasi bila perlu.

## Laporan setelah bekerja
Laporkan:
- Ringkasan perubahan.
- File yang dibuat/diubah.
- Perintah pemeriksaan dan hasilnya.
- Risiko, asumsi, atau hal yang belum selesai.

## Kualitas kode
- Pilih solusi sederhana, terbaca, dan mudah dirawat.
- Tangani error dan validasi input pada batas sistem.
- Jangan menyalin kode berulang jika abstraksi sederhana lebih tepat.
- Ikuti `docs/TESTING.md` dan standar repository `../../docs/TESTING_STANDARDS.md`.
- Tambahkan test untuk perilaku penting, batas input, akses ditolak, dan kasus gagal.
- Jangan menyatakan task selesai sebelum pemeriksaan relevan dijalankan atau blocker dicatat.
- Jangan mengubah format file massal tanpa kebutuhan.
