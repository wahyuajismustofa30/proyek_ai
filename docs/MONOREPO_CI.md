# CI terpusat untuk monorepo

## Workflow

| Workflow | Tanggung jawab |
|---|---|
| `.github/workflows/validate.yml` | YAML/schema Dependabot, JSON, kompilasi Python, unit test tooling, kesegaran indeks, Markdown, link internal, whitespace |
| `.github/workflows/project-matrix.yml` | Discovery proyek, pemeriksaan aplikasi yang tersedia, smoke test website statis, validasi HTML/CSS/aset |
| `.github/workflows/dependency-security.yml` | OSV-Scanner untuk manifest dan lockfile |

Ketiga workflow berjalan pada push ke `main`. Workflow juga memiliki pemicu
Pull Request ke `main`, jadwal mingguan, atau manual sesuai konfigurasi
masing-masing file.

## Hubungan CI dengan perlindungan `main`

Ruleset **Protect main** (ID `26797557`) diverifikasi aktif pada
11 November 2026. Aturan yang terverifikasi adalah perlindungan penghapusan,
larangan non-fast-forward, dan kewajiban linear history.

Ruleset aktif tidak menetapkan Pull Request, approval, atau required status
checks. Repository menggunakan kebijakan **Direct Commit to Main**: commit
langsung ke `main` diperbolehkan dan Pull Request bersifat opsional, kecuali
pengguna meminta alur berbeda.

CI berjalan setelah push dan memberikan hasil pemeriksaan kualitas serta
keamanan. Hasil CI bukan gerbang required status checks pada ruleset, sehingga
workflow yang gagal tidak secara otomatis mencegah commit yang sudah ter-push.
Periksa hasil Actions setelah push dan tangani kegagalan yang ditemukan.

Rincian aturan perlindungan branch dicatat di
[dokumentasi perlindungan branch](BRANCH_PROTECTION.md). Periksa kembali
GitHub Settings → Rules → Rulesets karena konfigurasi live dapat berubah
tanpa perubahan pada file repository.

## Prinsip CI adaptif

CI tidak mewajibkan README, manifest, lockfile, script test, build, lint, atau
struktur direktori tertentu. Deteksi dilakukan dari file aktual.

| Stack | Perilaku |
|---|---|
| Node.js (`package.json`) | Validasi JSON manifest; jalankan `lint`, `test`, dan `build` jika tersedia. Gunakan `npm ci` jika lockfile ada. Tanpa lockfile, instalasi menghasilkan NOTICE. Tanpa script test, tes dilewati dengan NOTICE. |
| Python (`pyproject.toml` atau `requirements.txt`) | Validasi TOML jika ada. Jalankan pytest jika file tes Python ditemukan; jika tidak, NOTICE. Dependensi proyek hanya dipasang ketika tes tersedia. |
| PHP (`composer.json`) | Validasi manifest Composer. Instal dependensi dan jalankan script `test` jika script tersebut tersedia. Tanpa script test, NOTICE. |
| Static website | Kenali file `.html` atau `.htm` di root proyek. Pilih `index.html` bila ada, selain itu file pertama secara alfabetis sebagai entrypoint smoke test. |
| Stack lain | Tetap ditemukan; pemeriksaan aplikasi otomatis berstatus NOTICE sampai adapter yang sesuai tersedia. |

Script `scripts/run_project_checks.py` menjalankan pemeriksaan stack.
Script ini tidak menyatakan tes lulus jika tes tidak dikonfigurasi. Kesalahan
manifest, instalasi yang dibutuhkan, atau tes yang gagal menghasilkan FAIL.

### Status pemeriksaan

- **PASS:** pemeriksaan benar-benar dijalankan dan berhasil.
- **NOTICE:** pemeriksaan tidak tersedia atau tidak dikonfigurasi; bukan hasil tes lulus.
- **FAIL:** kesalahan nyata, manifest tidak valid, instalasi gagal, atau tes gagal.
- **NOT RUN:** pemeriksaan tidak dijalankan di luar alur CI.

## Discovery dan indeks

`scripts/discover_projects.py` menemukan direktori tingkat pertama di
`projects/<slug>/`. Satu proyek dapat memiliki beberapa adapter, misalnya
Node.js sekaligus website statis.

`scripts/update_project_index.py` adalah satu-satunya sumber kebenaran untuk
indeks. Termux menjalankan generator saat `projects/` berubah. Jalur upload
lain harus menjalankan:

```sh
python3 scripts/update_project_index.py --write
python3 scripts/update_project_index.py --check
```

CI memeriksa kesesuaian indeks; workflow tidak melakukan commit otomatis ke
branch pengguna.

## Detail validasi

- Pada Pull Request, workflow validasi memeriksa JSON dan Markdown yang
  berubah, menjalankan pemeriksaan repository, pemeriksaan whitespace.
- Pada push ke `main`, jadwal, atau pemicu manual, workflow validasi
  memeriksa seluruh Markdown dan tautan internal serta menjalankan pemeriksaan
  repository, dan whitespace.
- `scripts/check_static_site.py` menjalankan HTTP smoke test terhadap
  entrypoint terdeteksi.
- `scripts/validate_web_projects.py` memeriksa sintaks HTML/CSS, SVG/XML,
  dan referensi aset lokal. Ini bukan browser compatibility, visual
  regression, atau audit aksesibilitas penuh.
- Validasi web rekursif penuh pada `project-matrix.yml` berjalan untuk push
  ke `main`, jadwal, dan pemicu manual. Job tersebut dilewati pada Pull
  Request; discovery dan application tests tetap dijalankan dan job agregat
  menerima status skipped untuk validasi web.
- Tidak ada pemindaian secret otomatis; helper Termux hanya mempertahankan pemeriksaan dasar nama file sensitif.
- OSV-Scanner memindai dependency.
- Dependabot mengelola pembaruan workflow GitHub Actions dan tooling Python
  di root. Ecosystem proyek ditambahkan secara eksplisit bila memang digunakan.

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

Jalankan tes manual atau adapter tambahan untuk stack yang belum didukung.
Jangan menyamakan NOTICE dengan PASS.
