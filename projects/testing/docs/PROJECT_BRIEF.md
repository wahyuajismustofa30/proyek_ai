# Project Brief — Testing Web Page Lab

## 1. Ringkasan

- Nama proyek: Testing
- Deskripsi: proyek uji untuk membuat halaman web statis dan memverifikasi kualitas dasarnya.
- Pemilik: Wahyu
- Tanggal: 2026-11-09
- Status: Active — Test Project

## 2. Masalah dan tujuan

**Masalah:** Repository memerlukan proyek web nyata untuk menguji jalur discovery CI, validasi web, serta test aplikasi pada proyek yang memiliki manifest stack.

**Tujuan utama:**

- Menyediakan halaman contoh yang bisa dijalankan lokal.
- Menguji HTML, CSS, aset lokal, dan interaksi JavaScript.
- Menjadi baseline untuk eksperimen pembuatan halaman web berikutnya.

**Indikator keberhasilan:**

- Halaman dapat dibuka melalui server statis lokal.
- Referensi aset lokal valid.
- Test otomatis Node.js lulus.
- CI mendeteksi proyek dan menjalankan web validation serta Node tests.

## 3. Pengguna dan skenario

**Target pengguna:** pemilik repository dan kontributor yang menguji alur pembuatan web.

**Skenario utama:**

1. Kontributor menjalankan halaman secara lokal untuk memeriksa hasil.
2. Kontributor mengubah komponen halaman dan menjalankan test untuk mencegah regresi.

## 4. Ruang lingkup

**Termasuk:**

- Satu landing page responsif.
- Navigasi mobile.
- Formulir demo dengan validasi email lokal.
- Unit test untuk kontrak halaman dan helper JavaScript.
- Validasi otomatis HTML, CSS, SVG, dan aset lokal oleh CI root.

**Tidak termasuk:**

- Backend, database, autentikasi, pembayaran, analytics, atau deployment produksi.
- Pengiriman atau penyimpanan data formulir.
- Visual regression dan browser automation lintas-browser.

## 5. Fitur dan prioritas

| ID | Fitur | Prioritas | Kriteria penerimaan |
|---|---|---|---|
| F-001 | Landing page semantik | Must | Memiliki title, lang, landmark, dan viewport |
| F-002 | Layout responsif | Must | CSS memiliki breakpoint untuk layar kecil |
| F-003 | Navigasi mobile | Must | Tombol mengubah status menu dan aria-expanded |
| F-004 | Form demo | Should | Email divalidasi lokal dan hasil diumumkan melalui live region |
| F-005 | Test otomatis | Must | `npm test` lulus tanpa dependency eksternal |

## 6. Platform dan batasan

- Platform: browser desktop dan mobile modern.
- Bahasa: Indonesia.
- Aksesibilitas: semantic HTML, label input, keyboard focus, skip link, dan status aria-live.
- Hosting/server: server statis lokal; tidak ada konfigurasi produksi.
- Integrasi eksternal: tidak ada.

## 7. Data dan integrasi

- Data yang disimpan: tidak ada.
- Form hanya memproses nilai di browser dan tidak mengirim request.
- Aset: SVG lokal.

## 8. Keamanan dan privasi

- Tidak ada autentikasi atau data sensitif.
- Jangan memasukkan data pribadi nyata pada test.
- Client-side validation bukan pengganti validasi server untuk aplikasi produksi.

## 9. Konten dan desain

- Gaya: halaman demo modern, sederhana, responsif.
- Brand: identitas visual generik khusus proyek testing; bukan aset brand eksternal.
- Semua teks merupakan konten contoh.

## 10. Definisi selesai

- [x] Scope demo dan acceptance criteria ditetapkan.
- [ ] Test otomatis dan validasi CI lulus.
- [ ] Review manual pada viewport desktop dan mobile.
- [ ] Dokumentasi diperbarui.
- [x] Tidak ada secret atau data nyata.

## 11. Pertanyaan terbuka

| Pertanyaan | Dampak | Status |
|---|---|---|
| Perlu browser automation? | Menambah biaya dependency dan waktu CI | Ditunda sampai diperlukan |
