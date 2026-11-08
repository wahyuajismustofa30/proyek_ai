# Dependabot dan pemantauan dependency

## Konfigurasi aktif

Dependabot dikonfigurasi di `.github/dependabot.yml`. Saat ini repository menggunakan GitHub Actions sebagai satu-satunya ecosystem dependency yang dapat dipantau secara nyata.

- **GitHub Actions:** diperiksa setiap Senin pukul 02.00 WIB.
- **Pengelompokan:** pembaruan minor dan patch Actions digabungkan dalam satu grup agar pull request tidak berlebihan.
- **Major update:** tetap dibuat terpisah untuk memudahkan review perubahan yang berpotensi memerlukan penyesuaian.
- **Pull request:** target branch `main`, label `dependencies` dan `github-actions`, maksimum 10 PR terbuka.
- **Security updates:** tetap mengikuti fitur security updates bawaan Dependabot GitHub; jadwal version updates tidak menggantikan pemeriksaan keamanan.

## Inventaris stack saat ini

| Area | Kondisi repository | Dependabot |
|---|---|---|
| GitHub Actions | Workflow CI dan dependency security aktif | Aktif |
| Python | Script validasi memakai standard library; belum ada manifest dependency | Belum perlu konfigurasi pip |
| Node.js / npm | Belum ada `package.json` atau lockfile | Belum diaktifkan |
| PHP / Composer | Belum ada `composer.json` atau lockfile | Belum diaktifkan |
| Docker | Belum ada Dockerfile atau image dependency | Belum diaktifkan |
| Go / Rust / Java / Ruby | Belum ada manifest stack tersebut | Belum diaktifkan |

Jangan menambahkan ecosystem hanya berdasarkan kemungkinan teknologi yang akan dipakai. Dependabot memerlukan manifest atau file dependency yang nyata agar dapat memeriksa versi dan membuat pembaruan yang valid.

## Kapan ecosystem ditambahkan

Saat proyek mulai menggunakan stack berikut, tambahkan entry Dependabot dengan `directory` yang menunjuk folder manifest proyek:

- Python: `pip` untuk `requirements.txt`, `pyproject.toml`, atau manifest yang didukung.
- Node.js: `npm` untuk `package.json` dan lockfile terkait.
- PHP: `composer` untuk `composer.json` dan `composer.lock`.
- Container: `docker` untuk Dockerfile yang benar-benar digunakan.
- GitHub Actions tetap dipantau pada root repository.

Untuk monorepo, buat entry terpisah per direktori proyek yang memiliki manifest. Jangan menunjuk ke folder yang belum memiliki manifest karena konfigurasi tersebut tidak memberi pemantauan yang berguna.

## Review pembaruan

1. Periksa changelog dan breaking changes dari dependency.
2. Pastikan perubahan tidak menaikkan versi major secara otomatis tanpa review.
3. Jalankan CI, test, lint, dan build proyek terkait.
4. Periksa advisory keamanan dan kompatibilitas runtime.
5. Merge hanya setelah hasil pemeriksaan relevan lulus.

OSV-Scanner di workflow `.github/workflows/dependency-security.yml` tetap menjadi pemindaian kerentanan dependency berbasis manifest/lockfile. OSV-Scanner dan Dependabot saling melengkapi: Dependabot mengusulkan pembaruan, sedangkan scanner memeriksa advisory yang diketahui.
