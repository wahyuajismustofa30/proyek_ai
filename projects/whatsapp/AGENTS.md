# AGENTS.md — WHATSAPP PROJECT

## 1. IDENTITAS DAN RUANG LINGKUP

Dokumen ini mengatur pekerjaan AI coding agent, developer, dan kontributor pada `projects/whatsapp/` dalam repository `wahyuajismustofa30/proyek_ai`.

Fokus proyek:

- Integrasi GoWA.
- Webhook WhatsApp.
- Gemini AI dan provider AI lainnya.
- OWNER assistant.
- CUSTOMER assistant DEKEKU.
- Otomasi dan pengembangan layanan WhatsApp.

Instruksi `AGENTS.md` root repository tetap berlaku. Instruksi ini melengkapi dan memperketat aturan untuk proyek WhatsApp.

Gunakan bahasa Indonesia untuk dokumentasi dan komunikasi teknis.

## 2. ARSITEKTUR DAN IMPLEMENTASI

Berdasarkan implementasi yang ditemukan saat penyusunan dokumen:

- `gowa-gemini-bridge/index.js`: HTTP server, webhook, autentikasi signature, validasi payload, routing pesan, deduplikasi, dan pengendalian DRY-RUN.
- `gowa-gemini-bridge/gemini.js`: integrasi Gemini API, system prompt, validasi input, conversation history, timeout, dan parsing respons.
- `gowa-gemini-bridge/package.json`: konfigurasi proyek Node.js CommonJS.
- `gowa/`: runtime/repository GoWA yang dikecualikan dari Git.

Struktur dapat berkembang. Selalu periksa file aktual sebelum mengubah atau mendokumentasikan arsitektur.

Jangan menganggap fitur yang belum diimplementasikan sebagai fitur aktif.

## 3. PRINSIP PENGEMBANGAN

- Terapkan minimal change.
- Pertahankan kompatibilitas.
- Gunakan modul dengan tanggung jawab yang jelas.
- Hindari dependency yang tidak diperlukan.
- Pisahkan konfigurasi, integrasi provider, pemrosesan webhook, dan business logic.
- Jangan melakukan refactoring besar tanpa kebutuhan dan persetujuan.
- Jangan mengubah file di luar ruang lingkup pekerjaan.

Setiap perubahan harus memiliki alasan teknis dan dapat diverifikasi.

## 4. KEAMANAN DAN PRIVASI

Keamanan dan isolasi data merupakan persyaratan wajib.

- Simpan secret hanya dalam environment atau penyimpanan rahasia.
- Jangan memasukkan API key, token, password, session, atau data sensitif ke Git.
- Pertahankan `.env` dan kredensial dalam pengecualian Git.
- Validasi semua input eksternal.
- Verifikasi signature webhook menggunakan HMAC dan constant-time comparison.
- Batasi ukuran request dan waktu pemrosesan.
- Tangani pesan duplikat dan replay.
- Hindari kebocoran isi pesan dan data pribadi melalui log.
- Jangan mengungkap data OWNER kepada CUSTOMER.
- Jangan menggunakan data satu pelanggan untuk percakapan pelanggan lain.

Jangan melemahkan autentikasi atau validasi demi kemudahan integrasi.

## 5. INTEGRASI GoWA

GoWA merupakan gateway WhatsApp utama.

Sebelum mengubah integrasi, periksa source code GoWA yang benar-benar digunakan.

Verifikasi:

- Endpoint dan autentikasi.
- Struktur payload webhook.
- Identitas device dan akun.
- Event dan identitas pesan.
- Format signature.
- Mekanisme pengiriman pesan.
- Respons, error, dan retry.

Jangan mengarang endpoint, field, atau format payload.

Bedakan `OWNER_JID` dengan `GOWA_DEVICE_ID`. Jangan menyamakan keduanya sebelum kontrak payload membuktikannya.

Setiap perubahan kontrak integrasi harus disertai pengujian kompatibilitas.

## 6. INTEGRASI AI

Integrasi AI harus modular dan memungkinkan pergantian provider.

Wajib memperhatikan:

- API key dan konfigurasi rahasia.
- Timeout dan pembatalan request.
- Validasi respons.
- Batas input dan output.
- Penggunaan token.
- Penanganan kegagalan provider.
- Pengelolaan conversation history.
- Pengendalian request bersamaan.

Pisahkan secara ketat:

- OWNER: asisten pribadi pemilik.
- CUSTOMER: asisten layanan pelanggan DEKEKU.

Pisahkan system prompt, history, identitas percakapan, dan data kedua jalur.

AI tidak boleh mengarang harga, fitur, kebijakan, atau informasi bisnis yang belum terverifikasi.

## 7. WEBHOOK DAN PEMROSESAN PESAN

Setiap webhook harus:

