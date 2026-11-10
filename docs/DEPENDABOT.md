# Dependabot dan pemantauan dependency

## Konfigurasi aktif

Dependabot dikelola terpusat melalui `.github/dependabot.yml`. Konfigurasi saat ini
memiliki dua entri repository-level:

| Ecosystem | Direktori | Manifest/cakupan |
|---|---|---|
| GitHub Actions | `/` | `.github/workflows/*.yml` |
| pip | `/` | `requirements-ci.txt` |

Direktori `projects/` **tidak kosong**. Pada snapshot repository yang diaudit,
terdapat proyek `preview` dan `testing`. Proyek `testing` memiliki
`package.json` dan `package-lock.json`, tetapi konfigurasi Dependabot saat ini
belum memiliki entri npm untuk `/projects/testing`. Dengan demikian, dependency
proyek tersebut tidak dipantau oleh version updates Dependabot.

Jangan menganggap dukungan adapter CI otomatis berarti Dependabot juga memantau
manifest proyek. Cakupan Dependabot ditentukan oleh entri ecosystem dan direktori
yang tertulis eksplisit di `.github/dependabot.yml`.

## Tindak lanjut untuk proyek

Saat proyek menggunakan manifest dependency yang perlu diperbarui secara otomatis:

1. Periksa manifest dan lockfile yang benar-benar ada pada proyek.
2. Tambahkan entri Dependabot eksplisit untuk ecosystem dan
   `directory: /projects/<slug>` yang sesuai.
3. Pastikan entri tidak menunjuk direktori atau manifest yang tidak ada.
4. Validasi YAML/schema dan tinjau hasil Dependabot setelah perubahan.

Pada kondisi audit ini, pertimbangkan entri npm untuk `/projects/testing`.
Perubahan konfigurasi Dependabot tidak dilakukan dalam audit dokumentasi ini.

## Jadwal dan pembaruan

Kedua entri repository-level dijadwalkan mingguan pada hari Senin dengan zona
waktu `Asia/Jakarta`: GitHub Actions pukul 02:00 dan pip pukul 02:15.
Keduanya menargetkan branch `main`, menggunakan label, dan membatasi jumlah
pull request terbuka. Pembaruan minor/patch GitHub Actions dikelompokkan;
pembaruan major tetap terpisah.

Dependabot security updates dan alerts merupakan fitur repository terpisah yang
perlu diperiksa di Settings → Security → Code security and analysis. Konfigurasi
version updates di file ini tidak membuktikan bahwa fitur security updates aktif.

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
