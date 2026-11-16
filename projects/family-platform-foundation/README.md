# Family Platform --- Product Foundation

**Dokumen:** Product Foundation Specification (PFS)\
**Versi:** 1.0\
**Status:** Baseline untuk implementasi\
**Codename:** `family-platform`\
**Nama produk final:** Belum ditentukan

## Tujuan

Membangun satu platform web untuk mengelola kebutuhan personal,
keluarga, dan bisnis dalam satu ekosistem dengan pemisahan data dan hak
akses yang tegas.

## Keputusan utama

-   Pengguna awal: dua orang (suami dan istri).
-   Ruang kerja: Personal, Family, dan Business.
-   Bisnis awal: DEKEKU dan ARTO PRINTING sebagai workspace terpisah.
-   Platform: web responsif, mobile-first.
-   Bahasa dan format: Indonesia, IDR, `Asia/Jakarta`.
-   Arsitektur: modular monolith.
-   Stack awal: Next.js, TypeScript, PostgreSQL, Prisma.
-   Hosting: server Armbian; deployment produksi hanya setelah uji
    kapasitas dan prosedur rollback.

## Dokumen acuan

  Dokumen                       Isi
  ----------------------------- -------------------------------------------
  `docs/PRD.md`                 Kebutuhan produk dan ruang lingkup
  `docs/ARCHITECTURE.md`        Arsitektur aplikasi dan keputusan teknis
  `docs/DATABASE.md`            Model data dan aturan integritas
  `docs/SECURITY.md`            Keamanan dan privasi
  `docs/PHASE-1.md`             Rencana implementasi tahap pertama
  `docs/REPOSITORY.md`          Struktur repository dan aturan kontribusi
  `database/schema-notes.sql`   Catatan konseptual skema awal

## Prinsip yang tidak boleh dilanggar

1.  Data selalu dimiliki oleh workspace yang jelas.
2.  Akses ditolak secara default; izin diberikan secara eksplisit.
3.  Modul tidak mengakses tabel internal modul lain secara langsung.
4.  Aktivitas sensitif tercatat dalam audit log.
5.  Transaksi keuangan yang sudah diposting tidak dihapus atau ditimpa
    diam-diam.
6.  Tidak ada deployment atau migrasi produksi tanpa backup dan rencana
    rollback.
7.  Jangan mengubah konfigurasi aaPanel, Nginx, Cloudflare Tunnel, atau
    service produksi yang sudah ada tanpa rencana dan persetujuan
    eksplisit.

## Status dokumen

Dokumen ini adalah baseline awal. Perubahan keputusan arsitektur harus
dicatat dalam `docs/DECISIONS.md` (buat file tersebut saat repository
diinisialisasi) sebagai Architecture Decision Record (ADR).
