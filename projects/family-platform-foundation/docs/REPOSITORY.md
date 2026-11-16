# Repository Structure & Engineering Rules

## 1. Struktur yang disarankan

``` text
family-platform/
├── apps/
│   └── web/
│       ├── src/
│       │   ├── app/
│       │   │   ├── (auth)/
│       │   │   ├── (app)/
│       │   │   └── api/
│       │   │       └── v1/
│       │   ├── modules/
│       │   │   ├── auth/
│       │   │   ├── workspaces/
│       │   │   ├── audit/
│       │   │   ├── finance/
│       │   │   ├── family/
│       │   │   └── business/
│       │   ├── shared/
│       │   │   ├── components/
│       │   │   ├── lib/
│       │   │   ├── validation/
│       │   │   └── types/
│       │   └── server/
│       │       ├── auth/
│       │       ├── db/
│       │       └── security/
│       ├── prisma/
│       │   ├── schema.prisma
│       │   ├── migrations/
│       │   └── seed.ts
│       ├── public/
│       ├── tests/
│       ├── package.json
│       └── next.config.ts
├── docs/
├── database/
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   └── backup/
├── scripts/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── package.json
├── pnpm-lock.yaml
└── README.md
```

Struktur ini adalah target awal; jangan membuat semua folder kosong
sekaligus. Tambahkan ketika modul mulai dikerjakan.

## 2. Aturan kode

-   TypeScript strict mode.
-   Hindari `any`; jelaskan setiap pengecualian.
-   Validasi semua input di server.
-   Business rule berada di service/domain, bukan komponen UI.
-   Komponen UI tidak boleh menjalankan query database langsung.
-   Semua query privat melalui authorization boundary.
-   Hindari circular imports.
-   Gunakan naming konsisten.
-   Semua fitur baru disertai test.
-   Tidak menyimpan file upload di Git.

## 3. Git workflow

-   `main`: selalu stabil dan siap rilis.
-   Feature branch: `feat/<module>-<short-name>`.
-   Bugfix branch: `fix/<short-name>`.
-   Perubahan database dan API harus direview.
-   Commit kecil dengan pesan jelas.
-   Pull request harus menyertakan ringkasan, test, screenshot bila UI,
    dan dampak migration.

## 4. Conventional commit

-   `feat: add workspace switcher`
-   `fix: enforce workspace membership`
-   `docs: update database specification`
-   `test: add authorization coverage`
-   `refactor: isolate finance domain`

## 5. Wajib masuk Git

-   Source code.
-   Migration.
-   Dokumentasi.
-   Test.
-   `.env.example` tanpa secret.
-   Script deployment yang aman.

## 6. Dilarang masuk Git

-   `.env` produksi.
-   Password, token, private key.
-   Database dump berisi data pribadi.
-   Bukti transaksi dan dokumen keluarga.
-   Backup.
-   `node_modules`, build output, log.

## 7. Definition of Done

Sebuah fitur selesai jika: 1. Kebutuhan dan acceptance criteria
terpenuhi. 2. Validasi server tersedia. 3. Authorization diuji. 4.
Error/loading/empty states tersedia. 5. Test lulus. 6. Dokumentasi
diperbarui. 7. Audit log ditambahkan bila aksi sensitif. 8. Tidak ada
secret atau data pribadi di commit.
