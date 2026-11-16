# Phase 1 Implementation Plan --- Core Foundation

**Tujuan:** menghasilkan fondasi aplikasi yang aman, dapat diuji, dan
siap menerima modul Finance.

## 1. Scope

### Termasuk

-   Inisialisasi repository.
-   Aplikasi Next.js + TypeScript.
-   PostgreSQL dan Prisma.
-   Authentication dua akun.
-   Workspace dan membership.
-   Workspace switcher.
-   Authorization server-side.
-   Audit log dasar.
-   Dashboard shell.
-   Health check.
-   Backup/restore runbook.
-   Test dan dokumentasi.

### Tidak termasuk

-   Ledger dan pencatatan keuangan lengkap.
-   Business orders/invoices.
-   AI.
-   WhatsApp.
-   Integrasi bank.
-   Aplikasi native.
-   Deployment produksi sebelum resource audit.

## 2. Urutan pekerjaan

### Milestone 1 --- Repository & local development

-   Buat repository privat.
-   Inisialisasi package manager dan lockfile.
-   Aktifkan TypeScript strict.
-   Tambahkan lint, format, test.
-   Buat `.env.example`.
-   Buat README dan docs.
-   Pastikan secret tidak pernah masuk Git.

Acceptance: - Fresh clone dapat di-setup mengikuti README. - Lint dan
test command berjalan. - Build berhasil.

### Milestone 2 --- Database foundation

-   Buat PostgreSQL development database.
-   Definisikan Prisma schema untuk users, workspaces, memberships,
    roles, permissions, audit logs.
-   Buat migration awal.
-   Buat seed development yang aman.
-   Tambahkan index dan unique constraints.

Acceptance: - Migration berjalan dari database kosong. - Duplicate
membership ditolak. - Foreign key bekerja. - Tidak ada data produksi di
seed.

### Milestone 3 --- Authentication

-   Login/logout.
-   Password hash Argon2id.
-   Session aman.
-   Rate limiting.
-   Proteksi route.
-   Error generik untuk kredensial salah.

Acceptance: - Dua akun dapat login secara independen. - Session invalid
setelah logout. - Password tidak pernah disimpan plaintext. - Route
privat menolak anonymous request.

### Milestone 4 --- Workspace & authorization

-   Buat Personal workspace masing-masing.
-   Buat Family workspace.
-   Siapkan Business workspace DEKEKU dan ARTO PRINTING.
-   Membership dan role.
-   Workspace switcher.
-   Server-side workspace context.

Acceptance: - Setiap pengguna melihat hanya workspace yang diikutinya. -
Mengganti UUID tidak memberi akses. - Data personal tidak bocor ke
anggota lain. - Kedua pengguna dapat mengakses Family workspace sesuai
izin.

### Milestone 5 --- Audit & dashboard shell

-   Audit event untuk login penting, perubahan membership, perubahan
    role, dan perubahan pengaturan.
-   Dashboard minimal.
-   Navigation berdasarkan workspace dan permission.
-   Empty state dan error state.

Acceptance: - Audit log menyimpan actor, action, resource, waktu,
request ID. - Pengguna tidak dapat mengubah audit log melalui API
umum. - Dashboard tidak menampilkan data workspace lain.

### Milestone 6 --- Backup, restore & staging

-   Backup database.
-   Backup file metadata/storage.
-   Simpan backup di lokasi terpisah.
-   Uji restore ke database staging.
-   Jalankan aplikasi di port staging.
-   Ukur resource pada Armbian.

Acceptance: - Restore berhasil. - Tidak ada perubahan pada aaPanel atau
layanan produksi. - Port dan konfigurasi reverse proxy tidak
berbenturan. - RAM, CPU, disk, dan suhu dipantau selama uji.

## 3. Urutan workspace awal

1.  Personal Suami.
2.  Personal Istri.
3.  Family.
4.  DEKEKU.
5.  ARTO PRINTING.

Workspace bisnis dapat dibuat sejak fondasi, tetapi modul bisnis belum
perlu aktif.

## 4. Resource gate sebelum production

Sebelum deployment: - Catat baseline RAM/CPU/disk ketika layanan yang
ada berjalan. - Jalankan aplikasi dan database pada staging. - Uji
login, navigasi, dan query. - Amati memory peak dan restart. - Pastikan
disk memiliki ruang untuk database dan backup. - Jangan lanjut jika
service produksi mengalami degradasi. - Tentukan apakah database perlu
dipindahkan ke host lain.

## 5. Release gate

Phase 1 tidak boleh dinyatakan selesai sebelum: - Test authorization
lintas-workspace lulus. - Migration teruji. - Backup restore teruji. -
Tidak ada secret di repository. - Aplikasi dapat rollback. - Dokumentasi
deployment tersedia.

## 6. Deliverables

-   Repository GitHub privat.
-   Aplikasi web dasar.
-   Database migration awal.
-   Dua akun pengguna.
-   Lima workspace awal.
-   Workspace access control.
-   Audit log dasar.
-   Dashboard shell.
-   Test suite awal.
-   Runbook backup/restore dan deployment.
