# Decisions — Preview

## 2026-11-09 — Website tetap static vanilla

- **Status:** Existing architecture documented (not a new implementation decision).
- **Konteks:** Source menggunakan HTML/CSS/JavaScript tanpa framework/build step yang terlihat.
- **Keputusan saat ini:** Pertahankan pendekatan static vanilla untuk perubahan rutin; dependency baru memerlukan alasan dan scope jelas.
- **Konsekuensi:** Deployment sederhana; validasi dan pengujian interaksi perlu mencakup browser manual atau E2E.

## 2026-11-09 — Data kampanye harus bersumber

- **Status:** Prinsip pengembangan.
- **Konteks:** README mengidentifikasi bagian profil sebagai placeholder.
- **Keputusan:** Jangan mengisi detail kandidat, klaim, statistik, atau foto dokumenter tanpa sumber/otorisasi.
- **Konsekuensi:** Placeholder dapat tetap terlihat sampai data sah tersedia; dokumentasi tidak boleh dianggap sebagai verifikasi fakta.

## 2026-11-09 — Pisahkan nama lengkap dan nama kampanye

- **Status:** Diterapkan berdasarkan informasi nama yang diberikan pemilik proyek.
- **Keputusan:** Gunakan **Slamet Purwanto** sebagai nama lengkap pada identitas profil dan metadata; pertahankan **SLAMET** sebagai nama kampanye/brand yang sudah digunakan pada logo teks, slogan, dan elemen visual utama.
- **Konsekuensi:** Perubahan nama lengkap tidak menghapus identitas kampanye yang telah dikenal. Jika kelak ada koreksi ejaan atau nama resmi, perbarui `candidate.fullName` di `js/data.js` serta salinan metadata statis di `index.html`.
