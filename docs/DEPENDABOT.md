# Dependabot dan pemantauan dependency

## Konfigurasi aktif

Dependabot dikonfigurasi di `.github/dependabot.yml`. Repository saat ini memantau dua ecosystem yang benar-benar digunakan:

- **GitHub Actions:** diperiksa setiap Senin pukul 02.00 WIB (`Asia/Jakarta`).
- **Python / pip:** diperiksa setiap Senin pukul 02.15 WIB (`Asia/Jakarta`), berdasarkan manifest root `requirements-ci.txt`.
- **Target pull request:** branch `main`.
- **Label:** `dependencies` dan label ecosystem (`github-actions` atau `python`).
- **Batas PR terbuka:** maksimum 10 untuk GitHub Actions dan 5 untuk pip.
- **Pengelompokan Actions:** pembaruan minor dan patch digabungkan dalam grup `github-actions`; pembaruan major tetap dibuat terpisah agar breaking changes dapat ditinjau.
- **Pembaruan pip:** saat ini tidak dikelompokkan, sehingga usulan dependency dapat ditinjau secara individual.

Security updates mengikuti fitur security updates bawaan Dependabot GitHub. Status aktif/nonaktif harus diverifikasi pada Settings → Security → Code security and analysis; konfigurasi version updates di `.github/dependabot.yml` tidak mengaktifkannya secara otomatis.

## Manifest dependency Python

File `requirements-ci.txt` adalah manifest dependency Python untuk tooling validasi repository. Saat ini isinya:

- `markdown-it-py==4.2.0`

Dependabot ecosystem `pip` menggunakan `directory: /` untuk memantau manifest tersebut. Jika dependency CI ditambahkan atau diubah, perbarui manifest ini dan pastikan workflow validasi tetap lulus.

Script validasi lain yang hanya menggunakan standard library Python tidak memerlukan dependency tambahan.

## Pinning GitHub Actions

Semua referensi Action yang dijalankan dalam workflow harus menggunakan commit SHA penuh (40 karakter), disertai komentar versi rilis agar mudah dibaca. Hindari tag bergerak seperti `@v4` atau `@v5` sebagai referensi eksekusi.

- SHA pin mengunci kode Action ke satu commit tertentu dan mengurangi risiko tag dipindahkan.
- Komentar versi membantu reviewer mengenali versi rilis yang dimaksud.
- Dependabot memantau referensi SHA dan dapat mengusulkan pembaruan ke commit rilis yang lebih baru.
- Setiap pembaruan SHA harus ditinjau melalui diff/changelog, kompatibilitas runtime, dan hasil CI sebelum digabungkan.
- Contoh Action dalam template juga harus menggunakan SHA pin agar aman saat diaktifkan.

## Inventaris ecosystem

| Area | Kondisi repository | Dependabot |
|---|---|---|
| GitHub Actions | Workflow CI dan dependency security aktif | Aktif |
| Python / pip | `requirements-ci.txt` berisi dependency tooling CI | Aktif |
| Node.js / npm | Belum ada `package.json` atau lockfile yang digunakan repository | Belum diaktifkan |
| PHP / Composer | Belum ada `composer.json` atau `composer.lock` | Belum diaktifkan |
| Docker | Belum ada Dockerfile atau image dependency yang digunakan | Belum diaktifkan |
| Go / Rust / Java / Ruby | Belum ada manifest dependency terkait | Belum diaktifkan |

Jangan menambahkan ecosystem hanya berdasarkan kemungkinan teknologi yang akan dipakai. Dependabot memerlukan manifest atau file dependency nyata agar dapat memeriksa versi dan membuat pembaruan yang valid.

## Kapan ecosystem ditambahkan

Saat proyek mulai menggunakan stack berikut, tambahkan entry Dependabot dengan `directory` yang menunjuk folder manifest proyek:

- Python: `pip` untuk `requirements.txt`, `requirements-ci.txt`, `pyproject.toml`, atau manifest yang didukung.
- Node.js: `npm` untuk `package.json` dan lockfile terkait.
- PHP: `composer` untuk `composer.json` dan `composer.lock`.
- Container: `docker` untuk Dockerfile yang benar-benar digunakan.
- GitHub Actions tetap dipantau pada root repository.

Untuk monorepo, buat entry terpisah per direktori proyek yang memiliki manifest. Jangan menunjuk ke folder yang belum memiliki manifest karena konfigurasi tersebut tidak memberi pemantauan yang berguna.

## Review pembaruan

1. Periksa changelog dan breaking changes dependency.
2. Tinjau pembaruan major secara khusus; jangan menganggap perubahan major otomatis kompatibel.
3. Jalankan CI, test, lint, dan build proyek terkait.
4. Periksa advisory keamanan serta kompatibilitas runtime.
5. Pastikan pemeriksaan wajib pada branch tujuan berhasil.
6. Merge hanya setelah hasil pemeriksaan relevan lulus.

## OSV-Scanner

Workflow `.github/workflows/dependency-security.yml` menjalankan OSV-Scanner untuk memeriksa kerentanan yang diketahui pada manifest dan lockfile yang terdeteksi.

Dependabot dan OSV-Scanner saling melengkapi:
- Dependabot mengusulkan pembaruan dependency.
- OSV-Scanner memeriksa apakah dependency yang digunakan memiliki advisory kerentanan yang diketahui.

Lulus pemindaian OSV bukan jaminan bahwa dependency bebas dari seluruh risiko; hasilnya terbatas pada advisory yang tersedia dan cakupan file yang dipindai.
