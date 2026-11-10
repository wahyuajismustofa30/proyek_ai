# CI terpusat untuk monorepo

## Workflow

| Workflow | Tanggung jawab |
|---|---|
| `.github/workflows/validate.yml` | YAML/schema, JSON, kompilasi Python, unit test tooling, kesegaran indeks, Markdown, link, secret, whitespace |
| `.github/workflows/project-matrix.yml` | Discovery, pemeriksaan aplikasi yang tersedia, smoke test website statis, validasi HTML/CSS/aset |
| `.github/workflows/dependency-security.yml` | OSV-Scanner untuk manifest dan lockfile |

Snapshot branch protection di `docs/BRANCH_PROTECTION.md` adalah catatan historis. Verifikasi live required checks melalui GitHub Settings → Rules → Rulesets; nama job dalam file workflow tidak membuktikan bahwa job tersebut diwajibkan oleh ruleset.

## Prinsip CI adaptif

CI tidak mewajibkan README, manifest, lockfile, script test, build, lint, atau struktur direktori tertentu. Deteksi dilakukan dari file aktual.

| Stack | Perilaku |
|---|---|
| Node.js (`package.json`) | Validasi JSON manifest; jalankan `lint`, `test`, dan `build` jika tersedia. Gunakan `npm ci` jika lockfile ada. Tanpa lockfile, instalasi menghasilkan NOTICE. Tanpa script test, tes dilewati dengan NOTICE. |
| Python (`pyproject.toml` atau `requirements.txt`) | Validasi TOML jika ada. Jalankan pytest jika file tes Python ditemukan; jika tidak, NOTICE. Dependensi proyek hanya dipasang ketika tes tersedia. |
| PHP (`composer.json`) | Validasi manifest Composer. Instal dependensi dan jalankan script `test` jika script tersebut tersedia. Tanpa script test, NOTICE. |
| Static website | Kenali file `.html` atau `.htm` di root proyek. Pilih `index.html` bila ada, selain itu file pertama secara alfabetis sebagai entrypoint smoke test. |
| Stack lain | Tetap ditemukan; pemeriksaan aplikasi otomatis berstatus NOTICE sampai adapter yang sesuai tersedia. |

Script `scripts/run_project_checks.py` menjalankan pemeriksaan stack. Script ini tidak menyatakan tes lulus jika tes tidak dikonfigurasi. Kesalahan manifest, instalasi yang dibutuhkan, atau tes yang gagal menghasilkan FAIL.

### Status pemeriksaan

- **PASS:** pemeriksaan benar-benar dijalankan dan berhasil.
- **NOTICE:** pemeriksaan tidak tersedia atau tidak dikonfigurasi; bukan hasil tes lulus.
- **FAIL:** kesalahan nyata, manifest tidak valid, instalasi gagal, atau tes gagal.
- **NOT RUN:** pemeriksaan tidak dijalankan di luar alur CI.

## Discovery dan indeks

`scripts/discover_projects.py` menemukan direktori tingkat pertama di `projects/<slug>/`. Satu proyek dapat memiliki beberapa adapter, misalnya Node.js sekaligus website statis.

`scripts/update_project_index.py` adalah satu-satunya sumber kebenaran untuk indeks. Termux menjalankan generator saat `projects/` berubah. Jalur upload lain harus menjalankan:

```sh
python3 scripts/update_project_index.py --write
python3 scripts/update_project_index.py --check
```

CI memeriksa kesesuaian indeks; workflow tidak melakukan commit otomatis ke branch pengguna.

## Validasi web dan keamanan

- `scripts/check_static_site.py` menjalankan HTTP smoke test terhadap entrypoint terdeteksi.
- `scripts/validate_web_projects.py` memeriksa sintaks HTML/CSS, SVG/XML, dan referensi aset lokal. Ini bukan browser compatibility, visual regression, atau audit aksesibilitas penuh.
- Gitleaks memindai secret.
- OSV-Scanner memindai dependency.
- Dependabot mengelola pembaruan workflow GitHub Actions dan tooling Python di root. Ecosystem proyek ditambahkan secara eksplisit bila memang digunakan.

## Pemeriksaan lokal

Dari root repository:

```sh
python -m pip install -r requirements-ci.txt
python -m compileall -q scripts
python -m unittest discover -s scripts/tests -v
python scripts/update_project_index.py --check
python scripts/check_internal_links.py
python scripts/discover_projects.py
python scripts/validate_web_projects.py
npx --yes markdownlint-cli2@0.18.1 "**/*.md"
git diff --check
```

Jalankan tes manual atau adapter tambahan untuk stack yang belum didukung. Jangan menyamakan NOTICE dengan PASS.
