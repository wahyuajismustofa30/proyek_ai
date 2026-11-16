# Product Requirements Document (PRD)

**Produk:** Family Platform (codename)\
**Versi:** 1.0\
**Status:** Baseline

## 1. Ringkasan produk

Family Platform adalah aplikasi web privat untuk membantu dua pengguna
mengelola aktivitas personal, keluarga, dan bisnis. Platform dimulai
dari sistem keuangan keluarga, kemudian berkembang menjadi manajemen
rumah tangga, perencanaan, proyek, dokumen, aset, dan operasional
bisnis.

Produk bukan aplikasi akuntansi publik atau SaaS pada tahap awal.
Prioritasnya adalah penggunaan internal, keandalan data, kemudahan
pencatatan melalui ponsel, dan kemampuan audit.

## 2. Masalah yang ingin diselesaikan

-   Catatan keuangan tersebar di beberapa tempat.
-   Sulit mengetahui siapa yang membuat atau mengubah catatan.
-   Keuangan pribadi, keluarga, dan bisnis berisiko tercampur.
-   Dokumen, agenda, tugas, dan informasi operasional tidak terpusat.
-   Laporan dan evaluasi membutuhkan pekerjaan manual.

## 3. Tujuan produk

1.  Menyatukan aktivitas personal, keluarga, dan bisnis dalam satu
    platform.
2.  Memastikan data antar-workspace terisolasi.
3.  Menyediakan pencatatan keuangan yang dapat ditelusuri.
4.  Menyediakan fondasi modul yang dapat ditambah tanpa merombak core.
5.  Memberikan pengalaman yang nyaman di ponsel dan desktop.

## 4. Bukan tujuan tahap awal

-   Membuka pendaftaran publik atau menjadi SaaS multi-pelanggan.
-   Mengakses rekening bank secara otomatis.
-   Melakukan pembayaran atau transfer uang sungguhan.
-   Aplikasi Android/iOS native.
-   Microservices, Kubernetes, atau event streaming eksternal.
-   AI yang dapat mengubah data tanpa persetujuan pengguna.
-   Menggantikan software akuntansi pajak atau sistem perbankan.

## 5. Pengguna dan peran

### Pengguna awal

-   Pengguna A: suami.
-   Pengguna B: istri.

### Workspace

-   Personal: masing-masing pengguna memiliki ruang pribadi.
-   Family: ruang bersama yang dapat diakses kedua pengguna.
-   Business: ruang terpisah untuk masing-masing bisnis.

### Peran awal

-   `owner`: mengelola pengaturan dan anggota workspace.
-   `member`: menjalankan aktivitas sesuai izin.
-   `viewer`: hanya membaca data yang diizinkan (dapat diaktifkan
    kemudian).

Peran tidak boleh menjadi satu-satunya mekanisme keamanan. Semua query
harus memeriksa keanggotaan workspace dan izin atas resource.

## 6. Modul produk

### 6.1 Core Platform

-   Login/logout.
-   Profil pengguna.
-   Workspace dan keanggotaan.
-   Role dan permission.
-   Pengaturan lokal.
-   Audit log.
-   Notifikasi dasar.
-   File metadata dan lampiran.
-   Global navigation.

### 6.2 Finance

-   Akun kas, bank, dan e-wallet.
-   Kategori dan klasifikasi.
-   Pemasukan dan pengeluaran.
-   Transfer antar-akun.
-   Jurnal berpasangan (debit/kredit).
-   Anggaran.
-   Utang dan piutang.
-   Target tabungan.
-   Rekonsiliasi.
-   Laporan arus kas dan ringkasan.
-   Bukti transaksi dan riwayat koreksi.

### 6.3 Family & Planning

-   Agenda keluarga.
-   Tugas rumah.
-   Pengingat.
-   Kebutuhan belanja.
-   Aset keluarga.
-   Dokumen keluarga.

### 6.4 Business

