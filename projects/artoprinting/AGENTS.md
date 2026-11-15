# Instruksi Pengembangan ARTO PRINTING

Instruksi ini berlaku untuk seluruh pekerjaan di `projects/artoprinting/`. Ikuti juga `AGENTS.md` di root repository.

## 1. Master Theme adalah standar wajib

Seluruh pengembangan, perbaikan, debugging, refactoring, dan pemeliharaan antarmuka ARTO PRINTING WAJIB merujuk pada Master Theme yang sudah tersedia.

Master Theme merupakan sumber standar visual dan pola komponen proyek. Jangan membuat tema, design system, token, atau pola komponen alternatif yang menduplikasi atau bertentangan dengannya.

Sebelum mengubah UI, periksa implementasi aktual pada:

- `master-theme.html` — showcase dan referensi visual komponen.
- `assets/css/base.css` — sumber kebenaran tema: token, warna, tipografi, spacing, radius, surface, tombol, dan utilitas.
- `assets/css/layout.css` — layout global.
- `assets/css/components.css` — komponen lintas halaman.
- `assets/css/pages/` — penyesuaian khusus halaman.
- `assets/js/components/interaction-primitives.js` dan `state-primitives.js` — perilaku interaksi dan state reusable.

Periksa file dan API yang benar-benar tersedia sebelum menggunakannya. Jangan mengasumsikan nama class, token, selector, atau fungsi yang belum diverifikasi.

## 2. Prioritas penggunaan ulang

Sebelum membuat implementasi baru:

1. Periksa apakah pola atau komponen yang dibutuhkan sudah ada di Master Theme.
2. Gunakan token, class, markup, dan API yang tersedia.
3. Jika perlu variasi, perluas komponen yang ada dengan cara yang konsisten dan tidak merusak pemakaian lain.
4. Buat komponen atau aturan baru hanya jika kebutuhan belum dapat dipenuhi oleh implementasi yang tersedia.

Jangan menyalin CSS atau JavaScript komponen bersama ke stylesheet atau script halaman. Showcase `master-theme.html` adalah referensi implementasi, bukan sumber untuk menduplikasi CSS komponennya.

## 3. Konsistensi visual

Semua halaman dan komponen wajib mengikuti standar Master Theme, termasuk:

- Identitas merek, palet warna, dan semantic color token.
- Tipografi, hierarki heading, dan keterbacaan.
- Skala spacing, ukuran, border, radius, dan shadow.
- Tombol, tautan, formulir, navigasi, breadcrumb, card, badge, dan komponen interaktif.
- Empty, loading, error, dan success state.
- Responsive behavior untuk mobile hingga desktop.
- Fokus keyboard, kontras, nama aksesibel, semantik HTML, dan reduced motion.

Gunakan token semantik yang sudah tersedia, misalnya token warna brand, text, surface, border, dan focus. Hindari nilai warna atau ukuran hardcoded jika token yang sesuai sudah tersedia.

## 4. Pembagian tanggung jawab file

Pertahankan pembagian tanggung jawab yang sudah digunakan proyek:

- `assets/css/base.css`: fondasi dan token tema.
- `assets/css/layout.css`: layout global.
- `assets/css/components.css`: komponen lintas halaman.
- `assets/css/pages/<halaman>.css`: kebutuhan unik halaman.
- `assets/js/components/`: perilaku komponen reusable.
- `assets/js/pages/` dan `assets/js/features/`: logika halaman dan fitur sesuai arsitektur yang ada.

Jangan memindahkan aturan global ke stylesheet halaman untuk menyelesaikan masalah lokal. Jangan membuat file, dependensi, atau lapisan abstraksi baru tanpa kebutuhan teknis yang jelas.

## 5. Aksesibilitas dan perilaku komponen

Pertahankan semantik dan perilaku aksesibilitas Master Theme. Contoh:

- Breadcrumb menggunakan pola `.ui-breadcrumb`, elemen `nav` berlabel, dan `aria-current="page"` sesuai struktur yang berlaku.
- Skip link tetap tersedia untuk pengguna keyboard; boleh disembunyikan secara visual saat tidak fokus, tetapi jangan dihapus atau dibuat tidak dapat dijangkau.
- Navigasi menggunakan tautan; aksi menggunakan tombol.
- Formulir memiliki label yang terhubung dengan kontrol.
- Status dinyatakan secara semantik dan tidak mengandalkan warna saja.
- Komponen interaktif harus mendukung keyboard dan fokus yang terlihat.

Periksa markup, selector, dan API aktual pada Master Theme sebelum mengubah komponen terkait.

## 6. Perubahan fondasi tema

Jangan mengubah token, komponen global, atau standar Master Theme hanya untuk menyelesaikan masalah satu halaman.

Jika perubahan fondasi memang diperlukan:

1. Jelaskan kebutuhan dan alasan teknisnya.
2. Periksa semua pemakaian token atau komponen yang terdampak.
3. Pilih perubahan sekecil mungkin.
4. Validasi halaman lain yang menggunakan fondasi tersebut.
5. Perbarui showcase Master Theme bila perilaku atau standar komponen berubah.

Variasi halaman diperbolehkan hanya jika memiliki kebutuhan fungsional yang jelas dan tetap konsisten dengan fondasi Master Theme.

## 7. Validasi setiap perubahan UI

Sebelum pekerjaan dinyatakan selesai:

- Cocokkan hasil dengan showcase dan standar Master Theme.
- Periksa penggunaan ulang token dan komponen.
- Periksa duplikasi atau override CSS/JavaScript.
- Uji tampilan mobile dan desktop yang relevan.
- Periksa kontras, fokus keyboard, semantik, dan aksesibilitas.
- Periksa dampak regresi pada halaman lain yang menggunakan komponen bersama.

Laporkan pemeriksaan yang benar-benar dijalankan. Bedakan PASS, NOTICE, FAIL, dan NOT RUN sesuai instruksi root repository.

## 8. Aturan mutlak

**Jangan membuat desain atau komponen sendiri ketika standar atau implementasi yang sesuai sudah tersedia di Master Theme. Selalu periksa, gunakan, dan kembangkan standar yang sudah ada terlebih dahulu.**

Aturan ini berlaku untuk seluruh halaman, blog, artikel, header, footer, navigasi, breadcrumb, formulir, tombol, komponen interaktif, responsive layout, dan pekerjaan UI ARTO PRINTING lainnya.
