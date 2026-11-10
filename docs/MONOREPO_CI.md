# CI terpusat untuk monorepo

## Workflow aktif

Seluruh orkestrasi berada di root repository.

| Workflow | Tanggung jawab |
|---|---|
| .github/workflows/validate.yml | YAML/schema, JSON, kompilasi Python, unit test tooling, kesegaran indeks, Markdown, link, secret, whitespace |
| .github/workflows/project-matrix.yml | Discovery proyek, adapter test yang dikenali, smoke test website statis, validasi HTML/CSS/aset, job agregat |
| .github/workflows/dependency-security.yml | OSV-Scanner rekursif untuk manifest dan lockfile |

Snapshot BRANCH_PROTECTION.md belum dapat diverifikasi ulang melalui integrasi GitHub pada audit ini. Jangan menganggap required checks aktif atau mengubah nama check tanpa memeriksa ruleset langsung di GitHub Settings.

## Discovery dan adapter CI

scripts/discover_projects.py menemukan direktori satu tingkat di projects/<slug>/. Struktur internal tidak dibatasi dan tidak ada README, metadata, source directory, test directory, atau manifest yang diwajibkan. Nama direktori tetap menggunakan slug huruf kecil, angka, dan tanda hubung; symlink langsung di bawah projects/ ditolak.

| Manifest | Adapter | Pemeriksaan |
|---|---|---|
| package.json | Node.js | package-lock.json wajib; lint/test/build jika tersedia dan test wajib |
| pyproject.toml atau requirements.txt | Python | Instalasi dependency proyek dan pytest |
| composer.json | PHP | composer.lock, validasi Composer, dan script test |
| index.html di root | Static website | HTTP smoke test halaman root |

Satu proyek dapat menghasilkan beberapa entri jika memiliki beberapa manifest yang dikenali. Static website dapat diuji bersamaan dengan adapter aplikasi.

Proyek tanpa adapter tetap masuk matriks dengan stack none. CI menampilkan notice bahwa pengujian aplikasi otomatis belum tersedia, tetapi tidak menggagalkan repository hanya karena teknologi belum dikenali. Tambahkan adapter ketika ada kebutuhan nyata.

Jika projects/ kosong, discovery menghasilkan sentinel __no_projects__ agar GitHub Actions tetap dapat membentuk matriks.

## Validasi web dan dokumentasi

scripts/check_static_site.py menjalankan HTTP smoke test untuk website dengan index.html di root. scripts/validate_web_projects.py memeriksa sintaks HTML/CSS, referensi aset lokal, batas path, dan parse SVG/XML. Pemeriksaan ini bukan browser compatibility, visual regression, atau audit aksesibilitas penuh.

scripts/check_internal_links.py memeriksa tautan Markdown dan anchor lokal. URL HTTP/HTTPS eksternal sengaja dilewati.

Indeks dibuat oleh scripts/update_project_index.py. Sinkronisasi Termux menjalankan generator ketika projects/ berubah; CI memeriksa docs/PROJECT_INDEX.md sesuai direktori aktual.

## Dependabot dan keamanan

Dependabot terpusat di .github/dependabot.yml. Pemantauan ecosystem proyek yang memiliki manifest/lockfile perlu ditambahkan secara eksplisit bila diperlukan. OSV-Scanner melengkapi Dependabot; Gitleaks memindai secret. Semua GitHub Actions dipatok ke full commit SHA dengan komentar versi.

## Pemeriksaan lokal

Dari root repository:

    python -m pip install -r requirements-ci.txt
    python -m compileall -q scripts
    python -m unittest discover -s scripts/tests -v
    python scripts/update_project_index.py --check
    python scripts/check_internal_links.py
    python scripts/discover_projects.py
    python scripts/validate_web_projects.py
    npx --yes markdownlint-cli2@0.18.1 "**/*.md"
    git diff --check

Jalankan test aplikasi sesuai stack yang dikenali dan dokumentasi yang tersedia. Proyek tanpa adapter memerlukan pemeriksaan manual atau adapter baru sebelum hasil test aplikasi dapat dinyatakan otomatis.