-   Workspace per bisnis.
-   Pelanggan dan pemasok.
-   Layanan/produk.
-   Pesanan dan status pekerjaan.
-   Invoice dan pembayaran.
-   Inventaris dasar.
-   Biaya operasional.
-   Integrasi transaksi keuangan bisnis.

### 6.5 Projects & Knowledge

-   Proyek dan tugas.
-   Penanggung jawab.
-   Tenggat dan status.
-   Catatan, jurnal, referensi.
-   Dokumen dan lampiran.

### 6.6 AI & Integrations (masa depan)

-   Ringkasan laporan.
-   Ekstraksi data nota dengan verifikasi manusia.
-   Pencarian semantik.
-   Integrasi kalender dan WhatsApp.
-   Webhook dan API eksternal.

## 7. Kebutuhan fungsional tahap pertama

  ------------------------------------------------------------------------
  ID                      Kebutuhan                Prioritas
  ----------------------- ------------------------ -----------------------
  FR-001                  Pengguna dapat login dan Must
                          logout                   

  FR-002                  Pengguna dapat melihat   Must
                          workspace yang           
                          diikutinya               

  FR-003                  Setiap request           Must
                          memvalidasi keanggotaan  
                          workspace                

  FR-004                  Owner dapat              Must
                          mengundang/menambahkan   
                          anggota secara           
                          terkendali               

  FR-005                  Pengguna dapat berpindah Must
                          workspace                

  FR-006                  Pengguna dapat mengubah  Should
                          profil dan preferensi    
                          dasar                    

  FR-007                  Aktivitas sensitif       Must
                          tercatat dalam audit log 

  FR-008                  Dashboard menampilkan    Should
                          workspace aktif dan      
                          ringkasan                

  FR-009                  Sistem mendukung         Should
                          lampiran privat melalui  
                          metadata file            

  FR-010                  Admin dapat membuat      Must
                          backup dan menguji       
                          restore                  

  FR-011                  Sistem memiliki health   Must
                          check internal           

  FR-012                  Semua perubahan skema    Must
                          memakai migration        
  ------------------------------------------------------------------------

## 8. Kebutuhan nonfungsional

-   Mobile-first dan responsif.
-   Bahasa antarmuka Indonesia.
-   Mata uang IDR; nominal uang disimpan sebagai integer rupiah atau
    tipe `BIGINT`.
-   Zona waktu tampilan `Asia/Jakarta`; timestamp disimpan dalam UTC.
-   Semua endpoint privat memerlukan autentikasi dan otorisasi.
-   Query data harus dibatasi berdasarkan workspace.
-   Error tidak boleh membocorkan stack trace atau rahasia.
-   Backup harus dapat dipulihkan dan diuji.
-   Log tidak boleh menyimpan password, token, atau isi dokumen
    sensitif.
-   Performa diukur pada perangkat dan server target sebelum rilis.

## 9. Kriteria keberhasilan

Tahap pertama dinyatakan berhasil jika: 1. Dua pengguna dapat login
secara terpisah. 2. Pengguna hanya melihat workspace yang diikutinya. 3.
Pengguna tidak dapat membaca resource workspace lain dengan mengganti ID
pada URL/API. 4. Audit log merekam aksi penting dengan actor dan waktu.
5. Migration dapat dijalankan pada database kosong dan database
pengujian. 6. Backup database dapat dipulihkan ke environment uji. 7.
Aplikasi berjalan tanpa mengganggu layanan produksi Armbian yang sudah
ada.

## 10. Prinsip UX

-   Formulir singkat dan jelas.
-   Tombol aksi utama mudah dijangkau di ponsel.
-   Status simpan, gagal, dan loading terlihat.
-   Jangan mengandalkan warna saja untuk menyampaikan status.
-   Konfirmasi untuk aksi destruktif.
-   Tampilkan workspace aktif secara jelas.
-   Hindari dashboard penuh grafik sebelum data nyata tersedia.
