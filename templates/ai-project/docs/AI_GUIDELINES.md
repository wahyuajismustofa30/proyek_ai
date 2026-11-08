# Panduan Pengembangan Proyek AI

Panduan ini berlaku untuk proyek yang memakai model, prompt, atau output
generatif. Sesuaikan prosedur dengan risiko dan kebijakan data proyek.

## Prompt dan versioning

- Simpan prompt sistem, template prompt, instruksi, dan konfigurasi evaluasi
  sebagai file teks berversi di repository.
- Beri nama/ID dan versi yang stabil; catat perubahan perilaku penting di
  changelog atau catatan keputusan.
- Pisahkan prompt produksi dari eksperimen. Jangan menaruh prompt yang berisi
  secret, data pribadi, atau data pelanggan.
- Review perubahan prompt seperti perubahan kode: jelaskan tujuan, dampak,
  contoh input/output sintetis, dan hasil evaluasi.

## Evaluasi model dan output

- Tetapkan kriteria evaluasi sebelum memilih atau mengganti model: akurasi,
  relevansi, konsistensi, keamanan, latensi, dan biaya sesuai kebutuhan.
- Simpan dataset evaluasi sintetis atau yang telah dianonimkan; jangan
  memasukkan data pribadi/produksi tanpa dasar dan persetujuan yang sah.
- Uji kasus normal, edge case, prompt injection, output tidak valid, dan
  penolakan yang diharapkan.
- Catat hasil evaluasi dan regresi saat prompt, model, parameter, atau pipeline
  berubah. Lakukan review manusia untuk output berisiko tinggi.

## API key dan secret

- Simpan API key hanya pada file `.env` lokal yang diabaikan Git atau secret
  manager/environment variable pada runtime.
- Jangan pernah menaruh API key di Git, prompt, source code, dokumentasi,
  fixture, log, screenshot, atau output model.
- Sediakan nama variabel tanpa nilai rahasia di `.env.example`. Rotasi key
  segera jika terpapar dan periksa log/riwayat sesuai prosedur keamanan proyek.

## Pencatatan model dan versi

Untuk setiap integrasi/evaluasi, catat provider, nama/ID model, versi atau
snapshot jika tersedia, tanggal penggunaan, parameter penting (misalnya
temperature dan max output), versi prompt, serta versi kode/dataset evaluasi.
Jangan mengklaim versi model tetap jika provider hanya menawarkan alias dinamis.

## Data pribadi dan batas penggunaan

- Minimalkan data yang dikirim ke provider; gunakan data sintetis atau
  anonim untuk pengembangan dan pengujian.
- Jangan mengirim data pribadi sensitif, rahasia, kredensial, atau data pihak
  ketiga tanpa dasar pemrosesan, otorisasi, dan kontrol yang disetujui.
- Tetapkan retensi, akses, redaksi log, dan penghapusan data sesuai kebijakan
  proyek serta ketentuan hukum yang berlaku.
- Jangan menganggap output model benar atau aman secara otomatis. Verifikasi
  fakta, batasi tindakan otomatis, dan sediakan eskalasi manusia sesuai risiko.
