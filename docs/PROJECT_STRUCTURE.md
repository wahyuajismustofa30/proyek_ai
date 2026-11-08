# Aturan Direktori dan Struktur Proyek

Dokumen ini adalah aturan kanonis untuk isi `projects/`. Tujuannya menjaga batas
antarproyek, membuat discovery CI deterministik, dan mencegah proyek tersembunyi dari
pemeriksaan otomatis.

## 1. Batas direktori proyek

- Hanya direktori satu tingkat langsung di bawah `projects/` yang dianggap proyek.
- Nama direktori harus berupa slug ASCII huruf kecil dan angka, dengan segmen dipisahkan
  satu tanda hubung: `[a-z0-9]+(?:-[a-z0-9]+)*`.
- Contoh valid: `web-app`, `api-v2`, `dekeku-landing-page`.
- Contoh tidak valid: `.draft`, `MyApp`, `my_app`, `my app`, `project.backup`.
- Nama harus unik karena satu direktori adalah satu batas proyek.
- Symlink apa pun yang berada langsung di dalam `projects/` ditolak. Gunakan file
  dan direktori nyata di dalam batas proyek.

File biasa di root `projects/` (misalnya `.gitkeep` atau catatan) bukan proyek dan
diabaikan oleh discovery. Direktori tersembunyi tepat di bawah `projects/` ditolak
dengan error, bukan diabaikan. Jangan gunakan nama seperti `.draft/`, `.archive/`,
`.internal/`, atau `.cache/` untuk menyimpan proyek atau pekerjaan sementara.
Simpan arsip di `archives/` dan fixture pengujian di direktori sementara test.

## 2. Direktori tersembunyi di dalam proyek

Direktori dan file tersembunyi diperbolehkan di dalam folder proyek karena sering
dibutuhkan oleh tool dan konfigurasi, misalnya:

- `.github/ISSUE_TEMPLATE/` untuk template issue;
- `.config/` untuk konfigurasi tool;
- `.well-known/` untuk kebutuhan aplikasi web;
- `.gitignore`, `.editorconfig`, dan file dot-config lainnya.

Direktori tersembunyi tersebut adalah bagian dari proyek induk, bukan proyek terpisah.
Discovery CI tidak menelusuri subdirektori untuk menemukan proyek tambahan. Workflow
di `projects/<slug>/.github/workflows/` juga tidak menjadi workflow CI aktif monorepo;
orkestrasi tetap berada di `.github/workflows/` root repository.

## 3. Struktur scaffold standar

Buat proyek dengan `python scripts/bootstrap_project.py --name "Nama Proyek"`.
Jangan menyalin struktur secara manual. Template standar menyediakan:

```text
projects/
└── <slug>/
    ├── README.md
    ├── AGENTS.md
    ├── .project-meta.json
    ├── .gitignore
    ├── .env.example
    ├── SECURITY.md
    ├── .github/
    │   └── ISSUE_TEMPLATE/
    ├── assets/
    ├── docs/
    │   ├── ARCHITECTURE.md
    │   ├── CHANGELOG.md
    │   ├── DECISIONS.md
    │   ├── PROJECT_BRIEF.md
    │   ├── TASKS.md
    │   └── TESTING.md
    ├── src/
    └── tests/
```

Peran direktori:

| Lokasi | Aturan |
|---|---|
| `README.md` | Ringkasan, teknologi, cara menjalankan, dan status proyek |
| `AGENTS.md` | Instruksi AI/kontributor khusus proyek |
| `.project-meta.json` | Metadata scaffold dan orkestrasi CI root; pertahankan format valid |
| `docs/` | Brief, arsitektur, keputusan, task, changelog, dan strategi test |
| `src/` | Source code aplikasi; jangan mencampur source proyek lain |
| `tests/` | Unit, integrasi, dan end-to-end test proyek |
| `assets/` | Aset proyek yang memang menjadi bagian source |
| `.github/` | Template issue dan konfigurasi kontribusi; bukan tempat workflow CI aktif |
| `.env.example` | Nama variabel dan contoh non-rahasia saja; jangan isi credential nyata |

Folder tambahan boleh ditambahkan sesuai kebutuhan stack, misalnya `public/`,
`config/`, `migrations/`, atau `scripts/`. Jangan menambahkan folder hanya sebagai
placeholder. Folder `node_modules/`, `.venv/`, `vendor/`, cache, hasil build, dan
secret lokal tidak boleh di-commit kecuali ada alasan teknis yang terdokumentasi.

## 4. Manifest dan stack

Letakkan manifest stack pada root proyek agar adapter discovery dapat menemukannya:

| Stack | Manifest yang dikenali | Lockfile/kontrak CI |
|---|---|---|
| Node.js | `package.json` | `package-lock.json` dan script `test` |
| Python | `pyproject.toml` atau `requirements.txt` | dependency test sesuai kontrak CI; test ditemukan pytest |
| PHP | `composer.json` | `composer.lock` dan script Composer `test` |

Satu proyek dapat memiliki lebih dari satu manifest dan akan menghasilkan satu entri
matrix untuk setiap stack yang terdeteksi. Manifest di subfolder tidak otomatis
membuat stack baru. Stack yang belum memiliki adapter CI tidak boleh dianggap telah
teruji otomatis.

## 5. Aturan perubahan

1. Gunakan bootstrap resmi untuk membuat folder baru.
2. Jangan membuat proyek di subfolder proyek lain atau di direktori tersembunyi.
3. Jangan menaruh arsip, backup, fixture, dependency terpasang, cache, atau output build
   di root `projects/`.
4. Jangan membuat workflow CI atau Dependabot lokal untuk proyek monorepo.
5. Lengkapi README dan brief; tambahkan manifest serta lockfile yang sesuai.
6. Tambahkan proyek yang diterima ke `docs/PROJECT_INDEX.md`.
7. Jalankan discovery dan seluruh test repository sebelum membuka PR.

Perilaku ini ditegakkan oleh `scripts/discover_projects.py` dan test
`scripts/tests/test_discover_projects.py`. Dokumentasi CI terkait berada di
`docs/MONOREPO_CI.md`.
