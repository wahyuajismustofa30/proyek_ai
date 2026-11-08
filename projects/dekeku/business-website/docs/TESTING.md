# Testing — DEKEKU Business Website

## Status
Proyek masih tahap persiapan; belum ada implementasi aplikasi. Test runtime belum dapat dijalankan.

## Strategi setelah implementasi
- **Unit:** validasi konten/konfigurasi, helper, komponen interaktif, dan logika formulir.
- **Integration:** pengiriman formulir, API/CRM atau kanal kontak yang benar-benar disetujui, serta penyimpanan data jika digunakan.
- **E2E:** navigasi halaman, CTA, form inquiry (valid/invalid/sukses/gagal), halaman tidak ditemukan, dan tampilan mobile.
- **Accessibility/visual:** keyboard-only, label form, semantic HTML, contrast, responsive mobile/desktop.
- **SEO/metadata:** title, description, canonical, sitemap/robots bila digunakan, link rusak, dan metadata sharing.
- **Security:** validasi server-side, spam/rate limit, sanitasi output, dan proteksi secret.

## Data dan environment
Gunakan konten dummy yang diberi label. Jangan mengirim inquiry ke kontak produksi atau menyimpan data calon pelanggan nyata selama test. Integrasi eksternal harus memakai sandbox/mock.

## Perintah
Belum ditetapkan karena stack belum dipilih. Setelah implementasi, dokumentasikan perintah install, lint/typecheck, unit/integration, E2E, dan build di sini dan README.

## Acceptance minimum sebelum rilis
- Alur utama dari landing page ke CTA berjalan.
- Form memiliki validasi dan state sukses/gagal yang jelas.
- Layout diuji pada viewport mobile dan desktop.
- Tidak ada link placeholder, data bisnis fiktif, atau secret.
- Pemeriksaan aksesibilitas dan SEO dasar dicatat.

## Pengecualian saat ini
Unit, integration, E2E, dan build berstatus NOT APPLICABLE / NOT RUN karena belum ada source aplikasi. Status ini bukan PASS. Perbarui dokumen ketika stack dan implementasi tersedia.
