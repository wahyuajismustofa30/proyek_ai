# Dependabot dan pemantauan dependency

## Konfigurasi aktif

Dependabot dikelola terpusat melalui `.github/dependabot.yml`. Saat ini hanya dua
entri repository-level yang aktif:

| Ecosystem | Direktori | Manifest |
|---|---|---|
| GitHub Actions | `/` | `.github/workflows/*.yml` |
| pip | `/` | `requirements-ci.txt` |

Folder `projects/` sengaja kosong. Jangan menambahkan entri untuk
`/projects/*` atau proyek yang belum ada; direktori tanpa manifest yang cocok
dapat menghasilkan `dependency_file_not_found`. Jangan membuat konfigurasi
Dependabot lokal di dalam proyek.

## Checklist saat proyek pertama dibuat

Dalam PR yang sama dengan penambahan proyek:

1. Tambahkan manifest nyata untuk setiap ecosystem yang dipakai.
2. Commit lockfile yang sesuai dengan stack dan kontrak CI:
   - Node.js: `package.json` dan `package-lock.json`.
   - Python: `pyproject.toml` atau `requirements*.txt`; commit lockfile bila
     dipakai oleh workflow/package manager proyek.
   - PHP: `composer.json` dan `composer.lock`.
3. Tambahkan satu entri Dependabot eksplisit per ecosystem, dengan
   `directory: /projects/<slug>` dan `package-ecosystem` yang tepat.
4. Pastikan entri hanya menunjuk direktori/manifest yang benar-benar ada,
   lalu jalankan validasi YAML/schema pada workflow repository.
5. Sinkronkan kontrak tersebut dengan adapter CI dan dokumentasikan stack baru.

Jangan menambahkan entri ecosystem yang tidak digunakan hanya karena adapter CI
mendukungnya. Dukungan CI dan cakupan Dependabot adalah dua hal terpisah.

## Jadwal dan pembaruan

Jadwal repository-level menggunakan zona waktu `Asia/Jakarta`. Semua pembaruan
ditargetkan ke `main`, memakai label, dan dibatasi jumlah PR terbuka. GitHub Actions
dikelompokkan untuk pembaruan minor/patch; major tetap terpisah.

File ini mengatur version updates terjadwal. Dependabot security updates dan alerts
merupakan fitur repository terpisah yang perlu diperiksa di Settings → Security →
Code security and analysis.

## Dependency CI Python

`requirements-ci.txt` berisi tooling validasi repository dan dipantau oleh entri
pip di root. Versi dependency dipatok, tetapi belum memakai `--require-hashes`.
Hash mode membutuhkan hash lengkap untuk seluruh distribusi/platform dan proses
pembaruan yang konsisten (misalnya pip-compile atau uv); menambahkan hash manual
berisiko menghasilkan daftar tidak lengkap. Pertahankan pin versi saat ini sampai
tool resmi dan alur regenerasi hash ditetapkan, lalu uji perintah instalasi CI
dengan `--require-hashes` sebelum mengaktifkannya.

## Keamanan dependency dan GitHub Actions

Workflow `.github/workflows/dependency-security.yml` menjalankan OSV-Scanner
secara rekursif untuk mencari advisory yang diketahui. Hasil bersih bukan jaminan
bebas risiko; cakupannya bergantung pada manifest, lockfile, dan advisory yang
tersedia.

Semua GitHub Actions harus dipatok ke full commit SHA 40 karakter dan disertai
komentar versi rilis. Tinjau changelog, kompatibilitas, hasil CI, dan advisory
sebelum menerima pembaruan dependency.
