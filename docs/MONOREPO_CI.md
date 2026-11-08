# CI terpusat untuk monorepo

## Keputusan arsitektur

Repository menggunakan satu workflow aktif di root untuk menguji semua proyek di
`projects/<slug>/`. Workflow yang disalin ke subfolder proyek tidak otomatis dijalankan
oleh GitHub Actions. Karena itu, proyek di monorepo tidak boleh mengandalkan workflow
di `projects/<slug>/.github/workflows/` sebagai CI aktif.

Workflow utama:

- `.github/workflows/validate.yml`: validasi repository, dokumentasi, JSON, YAML dan schema
  Dependabot, Python, aset arsip, tautan internal, secret, dan whitespace.
- `.github/workflows/project-matrix.yml`: menemukan proyek, menjalankan test aplikasi
  per stack, serta memvalidasi HTML, CSS, dan referensi aset lokal setiap proyek.
- `.github/workflows/dependency-security.yml`: pemindaian OSV-Scanner rekursif
  untuk manifest dan lockfile di seluruh repository.

Semua workflow berjalan pada pull request ke `main` dan push ke `main`; project CI
juga memiliki jadwal mingguan dan pemicu manual.

## Cara discovery bekerja

Script `scripts/discover_projects.py` hanya memeriksa satu tingkat folder langsung
di bawah `projects/`. Aturan nama, direktori tersembunyi, symlink, dan struktur scaffold
dijelaskan lengkap di `docs/PROJECT_STRUCTURE.md`. File biasa di root `projects/`
diabaikan; direktori tersembunyi di tingkat root ditolak secara eksplisit agar tidak
dapat menyembunyikan proyek dari CI. Direktori tersembunyi di dalam folder proyek
diperbolehkan dan tidak dianggap sebagai proyek terpisah. Setiap folder proyek dipetakan
menjadi satu atau lebih job:

| Manifest | Stack CI | Pemeriksaan |
|---|---|---|
| `package.json` | Node.js | npm ci, lint jika tersedia, test wajib, build jika tersedia |
| `pyproject.toml` atau `requirements.txt` | Python | instalasi dependency, lalu pytest |
| `composer.json` | PHP | validasi Composer, install lockfile, script test wajib |
| Tidak ada manifest di atas | Belum didukung | Job proyek gagal; implementasikan adapter sebelum merge |

Satu proyek boleh memiliki lebih dari satu stack. Setiap stack mendapatkan job terpisah
agar kegagalan satu stack tidak menyembunyikan hasil stack lainnya. Matriks dibatasi
maksimum empat job paralel untuk menjaga penggunaan runner.

Pengujian discovery mencakup dua bentuk berbeda: satu folder dengan beberapa manifest, dan beberapa folder proyek independen yang masing-masing memakai stack berbeda. Kasus kedua menjalankan CLI discovery sungguhan lalu memeriksa JSON matrix berisi `projects/alpha-node` (Node.js), `projects/beta-python` (Python), dan `projects/gamma-php` (PHP). Assertion juga memastikan ketiganya memiliki path proyek berbeda, sehingga test tidak dapat terpenuhi hanya dengan beberapa manifest dalam satu folder.

Jika `projects/` kosong, discovery menghasilkan sentinel `__no_projects__` agar
GitHub Actions tetap dapat menjalankan matrix yang valid. Sentinel ini bukan proyek
aplikasi dan tidak menggagalkan CI. Sebaliknya, folder proyek nyata tanpa manifest
Node.js, Python, atau PHP akan membuat job gagal dengan pesan untuk menambahkan
manifest yang didukung atau adapter CI. Dengan demikian proyek yang belum diuji tidak
dapat lolos sebagai sukses hanya karena job berisi perintah `echo`.

## Validasi web

Validasi web dijalankan terpisah dari matriks bahasa:

- HTML diparse dengan parser HTML5 strict.
- Referensi aset HTML dan CSS diperiksa keberadaannya.
- URL berawalan `/` diresolusikan dari root proyek; URL relatif diresolusikan dari
  direktori file sumber.
- Path traversal yang keluar dari folder proyek ditolak.
- Atribut `srcset` diparse per kandidat sehingga koma di dalam URL `data:` tidak
  memecah kandidat berikutnya.
- CSS diperiksa delimiter, deklarasi pada rule biasa, deklarasi di dalam at-rule
  seperti `@media` dan `@font-face`, serta URL aset.
- SVG diparse sebagai XML dan file kosong ditolak (kecuali `.gitkeep`).

Pemeriksaan CSS adalah validasi sintaks berbasis parser, bukan browser compatibility
test. Validator ini juga bukan pengganti visual regression, browser-based test, atau
audit accessibility penuh.

