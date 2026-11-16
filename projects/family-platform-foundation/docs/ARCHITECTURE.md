# Architecture Specification

**Versi:** 1.0\
**Gaya:** Modular Monolith dengan batas domain yang eksplisit

## 1. Keputusan arsitektur

Aplikasi dimulai sebagai satu deployment web untuk menekan kompleksitas
operasional pada server Armbian. Kode tetap dipisah menjadi modul
domain. Backend dapat dipisahkan menjadi service tersendiri jika beban,
tim, atau kebutuhan integrasi membenarkannya.

### Stack baseline

-   Next.js (App Router) + TypeScript.
-   PostgreSQL.
-   Prisma ORM dan migration.
-   REST API `/api/v1`.
-   Zod untuk validasi boundary.
-   Vitest untuk unit/integration test.
-   Playwright untuk end-to-end.
-   Docker Compose opsional untuk deployment terisolasi.
-   Nginx/reverse proxy yang sudah ada hanya disentuh melalui perubahan
    terencana.

Versi dependency harus dipatok di lockfile. Gunakan versi stabil yang
kompatibel saat implementasi; jangan menggunakan tag `latest` pada
produksi.

## 2. Diagram logis

``` text
Browser (mobile/desktop)
        |
        v
Next.js UI + Server/API boundary
        |
        +-- Core: auth, workspace, permission, audit
        +-- Finance module
        +-- Family module
        +-- Business module
        +-- Planning/Projects module
        +-- Documents/Assets module
        |
        v
Application services + domain rules
        |
        v
Repositories / Prisma
        |
        v
PostgreSQL

File upload -> private file storage
Scheduled work -> cron/background worker (ditambahkan saat perlu)
```

## 3. Aturan batas modul

-   Modul memiliki folder domain, application, infrastructure, dan
    presentation.
-   Modul lain tidak boleh mengakses Prisma model internal secara
    langsung.
-   Interaksi lintas modul melalui application service atau event
    internal.
-   Hindari circular dependency.
-   Core tidak boleh bergantung pada modul bisnis tertentu.
-   Finance tidak boleh mengimpor logika DEKEKU atau ARTO PRINTING.
-   Business dapat meminta Finance membuat transaksi melalui kontrak
    aplikasi yang tervalidasi.

## 4. Multi-workspace dan kepemilikan

Semua data operasional memiliki `workspace_id` atau hubungan kepemilikan
yang eksplisit. Workspace mempunyai `type`: `personal`, `family`, atau
`business`.

Business workspace dapat memiliki `business_profile` dan
`legal/operational entity` sendiri. Jangan menganggap setiap workspace
selalu satu entitas keuangan.

Pengguna awal hanya dua, tetapi tabel membership harus mendukung anggota
tambahan tanpa migrasi desain besar.

## 5. API

-   Prefix: `/api/v1`.
-   JSON request/response.
-   Validasi input di server.
-   Pagination untuk daftar.
-   Filter workspace harus berasal dari konteks autentikasi/otorisasi,
    bukan dipercaya hanya dari input klien.
-   Error memakai format konsisten: `code`, `message`, `requestId`.
-   Endpoint mutasi sensitif mendukung idempotency key bila relevan.
-   Dokumentasikan API dengan OpenAPI setelah endpoint inti stabil.

## 6. Database dan transaksi

-   PostgreSQL sebagai source of truth.
-   Semua operasi multi-tabel yang harus konsisten memakai transaksi
    database.
-   Gunakan foreign key, unique constraint, check constraint, dan index.
-   Simpan waktu sebagai `timestamptz` UTC.
-   Simpan nilai uang IDR sebagai integer rupiah (`BIGINT` bila perlu
    rentang besar), bukan floating point.
-   Jangan menyimpan saldo turunan sebagai satu-satunya sumber
    kebenaran.
-   Saldo dihitung dari saldo awal dan ledger yang sudah diposting;
    cache saldo boleh ditambahkan kemudian dengan mekanisme
    rekonsiliasi.

## 7. Keuangan

Gunakan model jurnal berpasangan: - `journal_entries`: header
transaksi. - `journal_lines`: baris debit/kredit. - Total debit harus
sama dengan total kredit sebelum posting. - Akun kas/bank/e-wallet
adalah akun ledger. - Transfer antar rekening adalah perpindahan antar
akun, bukan income atau expense. - Transaksi yang sudah posted tidak
diedit/hapus secara langsung; koreksi memakai reversal atau
adjustment. - Setiap posting menyimpan actor dan timestamp.

Untuk laporan sederhana, kategori dapat menjadi atribut transaksi atau
dipetakan ke akun ledger. Hindari membuat dua sumber kebenaran yang
bertentangan.

## 8. File storage

-   File bersifat privat secara default.
-   Database menyimpan metadata, bukan binary file.
-   Simpan object key, nama asli, MIME type, ukuran, checksum, uploader,
    workspace, dan waktu.
-   Validasi ukuran dan MIME di server.
-   Jangan gunakan nama file pengguna sebagai path filesystem.
-   Unduhan harus melewati pemeriksaan izin atau signed URL berumur
    pendek.
-   Backup file diuji terpisah dari backup database.

## 9. Deployment Armbian

-   Development dan test dilakukan lokal atau di environment terpisah.
-   Jangan memasang service baru langsung ke production sebelum resource
    audit.
-   Gunakan direktori deployment khusus, terpisah dari `/www` milik
    aaPanel.
-   Jangan mengubah konfigurasi Nginx/Cloudflare Tunnel yang sedang
    digunakan tanpa backup dan rollback.
-   Bind PostgreSQL ke jaringan privat/container, bukan port publik.
-   Gunakan port aplikasi yang telah diverifikasi kosong.
-   Batasi CPU/memory jika menggunakan container.
-   Sediakan health check, log rotation, backup, dan prosedur rollback.
-   Uji beban dan konsumsi RAM saat semua service yang ada berjalan.

### Catatan kapasitas

Server HG680P yang digunakan memiliki RAM sekitar 1.8 GiB menurut
pemeriksaan sebelumnya dan menjalankan layanan lain. Karena itu, jangan
mengasumsikan Next.js + PostgreSQL + layanan tambahan aman berjalan
bersamaan. Lakukan pengukuran idle/peak terlebih dahulu. Jika resource
tidak mencukupi, pertimbangkan database di host terpisah atau hosting
database eksternal yang aman, tanpa mengubah model aplikasi.

## 10. Observability

Minimal: - Log terstruktur. - Request ID. - Health endpoint. - Error log
tanpa secret. - Status backup. - Disk space dan memory monitoring. -
Audit log aplikasi terpisah dari log teknis.

## 11. Keputusan yang ditunda

-   Redis dan job queue.
-   Microservices.
-   Native mobile app.
-   Offline-first sync.
-   Multi-tenant publik.
-   AI agent yang dapat melakukan mutasi.
-   Integrasi bank/payment gateway.
