# Instruksi untuk AI Agent

## Wajib sebelum bekerja

1. Baca README.md di root.
2. Baca docs/PROJECT_INDEX.md.
3. Baca README proyek yang sedang dikerjakan.
4. Baca instruksi lokal (AGENTS.md) pada folder target jika tersedia.
5. Periksa struktur dan isi file yang ada sebelum mengedit.

## Aturan perubahan

- Jangan mengubah atau menghapus arsip versi yang sudah ditetapkan sebagai baseline.
- Jangan melakukan refactor luas jika tugas hanya meminta perubahan kecil.
- Pertahankan kompatibilitas nama file, path, token, dan aset kecuali diminta.
- Jangan mengganti aset brand dengan placeholder atau aset hasil tebakan.
- Jangan membuat data fiktif seolah data nyata (harga, testimoni, alamat, nomor WhatsApp, statistik).
- Pisahkan demo dari implementasi produksi dan tandai placeholder secara jelas.
- Hindari menambahkan dependency jika solusi sederhana sudah cukup.
- Jangan menyimpan secret, token, password, private key, atau file .env berisi kredensial.
- Jangan mengubah konfigurasi deployment/produksi tanpa instruksi eksplisit.

## Alur kerja

1. Nyatakan pemahaman singkat tentang tugas dan file yang akan terdampak.
2. Periksa dependensi dan konvensi yang sudah ada.
3. Buat perubahan terfokus.
4. Jalankan pemeriksaan yang relevan (lint, build, test, validasi JSON, atau pemeriksaan manual).
5. Laporkan file yang berubah, hasil verifikasi, risiko, dan pekerjaan lanjutan.

## Dokumentasi

- Setiap proyek memiliki README sendiri.
- Setiap versi desain/tema memiliki catatan perubahan.
- Perubahan keputusan arsitektur penting dicatat di docs/DECISIONS.md.
