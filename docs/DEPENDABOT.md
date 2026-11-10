# Dependabot dan pemantauan dependency

## Konfigurasi version updates

Dependabot dikelola terpusat melalui `.github/dependabot.yml`. Konfigurasi
repository saat ini memiliki dua entri:

| Ecosystem | Direktori | Cakupan |
|---|---|---|
| GitHub Actions | `/` | Workflow GitHub Actions di repository |
| pip | `/` | Tooling validasi pada `requirements-ci.txt` |

Entri tersebut memantau dependency tooling di root repository. Keberadaan
adapter CI untuk Node.js, Python, atau PHP di dalam `projects/` tidak otomatis
membuat Dependabot memantau manifest proyek. Pemantauan version updates untuk
proyek harus dikonfigurasi secara eksplisit berdasarkan manifest dan ecosystem
yang benar-benar digunakan.

## Dependabot untuk proyek

Sebelum menambahkan entri proyek:

1. Periksa manifest dan lockfile yang benar-benar tersedia pada
   `projects/<slug>/`.
2. Pastikan proyek menggunakan dependency eksternal yang memang perlu
   diperbarui.
3. Tambahkan satu entri untuk ecosystem dan direktori proyek yang sesuai,
   misalnya `directory: /projects/<slug>`.
4. Validasi YAML/schema dan periksa hasil Dependabot setelah perubahan.

Pada snapshot repository 11 November 2026, `projects/testing/package.json`
hanya mendefinisikan script test dan tidak mencantumkan dependency eksternal;
`package-lock.json` juga tidak mencatat paket dependency tambahan. Karena itu,
entri npm untuk proyek tersebut belum memberi manfaat pembaruan dependency
saat ini. Evaluasi kembali jika dependency eksternal ditambahkan.

Gunakan [indeks proyek](PROJECT_INDEX.md) untuk melihat daftar direktori proyek
terkini. Jangan mengandalkan daftar proyek statis di dokumen ini.

## Jadwal dan kebijakan pembaruan

Kedua entri root dijadwalkan mingguan pada hari Senin dengan zona waktu
`Asia/Jakarta`:

| Ecosystem | Waktu | Batas PR terbuka |
|---|---:|---:|
| GitHub Actions | 02:00 | 10 |
| pip | 02:15 | 5 |

Keduanya menargetkan branch `main` dan menggunakan label kategori dependency.
Pembaruan minor/patch GitHub Actions dikelompokkan; pembaruan major tetap
terpisah. Periksa `.github/dependabot.yml` sebagai sumber konfigurasi kanonis
jika jadwal atau kebijakan berubah.

Dependabot security alerts dan security updates adalah fitur repository yang
terpisah dari version updates di file ini. Status keduanya harus diperiksa
langsung melalui Settings → Security → Code security and analysis; isi file
ini tidak membuktikan bahwa fitur tersebut aktif.

## Dependency CI Python

`requirements-ci.txt` berisi tooling validasi repository dan dipantau oleh
entri pip di root. Versi dependency dipatok, tetapi belum memakai
`--require-hashes`. Hash mode membutuhkan hash lengkap untuk seluruh
distribusi/platform dan proses pembaruan yang konsisten (misalnya pip-compile
atau uv); menambahkan hash manual berisiko menghasilkan daftar tidak lengkap.
Pertahankan pin versi saat ini sampai tool resmi dan alur regenerasi hash
ditetapkan, lalu uji perintah instalasi CI dengan `--require-hashes` sebelum
mengaktifkannya.

## Pemindaian keamanan dependency dan GitHub Actions

Workflow `.github/workflows/dependency-security.yml` menjalankan OSV-Scanner
secara rekursif untuk mencari advisory yang diketahui. Hasil bersih bukan
jaminan bebas risiko; cakupannya bergantung pada manifest, lockfile, dan
advisory yang tersedia.

Semua GitHub Actions harus dipatok ke full commit SHA 40 karakter dan disertai
komentar versi rilis. Tinjau changelog, kompatibilitas, hasil CI, dan advisory
sebelum menerima pembaruan dependency.
