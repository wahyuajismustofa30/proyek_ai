# Dependabot dan pemantauan dependency

## Konfigurasi aktif

Dependabot dikelola terpusat melalui `.github/dependabot.yml`. Konfigurasi saat
ini hanya memiliki dua entri repository-level:

| Ecosystem | Direktori | Manifest/cakupan |
|---|---|---|
| GitHub Actions | `/` | Workflow GitHub Actions di repository |
| pip | `/` | `requirements-ci.txt` |

Repository sudah memiliki proyek aktif di dalam `projects/` (lihat
`docs/PROJECT_INDEX.md`). Namun, saat ini `.github/dependabot.yml` belum
memiliki entri khusus untuk manifest dependency pada masing-masing proyek.
Karena itu, jangan menganggap dependency proyek otomatis tercakup oleh dua
entri root di atas.

## Checklist saat menambahkan atau mengaktifkan pemantauan dependency proyek

Ketika sebuah proyek menggunakan dependency yang perlu dipantau:

1. Periksa manifest dan lockfile yang benar-benar digunakan proyek.
2. Tambahkan satu entri Dependabot eksplisit per ecosystem yang digunakan,
   dengan `directory: /projects/<slug>` dan `package-ecosystem` yang sesuai.
3. Pastikan direktori dan manifest yang dirujuk benar-benar ada. Jangan
   menambahkan entri spekulatif untuk ecosystem yang tidak digunakan.
4. Selaraskan konfigurasi dengan adapter CI dan kontrak lockfile proyek.
5. Validasi YAML dan pastikan Dependabot dapat menemukan manifest yang dirujuk.

Contoh pasangan manifest yang digunakan oleh adapter CI repository:
- Node.js: `package.json` dan `package-lock.json`.
- Python: `pyproject.toml` dan/atau `requirements*.txt`.
- PHP: `composer.json` dan `composer.lock`.

Persyaratan CI terhadap lockfile tidak selalu identik dengan kemampuan
Dependabot menemukan manifest. Pastikan keduanya didokumentasikan secara
terpisah dan sesuai implementasi aktual.

## Jadwal dan pembaruan

Jadwal repository-level menggunakan zona waktu `Asia/Jakarta`. Pembaruan
ditargetkan ke `main`, memakai label, dan dibatasi jumlah PR terbuka. GitHub
Actions dikelompokkan untuk pembaruan minor/patch; major tetap terpisah.

File ini mengatur version updates terjadwal. Dependabot security updates dan
alerts merupakan fitur repository terpisah yang perlu diperiksa di Settings →
Security → Code security and analysis.

## Dependency CI Python

`requirements-ci.txt` berisi tooling validasi repository dan dipantau oleh
entri pip di root. Versi dependency dipatok, tetapi belum memakai
`--require-hashes`. Hash mode membutuhkan hash lengkap untuk seluruh
distribusi/platform dan proses pembaruan yang konsisten (misalnya pip-compile
atau uv); menambahkan hash manual berisiko menghasilkan daftar tidak lengkap.
Pertahankan pin versi saat ini sampai tool resmi dan alur regenerasi hash
ditetapkan, lalu uji perintah instalasi CI dengan `--require-hashes` sebelum
mengaktifkannya.

## Keamanan dependency dan GitHub Actions

Workflow `.github/workflows/dependency-security.yml` menjalankan OSV-Scanner
secara rekursif untuk mencari advisory yang diketahui. Hasil bersih bukan
jaminan bebas risiko; cakupannya bergantung pada manifest, lockfile, dan
advisory yang tersedia.

Semua GitHub Actions harus dipatok ke full commit SHA 40 karakter dan disertai
komentar versi rilis. Tinjau changelog, kompatibilitas, hasil CI, dan advisory
sebelum menerima pembaruan dependency.
