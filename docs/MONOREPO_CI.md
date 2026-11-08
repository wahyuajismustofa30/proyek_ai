# CI terpusat untuk monorepo

## Keputusan arsitektur

Repository menggunakan satu workflow aktif di root untuk menguji semua proyek di
projects/<slug>/. Workflow yang disalin ke subfolder proyek tidak otomatis dijalankan
oleh GitHub Actions. Karena itu, proyek di monorepo tidak boleh mengandalkan workflow
di projects/<slug>/.github/workflows/ sebagai CI aktif.

Workflow utama:

- .github/workflows/validate.yml: validasi repository, dokumentasi, JSON, Python,
  aset arsip, tautan internal, secret, dan whitespace.
- .github/workflows/project-matrix.yml: menemukan proyek dan menjalankan test
  stack per proyek.
- .github/workflows/dependency-security.yml: pemindaian OSV-Scanner rekursif
  untuk manifest dan lockfile di seluruh repository.

Semua workflow berjalan pada pull request ke main dan push ke main; project CI
juga memiliki jadwal mingguan dan pemicu manual.

## Cara discovery bekerja

Script scripts/discover_projects.py hanya memeriksa satu tingkat folder langsung
di bawah projects/. Setiap folder proyek dipetakan menjadi satu atau lebih job:

| Manifest | Stack CI | Pemeriksaan |
|---|---|---|
| package.json | Node.js | npm ci, lint jika tersedia, test wajib, build jika tersedia |
| pyproject.toml atau requirements.txt | Python | instalasi dependency, lalu pytest |
| composer.json | PHP | validasi Composer, install lockfile, script test wajib |
| Tidak ada manifest di atas | Belum didukung | Job memberi notice; validasi dan security scan root tetap berjalan |

Satu proyek boleh memiliki lebih dari satu stack. Setiap stack mendapatkan job terpisah
agar kegagalan satu stack tidak menyembunyikan hasil stack lainnya. Matriks dibatasi
maksimum empat job paralel untuk menjaga penggunaan runner.

Proyek tanpa stack yang didukung tidak dianggap lulus pengujian aplikasi. Statusnya
dilaporkan sebagai notice sampai adapter stack tersedia. Tambahkan adapter dan test
discovery sebelum memperluas stack yang didukung.

## Kontrak setiap proyek

- Node.js: commit package-lock.json dan sediakan script test di package.json.
  Script lint dan build dijalankan jika tersedia.
- Python: commit manifest dependency; gunakan requirements-test.txt atau
  requirements-dev.txt untuk dependency test. Jika keduanya tidak tersedia,
  CI menggunakan pytest versi yang dipatok oleh workflow. Test harus dapat ditemukan
  oleh python -m pytest.
- PHP: commit composer.lock, lolos composer validate --strict, dan sediakan
  script Composer bernama test.
- Stack lain belum dijalankan otomatis. Jangan menambahkan manifest tanpa adapter
  CI dan dokumentasi cara test.

## Dependabot

Dependabot hanya dikonfigurasi di .github/dependabot.yml root:

- GitHub Actions: direktori root.
- pip tooling repository: direktori root.
- npm, pip, dan Composer: pola direktori /projects/*.

Gunakan kunci directories untuk pola direktori monorepo. Jangan membuat
.github/dependabot.yml per proyek; konfigurasi bertingkat bukan sumber konfigurasi
Dependabot repository.

## Proyek baru

Bootstrap resmi menambahkan .project-meta.json dengan nama, slug, versi template,
dan penunjuk orkestrasi CI root. Pilih stack dengan menambahkan manifest dan lockfile
yang sesuai. Tidak perlu membuat workflow CI atau konfigurasi Dependabot lokal.

## Verifikasi lokal

    python scripts/discover_projects.py
    python -m unittest discover -s scripts/tests -v

Untuk menjalankan test aplikasi secara lokal, ikuti perintah di docs/TESTING.md
masing-masing proyek. Seluruh hasil CI harus diperiksa pada PR sebelum merge.
