# Aturan Direktori dan Struktur Proyek

Dokumen ini adalah aturan kanonis untuk isi `projects/`. Tujuannya menjaga batas
antarproyek, membuat discovery CI deterministik, dan mencegah proyek tersembunyi dari
pemeriksaan otomatis.

## 1. Batas direktori proyek

- Hanya direktori satu tingkat langsung di bawah `projects/` yang dianggap proyek.
- Nama direktori harus berupa slug ASCII huruf kecil dan angka, dengan segmen dipisahkan
  satu tanda hubung: `[a-z0-9]+(?:-[a-z0-9]+)*`.
- Contoh valid: `web-app`, `api-v2`, `landing-page`.
- Contoh tidak valid: `.draft`, `MyApp`, `my_app`, `my app`, `project.backup`.
- Nama harus unik karena satu direktori adalah satu batas proyek.
- Symlink apa pun yang berada langsung di dalam `projects/` ditolak. Gunakan file
  dan direktori nyata di dalam batas proyek.

Hanya `projects/README.md` yang boleh menjadi file langsung di root `projects/`;
file root lain ditolak oleh discovery agar fixture, catatan sementara, dan artefak
tidak bercampur dengan proyek. Direktori tersembunyi tepat di bawah `projects/`
ditolak dengan error, bukan diabaikan. Jangan gunakan nama seperti `.draft/`,
`.archive/`, `.internal/`, atau `.cache/` untuk menyimpan proyek atau pekerjaan sementara.
`archives/` saat ini hanya berisi README penjelas. Jangan menaruh fixture atau pekerjaan sementara di sana; gunakan direktori sementara test. Penambahan arsip historis memerlukan keputusan dan dokumentasi pemilik repository.

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

Template issue root repository menggunakan YAML GitHub Issue Forms agar pelaporan
masalah tooling dan CI memiliki field terstruktur serta validasi wajib. Template
proyek menggunakan Markdown karena scaffold bersifat generik dan tiap pemilik
proyek dapat mengubah pertanyaan sesuai domain tanpa mempertahankan skema form
terpusat repository induk.

Folder tambahan boleh ditambahkan sesuai kebutuhan stack, misalnya `public/`,
`config/`, `migrations/`, atau `scripts/`. Jangan menambahkan folder hanya sebagai
placeholder. Dependency terpasang (`node_modules/`, `vendor/`, `.venv/`, `venv/`),
cache (`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`), log,
file sementara, hasil build (`dist/`, `build/`), coverage, dan artefak tidak boleh
disimpan di repository. Simpan output yang dapat dibuat ulang di direktori sementara
sistem/CI. Discovery CI menolak pola artefak umum tersebut agar pelanggaran terdeteksi.

## 4. Manifest dan stack

Letakkan manifest stack pada root proyek agar adapter discovery dapat menemukannya:

| Stack | Manifest yang dikenali | Lockfile/kontrak CI |
|---|---|---|
| Node.js | `package.json` | `package-lock.json` dan script `test` |
| Python | `pyproject.toml` atau `requirements.txt` | dependency test sesuai kontrak CI; test ditemukan pytest |
| PHP | `composer.json` | `composer.lock` dan script Composer `test` |
| Static website | `index.html` tepat di root proyek | HTTP smoke test; HTML, CSS, dan aset lokal diperiksa oleh job web-validation |

Satu proyek dapat memiliki lebih dari satu manifest dan akan menghasilkan satu entri
matrix untuk setiap stack yang terdeteksi. Static website dideteksi dari keberadaan
`index.html` di root proyek; halaman HTML yang hanya berada di subfolder tidak cukup.
Satu proyek dapat menghasilkan job static dan job aplikasi sekaligus. Manifest di subfolder tidak otomatis
membuat stack baru. Stack yang belum memiliki adapter CI tidak boleh dianggap telah
teruji otomatis.

## 5. Aturan perubahan

1. Gunakan bootstrap resmi untuk membuat folder baru.
2. Selain `projects/README.md`, jangan menyimpan file langsung di root `projects/`.
3. Jangan membuat proyek di subfolder proyek lain atau di direktori tersembunyi.
4. Jangan menaruh arsip, backup, fixture, dependency terpasang, cache, log, file sementara,
   coverage, atau output build di mana pun di dalam proyek.
5. Jangan membuat workflow CI atau Dependabot lokal untuk proyek monorepo.
6. Lengkapi README dan brief; tambahkan manifest serta lockfile yang sesuai.
7. Tambahkan proyek yang diterima ke `docs/PROJECT_INDEX.md`.
8. Jalankan discovery dan seluruh test repository sebelum membuka PR.

Perilaku ini ditegakkan oleh `scripts/discover_projects.py` dan test
`scripts/tests/test_discover_projects.py`. Dokumentasi CI terkait berada di
`docs/MONOREPO_CI.md`.