Validator Markdown saat ini memeriksa tautan internal dan anchor dalam repository.
Tautan HTTP/HTTPS eksternal sengaja dilewati: ketersediaan situs pihak ketiga tidak
menjadi syarat kelulusan PR karena dapat berubah atau gagal sementara. Karena itu,
status CI tidak menyatakan bahwa semua tautan eksternal masih aktif; periksa manual
saat meninjau dokumentasi yang bergantung pada referensi eksternal.

## Kontrak setiap proyek

- Node.js: commit `package-lock.json` dan sediakan script `test` di `package.json`.
  Script lint dan build dijalankan jika tersedia.
- Python: commit manifest dependency; gunakan `requirements-test.txt` atau
  `requirements-dev.txt` untuk dependency test. Jika keduanya tidak tersedia,
  CI menggunakan pytest versi yang dipatok oleh workflow. Test harus dapat ditemukan
  oleh `python -m pytest`.
- PHP: commit `composer.lock`, lolos `composer validate --strict`, dan sediakan
  script Composer bernama `test`.
- Stack lain belum dijalankan otomatis. Jangan menambahkan manifest tanpa adapter
  CI dan dokumentasi cara test.

# Dependabot

Dependabot is configured centrally in `.github/dependabot.yml`. On every PR and push,
`validate.yml` runs the pinned `@bugron/validate-dependabot-yaml` CLI against this file.
The validator parses the YAML and checks it against the Dependabot v2 JSON Schema,
then applies additional semantic checks such as duplicate/overlapping directories and
unsupported option combinations. Schema validation catches structural mistakes but
is not a replacement for GitHub's own Dependabot runtime validation. The active
configuration must point only to dependency manifests that actually exist:

| Scope | Dependabot ecosystem | Directory | Existing manifest / adapter |
|---|---|---|---|
| Repository automation | `github-actions` | `/` | `.github/workflows/*.yml` |
| Repository validation tooling | `pip` | `/` | `requirements-ci.txt` |
| Node.js projects | `npm` | `/projects/<slug>` | `package.json`; CI adapter requires `package-lock.json` |
| Python projects | `pip` | `/projects/<slug>` | `pyproject.toml` and/or `requirements*.txt` |
| PHP projects | `composer` | `/projects/<slug>` | `composer.json`; CI adapter requires `composer.lock` |

The project matrix currently implements Node.js, Python, and PHP adapters, but
`projects/` currently contains no project directories. Therefore only the two
repository-level entries (GitHub Actions and root pip tooling) are active in
Dependabot today. Do not add npm, project pip, or Composer entries until a
matching project manifest exists.

When a project is added, add a concrete Dependabot entry using that project's
directory and matching ecosystem in the same change that introduces its
manifest and lockfile. Avoid a broad `/projects/*` pattern while there are no
matching projects: Dependabot can report `dependency_file_not_found` when a
configured directory has no manifest. Do not create per-project Dependabot
configuration files; the root file is the single source of truth.

CI support and Dependabot update support are related but distinct contracts:
the CI adapter defines how a project is installed and tested, while Dependabot
defines where dependency manifests are scanned and updated. A stack being
supported by CI does not imply that a Dependabot directory exists yet.

## Proyek baru

Bootstrap resmi menambahkan `.project-meta.json` dengan nama, slug, versi template,
dan penunjuk orkestrasi CI root. Pilih stack dengan menambahkan manifest dan lockfile
yang sesuai. Tidak perlu membuat workflow CI atau konfigurasi Dependabot lokal.

Workflow juga menjalankan matriks bootstrap end-to-end terpisah untuk Node.js, Python,
dan PHP. Setiap job membuat proyek baru melalui CLI bootstrap pada direktori sementara,
menambahkan aplikasi contoh minimal, membuat lockfile yang diperlukan, memasang
dependency, dan menjalankan test aplikasi. Job ini menjaga contoh integrasi tetap
teruji tanpa menyimpan proyek fixture di `projects/`.

## Pengujian failure-path

Suite `scripts/tests/test_ci_failure_paths.py` membuat fixture sementara untuk memastikan jalur gagal CI benar-benar menolak:

- proyek tanpa manifest stack yang didukung;
- konfigurasi JSON Node.js/Composer dan TOML Python yang rusak;
- lockfile Node.js atau Composer yang hilang;
- dependency Python yang tidak tersedia.

Fixture dependency menggunakan pip `--no-index` dan wheelhouse kosong, sehingga kegagalan resolusi tidak bergantung pada jaringan atau layanan eksternal. Seluruh fixture dibersihkan setelah test dan tidak ditulis ke `projects/` repository.

## Verifikasi lokal

    python scripts/discover_projects.py
    python -m unittest discover -s scripts/tests -v

Untuk menjalankan test aplikasi secara lokal, ikuti perintah di docs/TESTING.md
masing-masing proyek. Seluruh hasil CI harus diperiksa pada PR sebelum merge.