- Memverifikasi signature sebelum memproses payload.
- Memvalidasi tipe dan struktur data.
- Menolak payload tidak valid.
- Membatasi ukuran request.
- Memiliki batas waktu pemrosesan.
- Menangani duplikasi dan pesan yang sedang diproses.
- Menghindari pemrosesan bersamaan yang tidak terkendali.
- Menggunakan retry terbatas untuk kegagalan sementara jika diperlukan.

Bedakan kegagalan permanen dan sementara. Retry harus mempertimbangkan idempotensi agar tidak menghasilkan pesan ganda.

Evaluasi kebutuhan penyimpanan persisten untuk deduplikasi dan history jika sistem berkembang.

## 8. MODE OPERASIONAL

Gunakan tahapan:

1. DEVELOPMENT
2. DRY-RUN
3. STAGING
4. LIMITED PRODUCTION
5. PRODUCTION

DRY-RUN adalah mode default.

Pengiriman pesan WhatsApp aktual hanya boleh diaktifkan setelah pengujian memadai dan persetujuan eksplisit pemilik.

Jangan mengubah mode operasional, webhook produksi, atau mekanisme pengiriman tanpa instruksi.

## 9. SERVER DAN LAYANAN PRODUKSI

Lingkungan utama adalah HG680P dengan Armbian ARM64 dan sumber daya terbatas.

Utamakan efisiensi RAM, CPU, storage, dan jumlah proses.

Dilarang tanpa persetujuan:

- Reboot server.
- Menghentikan GoWA, aaPanel, Nginx, atau Cloudflare Tunnel.
- Mengubah jaringan, firewall, port, dan konfigurasi tunnel.
- Mengubah konfigurasi layanan produksi.
- Memasang atau menghapus software sistem.

Pengujian harus dilakukan secara terisolasi dan tidak mengganggu layanan lain.

## 10. PENGUJIAN DAN VERIFIKASI

Sesuaikan pengujian dengan risiko perubahan.

Pertimbangkan:

- Pemeriksaan sintaks.
- Unit test.
- Integration test.
- Validasi signature.
- Payload tidak valid.
- Batas ukuran request.
- Pesan duplikat.
- Pemrosesan bersamaan.
- Timeout dan kegagalan provider.
- Isolasi OWNER dan CUSTOMER.
- Regression test.

Jangan mengklaim test berhasil jika belum dijalankan.

Bedakan PASS, FAIL, NOTICE, dan NOT RUN.

Script test yang masih placeholder bukan bukti bahwa proyek telah memiliki test otomatis.

## 11. GIT DAN GITHUB

- Periksa branch, commit, status, dan diff sebelum bekerja.
- Pertahankan perubahan lokal pengguna.
- Jangan menghapus atau menimpa file tanpa persetujuan.
- Jangan memasukkan secret ke repository.
- Jangan commit, push, merge, atau mengubah branch tanpa instruksi eksplisit.
- Jangan force push atau mengubah riwayat Git.
- Jangan mengubah branch protection tanpa persetujuan.

Patuhi instruksi root repository dan batas perubahan khusus proyek ini.

## 12. DOKUMENTASI

Dokumentasikan:

- Arsitektur aktual.
- Konfigurasi tanpa nilai rahasia.
- Kontrak integrasi.
- Prosedur instalasi dan pengujian.
- Mode operasional.
- Risiko dan batasan.
- Perubahan perilaku sistem.

Bedakan fitur aktif, fitur belum tersedia, dan rencana pengembangan.

Jangan mendokumentasikan asumsi sebagai fakta.

## 13. PROSEDUR KERJA

Gunakan alur:

1. AUDIT — periksa kode, dependensi, Git, dan dampak.
2. PLAN — susun solusi dan ruang lingkup.
3. APPROVAL — minta persetujuan jika diperlukan.
4. IMPLEMENT — lakukan perubahan minimal.
5. TEST — jalankan validasi relevan.
6. REVIEW — periksa diff dan keamanan.
7. REPORT — laporkan hasil dan risiko.

Audit dan analisis tidak boleh mengubah file.

Jika pekerjaan berisiko atau informasi belum cukup, berhenti pada tahap pemeriksaan dan minta hasil atau persetujuan pengguna.

## 14. FORMAT LAPORAN

Laporan pekerjaan penting harus mencakup:

- Tujuan.
- File diperiksa.
- File diubah.
- Temuan dan alasan teknis.
- Hasil pengujian.
- Risiko tersisa.
- Status Git.
- Langkah lanjutan.

Jangan mengklaim perubahan atau pengujian berhasil tanpa verifikasi.

## 15. ATURAN UTAMA

Keamanan dan privasi adalah prioritas tertinggi, diikuti stabilitas layanan produksi, kebenaran integrasi GoWA, keandalan pemrosesan pesan, keandalan AI, efisiensi sumber daya, dan kemudahan pemeliharaan.

Jangan melakukan perubahan yang tidak diminta. Jangan menjalankan tindakan destruktif tanpa persetujuan. Setiap perubahan harus memiliki ruang lingkup jelas, alasan teknis, dan hasil yang dapat diverifikasi.
