# CI terpusat untuk monorepo

## Workflow aktif

Seluruh orkestrasi berada di root repository; workflow di dalam proyek tidak
dijalankan sebagai CI monorepo.

| Workflow | Tanggung jawab |
|---|---|
| `.github/workflows/validate.yml` | Dependabot YAML/schema, JSON, compile Python template dan scripts, unit test tooling, Markdown, link internal, secret, whitespace |
| `.github/workflows/project-matrix.yml` | Discovery proyek, test per stack, validasi HTML/CSS/aset, bootstrap E2E Node/Python/PHP, job agregat required check |
| `.github/workflows/dependency-security.yml` | OSV-Scanner rekursif untuk manifest dan lockfile |

Required checks tercatat di [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md):
`Validate JSON, Python, Markdown, links, and whitespace`,
`Scan dependencies with OSV-Scanner`, dan `Project matrix tests`.
Jangan mengubah nama job agregat atau nama job pemindai/validator tanpa
memeriksa ulang branch protection.

## Discovery dan kontrak stack

`scripts/discover_projects.py` hanya membaca direktori satu tingkat di
`projects/<slug>/`. Aturan nama, symlink, direktori tersembunyi, dan scaffold
diatur dalam [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md). Folder tersembunyi
di dalam proyek diperbolehkan; folder tersembunyi langsung di bawah
`projects/` ditolak.

| Manifest | Adapter | Kontrak |
|---|---|---|
| `package.json` | Node.js | `package-lock.json`, script `test`; lint/build jika tersedia |
| `pyproject.toml` atau `requirements.txt` | Python | dependency proyek, test ditemukan oleh pytest; CI memakai requirements-test/dev jika tersedia, atau pytest terpin |
| `composer.json` | PHP | `composer.lock`, `composer validate --strict`, script Composer `test` |
| `index.html` di root proyek | Static website | HTTP smoke test untuk memastikan halaman root disajikan dengan status 200 dan konten HTML yang benar; validasi HTML/CSS/aset lokal tetap dijalankan oleh job web-validation |
| Tidak didukung | — | Job proyek gagal; tambahkan adapter sebelum mengandalkan stack tersebut |

Setiap proyek static dikenali melalui `index.html` tepat di root proyek; file HTML di subfolder saja tidak otomatis menjadikan proyek static. Proyek dapat menghasilkan entri static sekaligus stack aplikasi bila memiliki `index.html` dan manifest aplikasi. Static website tidak memerlukan package manager atau test runner tambahan; CI melakukan HTTP smoke test dan tetap menjalankan validasi HTML/CSS/aset lokal secara terpusat.

Beberapa manifest dalam satu proyek menghasilkan job per stack. Matriks
membatasi paralelisme hingga empat. Jika `projects/` kosong, discovery
menghasilkan sentinel `__no_projects__`; sentinel bukan proyek aplikasi.
Folder proyek nyata tanpa stack yang didukung tetap gagal.

Tes discovery mencakup multi-manifest dalam satu proyek, beberapa proyek
independen lintas stack, aturan direktori tersembunyi, dan symlink.
Bootstrap E2E membuat fixture Node.js, Python, dan PHP di direktori sementara,
bukan menyimpan proyek contoh di `projects/`.

## Validasi web dan dokumentasi

`scripts/check_static_site.py` memverifikasi bahwa `index.html` root dapat disajikan melalui HTTP lokal dan mengembalikan konten HTML yang diharapkan. Test unitnya berada di `scripts/tests/test_check_static_site.py`.

`scripts/validate_web_projects.py` memeriksa HTML dengan parser HTML5 strict,
sintaks CSS menggunakan tinycss2, keberadaan referensi aset lokal, batas path
agar tidak keluar dari proyek, serta parse SVG/XML. Pemindaian melewati direktori dependency dan output/cache berikut di dalam
proyek: `node_modules/`, `.venv/`, `venv/`, `.git/`, dan `__pycache__/` pada
kedalaman mana pun. Direktori `vendor/`, `dist/`, dan `build/` hanya dilewati
jika berada langsung di root proyek. Direktori dengan nama tersebut di dalam
`src/` atau subdirektori lain tetap divalidasi sebagai source proyek.

Pemeriksaan ukuran nol hanya berlaku untuk file HTML/HTM, CSS, dan SVG.
File kosong bernama `.gitkeep`, `__init__.py`, atau `.nojekyll` diizinkan;
file kosong lain dengan ekstensi aset/web tersebut ditolak. File kosong dengan
ekstensi lain tidak diperiksa oleh aturan ukuran ini.

Pemeriksaan ini bukan browser compatibility, visual regression, atau audit aksesibilitas penuh.

`scripts/check_internal_links.py` memeriksa target tautan Markdown dan anchor
lokal. URL HTTP/HTTPS eksternal sengaja dilewati; ketersediaan situs pihak
ketiga bukan syarat CI.

## Dependabot dan keamanan

Konfigurasi Dependabot terpusat di `.github/dependabot.yml`. Saat ini hanya
GitHub Actions dan pip root (`requirements-ci.txt`) yang dipantau karena
`projects/` kosong. Tambahkan entri eksplisit per ecosystem hanya bersama
manifest/lockfile proyek nyata. Lihat [DEPENDABOT.md](DEPENDABOT.md).

OSV-Scanner melengkapi Dependabot dengan pemeriksaan advisory; keduanya tidak
menjamin dependency bebas seluruh risiko. Semua GitHub Actions dipatok ke full
commit SHA dengan komentar versi.

## Pemeriksaan lokal

Dari root repository:

```sh
python -m pip install -r requirements-ci.txt
python -m compileall -q templates scripts
python -m unittest discover -s scripts/tests -v
python scripts/check_internal_links.py
python scripts/discover_projects.py
python scripts/validate_web_projects.py
npx --yes markdownlint-cli2@0.18.1 "**/*.md"
git diff --check
```

Jalankan test aplikasi sesuai README dan dokumentasi testing masing-masing
proyek. Lihat [TESTING_STANDARDS.md](TESTING_STANDARDS.md) untuk kebijakan
cakupan test.
