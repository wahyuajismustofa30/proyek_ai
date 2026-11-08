# Audit Visual Aset Maskot DEKEKU — Baseline v1.1

Tanggal audit: 2026-11-08  
Sumber: paket `Master-tema-dekeku-v1.1.zip` dan salinan baseline di `versions/v1.1/source/Dekeku/`.  
Cakupan: seluruh 20 file visual maskot (10 SVG dan 10 PNG) serta skrip pembangkit PNG/SVG.

> Baseline v1.1 diperlakukan sebagai sumber read-only. Temuan dan perbaikan harus dicatat di luar source baseline; jangan menimpa aset asli.

## Ringkasan

**Temuan kritis: seluruh PNG tidak valid secara visual.**

- 10 SVG (5 ekspresi × 2 varian warna) berhasil dirender dan ditinjau.
- 10 PNG memiliki ukuran file, dimensi, dan SHA-256 yang identik. Semua berukuran 2.506 byte dengan dimensi 512 × 389; SHA-256: `e406ef3e5808f1c3336a06be0b44937790b30d3a9caf7f0f12146094c453562d`.
- Pemeriksaan visual PNG memperlihatkan hasil screenshot ikon gambar rusak/placeholder, bukan maskot. Jadi file PNG saat ini tidak boleh digunakan di website, undangan, UI, atau materi promosi.
- SVG menunjukkan lima keadaan ekspresi yang konsisten dan tersedia dalam versi gelap serta putih.

## Inventaris dan hasil visual

| Ekspresi | SVG gelap | SVG putih | Penilaian |
|---|---|---|---|
| Polos | Ada | Ada | Siluet tanpa fitur wajah; cocok sebagai keadaan netral/placeholder |
| Mikir | Ada | Ada | Mata kecil dan mulut garis; terbaca sebagai berpikir |
| Senang | Ada | Ada | Mata tertutup tersenyum; ekspresi ramah dan ringan |
| Oops | Ada | Ada | Mata terbuka, mulut terbuka, dan tetes keringat; terbaca sebagai kaget/keliru |
| Sukses | Ada | Ada | Mata tertutup dan senyum terbuka; cocok untuk konfirmasi berhasil |

### Kualitas visual SVG

- Siluet utama, lubang wajah, dan dua elemen kotak piksel konsisten di seluruh varian.
- Ekspresi ditempatkan mengikuti kemiringan wajah; tidak terlihat keluar dari area wajah pada hasil render audit.
- Varian gelap memakai `#0C0C0C`, varian putih memakai `#FFFFFF`.
- SVG memiliki `viewBox`, `role="img"`, `aria-label`, dan `title`.
- Varian putih harus ditempatkan pada latar gelap/berwarna. Pada latar putih atau transparan di atas putih, maskot putih akan kehilangan kontras.
- Komposisi cukup lebar (viewBox 1296.3 × 984.7; rasio sekitar 1.316:1), bukan kanvas persegi. Jangan menganggap nama PNG berakhiran `512` berarti 512 × 512.

## Temuan dan tingkat prioritas

### P0 — Hentikan penggunaan seluruh PNG saat ini

Semua 10 PNG identik byte-for-byte, termasuk file yang seharusnya berbeda ekspresi dan warna. Hasil inspeksi menunjukkan konten placeholder/broken-image, bukan hasil ekspor maskot. Ini bukan sekadar duplikasi yang aman: seluruh varian raster tidak dapat dipercaya.

**Tindakan:** jangan gunakan PNG yang ada. Pertahankan file baseline untuk jejak audit, lalu hasilkan ulang pada versi aset baru setelah proses ekspor diperbaiki dan diverifikasi.

### P1 — Perbaiki proses ekspor PNG

Skrip `scripts/build_maskot.py` membuat halaman dengan elemen `<img src="file://...">` melalui `page.set_content()`, lalu mengambil screenshot. Pola ini berisiko gagal memuat file lokal dari origin halaman `about:blank`; hasil screenshot placeholder dapat tersimpan tanpa terdeteksi.

**Arah perbaikan yang disarankan untuk versi berikutnya:**
1. Render SVG langsung sebagai inline markup pada halaman, atau navigasikan browser ke URI file lokal yang valid.
2. Tunggu event `load` dan pastikan tidak ada `pageerror`/request gagal.
3. Verifikasi bahwa gambar memiliki area piksel non-transparan yang memadai dan bukan placeholder browser.
4. Validasi dimensi, alpha/transparansi, variasi hash antar ekspresi, serta perbedaan warna antara versi gelap dan putih.
5. Buat PNG untuk seluruh 10 varian; hentikan build dengan exit code gagal jika salah satu validasi tidak terpenuhi.

### P2 — Tambahkan bukti penggunaan dan aturan latar

- Dokumentasikan contoh latar yang direkomendasikan untuk SVG gelap dan putih.
- Uji ukuran kecil (ikon/komponen UI), ukuran sedang (kartu/section), dan ukuran besar (hero/ilustrasi).
- Pastikan ekspresi tetap terbaca pada tampilan mobile dan tidak terpotong oleh container.
- Gunakan SVG sebagai format utama selama PNG hasil ekspor belum lolos validasi.

## Matriks penggunaan yang disarankan

| Ekspresi | Konteks yang cocok |
|---|---|
| Polos | Avatar netral, placeholder, keadaan awal |
| Mikir | Loading non-teknis, proses berpikir, tips |
| Senang | Sapaan, konten positif, empty state yang ramah |
| Oops | Error ringan, input keliru, halaman tidak ditemukan |
| Sukses | Form berhasil, RSVP berhasil, konfirmasi selesai |

Jangan gunakan maskot sebagai satu-satunya penyampai status penting; tetap tampilkan teks status yang jelas.

## Checklist sebelum aset versi baru dirilis

- [ ] 10 SVG lolos parse dan render.
- [ ] 10 PNG benar-benar menampilkan maskot, bukan placeholder.
- [ ] Hash antar ekspresi/varian berbeda sesuai isi visual yang diharapkan.
- [ ] Dimensi dan rasio dicatat secara eksplisit.
- [ ] Transparansi terjaga; tidak ada latar putih/hitam yang tidak disengaja.
- [ ] Varian gelap diuji di latar terang dan varian putih diuji di latar gelap.
- [ ] Ekspresi terbaca pada ukuran mobile dan desktop.
- [ ] Skrip build gagal jika aset tidak termuat atau hasil raster identik secara tidak wajar.
- [ ] Baseline v1.1 tetap tidak berubah; hasil perbaikan disimpan sebagai versi baru.

## Keputusan audit

**SVG: layak digunakan sebagai aset utama dengan aturan kontras latar.**  
**PNG: tidak layak digunakan; seluruh varian perlu diekspor ulang dan divalidasi.**

Audit ini memeriksa aset baseline dan skrip pembangkitnya. Audit belum mencakup integrasi aktual pada semua halaman website/undangan DEKEKU.
