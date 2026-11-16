# Master Database Specification

**Versi:** 1.0\
**Database:** PostgreSQL\
**ORM:** Prisma

Dokumen ini mendefinisikan domain dan kontrak data. Skema Prisma final
dibuat setelah review sebelum migration produksi.

## 1. Konvensi umum

-   Primary key: UUID.
-   Nama tabel/kolom: `snake_case`.
-   Timestamp: `created_at`, `updated_at` dalam `timestamptz`.
-   Soft delete hanya untuk data yang memang boleh diarsipkan; jangan
    menerapkan soft delete pada ledger posted sebagai pengganti
    reversal.
-   Data workspace selalu memiliki `workspace_id` atau relasi ownership
    yang jelas.
-   Foreign key wajib untuk relasi internal.
-   Unique constraint digunakan untuk mencegah duplikasi.
-   Uang IDR: integer rupiah (`BIGINT`), tidak memakai float.
-   Nominal dan tanggal tidak boleh hanya divalidasi di frontend.

## 2. Core domain

### `users`

-   `id` UUID PK
-   `email` unique, normalized
-   `display_name`
-   `password_hash`
-   `status` (`active`, `disabled`, `pending`)
-   `last_login_at`
-   `created_at`, `updated_at`

### `workspaces`

-   `id` UUID PK
-   `name`
-   `slug`
-   `type` (`personal`, `family`, `business`)
-   `status`
-   `timezone` default `Asia/Jakarta`
-   `default_currency` default `IDR`
-   `created_by`
-   timestamps

Unique: `(slug)` pada ruang lingkup yang dipilih; untuk multi-organisasi
nanti dapat menjadi `(owner_scope, slug)`.

### `workspace_members`

-   `id` UUID PK
-   `workspace_id` FK
-   `user_id` FK
-   `role_id` FK
-   `status`
-   `joined_at`
-   timestamps

Unique: `(workspace_id, user_id)`.

### `roles`, `permissions`, `role_permissions`

Role dan permission dipisahkan. Jangan mengandalkan nama role di
frontend sebagai kontrol keamanan.

### `user_preferences`

-   `user_id` FK unique
-   `locale`
-   `timezone`
-   `theme`
-   preferensi notifikasi

## 3. Core operational tables

### `audit_logs`

-   `id` UUID PK
-   `workspace_id` nullable hanya untuk aksi sistem global yang sah
-   `actor_user_id` nullable untuk system actor
-   `action`
-   `resource_type`
-   `resource_id`
-   `before_data` JSONB nullable
-   `after_data` JSONB nullable
-   `reason` nullable
-   `request_id`
-   `created_at`

Audit log bersifat append-only bagi aplikasi. Batasi data sensitif di
snapshot; jangan merekam password, token, atau isi file.

### `attachments`

-   `id` UUID PK
-   `workspace_id` FK
-   `uploaded_by` FK
-   `storage_key`
-   `original_filename`
-   `mime_type`
-   `size_bytes`
-   `checksum`
-   `created_at`

### `notifications`

-   `id` UUID PK
-   `user_id` FK
-   `workspace_id` nullable
-   `type`
-   `title`
-   `body`
-   `read_at`
-   `created_at`

## 4. Finance domain

### `financial_entities`

Mewakili pemilik/pembukuan: pribadi suami, pribadi istri, keluarga,
DEKEKU, ARTO PRINTING. - `id` UUID PK - `workspace_id` FK - `name` -
`entity_type` - `currency` - `status`

### `accounts`

-   `id` UUID PK
-   `financial_entity_id` FK
-   `name`
-   `account_type` (`cash`, `bank`, `ewallet`, `receivable`, `payable`,
    `income`, `expense`, `equity`, `other`)
-   `opening_balance` BIGINT
-   `is_active`
-   timestamps

### `categories`

-   `id` UUID PK
-   `workspace_id` FK
-   `name`
-   `kind` (`income`, `expense`, `transfer`, `other`)
-   `parent_id` nullable FK
-   `is_active`

### `journal_entries`

-   `id` UUID PK
-   `workspace_id` FK
-   `financial_entity_id` FK
-   `entry_number`
-   `entry_date`
-   `description`
-   `status` (`draft`, `posted`, `reversed`)
-   `created_by`
-   `posted_by` nullable
-   `posted_at` nullable
-   `reversal_of_id` nullable FK
-   timestamps

