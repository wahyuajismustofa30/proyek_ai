# CI terpusat untuk monorepo

## Workflow aktif

Seluruh orkestrasi berada di root repository; workflow di dalam proyek tidak
dijalankan sebagai CI monorepo.

| Workflow | Tanggung jawab |
|---|---|
| `.github/workflows/validate.yml` | Dependabot YAML/schema, JSON, compile Python template dan scripts, unit test tooling, Markdown, link internal, secret, whitespace |
| `.github/workflows/project-matrix.yml` | Discovery proyek, test per stack, validasi HTML/CSS/aset, bootstrap E2E Node/Python/PHP, job agregat status validasi proyek |
| `.github/workflows/dependency-security.yml` | OSV-Scanner rekursif untuk manifest dan lockfile |

Nama job di atas merupakan nama yang didefinisikan oleh source workflow.
[BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) menyimpan snapshot required checks
dari ruleset yang pernah diverifikasi, tetapi status required checks pada
GitHub Settings belum dapat dibaca ulang dalam audit 2026-11-09. Karena itu,
jangan menyebutnya sebagai merge gate yang dipastikan aktif sampai ruleset
diperiksa langsung. Sebelum mengubah nama job agregat atau job validator,
verifikasi kembali konfigurasi ruleset dan sinkronkan nama check yang diwajibkan.

## Discovery dan kontrak stack

`scripts/discover_projects.py` hanya membaca direktori satu tingkat di
`projects/<slug>/`. Aturan nama, symlink, direktori tersembunyi, dan scaffold
diatur dalam [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md). Discovery juga menolak file root selain `README.md`, dependency/cache umum, file log/sementara, dan output build/coverage yang terdeteksi. Folder tersembunyi
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
independen lintas stack, aturan direktori tersembunyi, symlink, file root, serta
penolakan artefak dependency/cache dan file sementara. Bootstrap E2E membuat
fixture Node.js, Python, dan PHP di direktori sementara di luar repository.
Script fixture menolak output yang berada di dalam repository, sedangkan bootstrap
proyek tetap mengizinkan output default ke root `projects/` dan menolak output
yang bersarang di dalam proyek lain.

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

Konfigurasi Dependabot terpusat di `.github/dependabot.yml`. Saat ini pemantauan
mencakup GitHub Actions dan pip root (`requirements-ci.txt`). Manifest proyek tidak
didaftarkan otomatis oleh konfigurasi tersebut; tambahkan entri ecosystem secara
eksplisit ketika proyek nyata memakai manifest/lockfile yang perlu dipantau.
Lihat [DEPENDABOT.md](DEPENDABOT.md).

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