Unique: `(financial_entity_id, entry_number)`.

### `journal_lines`

-   `id` UUID PK
-   `journal_entry_id` FK
-   `account_id` FK
-   `debit_amount` BIGINT default 0
-   `credit_amount` BIGINT default 0
-   `category_id` nullable FK
-   `memo` nullable

Constraint: tepat satu sisi debit/kredit bernilai positif pada setiap
baris; jumlah debit = jumlah kredit pada saat posting. Validasi
keseimbangan dilakukan dalam satu transaksi database di server.

### `budgets`

-   `id` UUID PK
-   `workspace_id` FK
-   `financial_entity_id` FK
-   `category_id` FK
-   `period_start`
-   `period_end`
-   `limit_amount` BIGINT
-   timestamps

### `reconciliations`

-   `id` UUID PK
-   `account_id` FK
-   `statement_date`
-   `statement_balance` BIGINT
-   `calculated_balance` BIGINT
-   `status`
-   `reconciled_by`
-   `reconciled_at`

### `debts`

-   `id` UUID PK
-   `workspace_id` FK
-   `financial_entity_id` FK
-   `direction` (`owed`, `receivable`)
-   `counterparty`
-   `principal_amount` BIGINT
-   `outstanding_amount` BIGINT
-   `due_date`
-   `status`

### `savings_goals`

-   `id` UUID PK
-   `workspace_id` FK
-   `financial_entity_id` FK
-   `name`
-   `target_amount` BIGINT
-   `target_date`
-   `status`

## 5. Business domain

-   `business_profiles`: profil DEKEKU/ARTO PRINTING.
-   `customers`: pelanggan per workspace bisnis.
-   `suppliers`: pemasok per workspace bisnis.
-   `products_services`: produk atau layanan.
-   `orders`: pesanan dan status.
-   `order_items`: rincian pesanan.
-   `invoices`: tagihan.
-   `invoice_items`: rincian tagihan.
-   `payments`: penerimaan pembayaran.
-   `inventory_items`: barang/bahan.
-   `stock_movements`: pergerakan stok.

Semua tabel bisnis harus dibatasi oleh workspace. Data pelanggan
antar-bisnis tidak otomatis dibagikan.

## 6. Planning, projects, assets, documents

-   `projects`: workspace, nama, status, tanggal.
-   `tasks`: proyek opsional, assignee, status, priority, due date.
-   `events`: kalender, waktu mulai/selesai, visibility.
-   `reminders`: target resource, waktu pengingat, status.
-   `assets`: workspace, kategori, nama, nilai, kondisi.
-   `asset_maintenance`: aset, aktivitas, tanggal, biaya.
-   `documents`: workspace, folder, metadata, classification, version.
-   `document_versions`: attachment, version number, uploader.
-   `notes`: workspace, author, visibility, content.
-   `journal_entries_personal`: jika jurnal naratif dibutuhkan, gunakan
    nama tabel berbeda dari finance journal.

## 7. Relasi dan batas akses

-   User dapat menjadi anggota beberapa workspace.
-   Workspace memiliki banyak anggota dan banyak resource.
-   Setiap request memeriksa workspace membership.
-   Query harus memfilter `workspace_id` di server.
-   UUID bukan mekanisme otorisasi.
-   Personal workspace default hanya dapat diakses pemiliknya.
-   Family workspace dibagikan kepada dua pengguna sesuai membership.
-   Business workspace tetap terpisah dari Family workspace.

## 8. Indeks minimum

-   `workspace_members(user_id, workspace_id)`
-   `audit_logs(workspace_id, created_at)`
-   `journal_entries(workspace_id, entry_date)`
-   `journal_lines(journal_entry_id)`
-   `accounts(financial_entity_id)`
-   `tasks(workspace_id, status, due_date)`
-   `documents(workspace_id, created_at)`
-   `notifications(user_id, read_at)`

Indeks final harus mengikuti query yang benar-benar digunakan dan
diperiksa dengan `EXPLAIN ANALYZE`.

## 9. Konsistensi dan migrasi

-   Semua perubahan skema melalui migration.
-   Migration diuji pada database kosong dan salinan data uji.
-   Backup sebelum migration produksi.
-   Perubahan destruktif memerlukan migration bertahap.
-   Seed hanya untuk data referensi dan akun development; jangan menanam
    password produksi.
-   Jangan mengubah histori ledger posted melalui migration data tanpa
    prosedur audit.
