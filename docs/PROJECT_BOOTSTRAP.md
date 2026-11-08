# Bootstrap Proyek Otomatis

Gunakan script scripts/bootstrap_project.py untuk membuat proyek baru dari
templates/ai-project/ tanpa menyalin folder secara manual.

## Persyaratan

- Python 3.10 atau lebih baru.
- Repository proyek_ai sudah di-clone.
- Jalankan perintah dari root repository atau gunakan path script yang benar.

## Penggunaan

Buat proyek dengan prompt interaktif:

    python scripts/bootstrap_project.py

Buat proyek langsung dengan nama:

    python scripts/bootstrap_project.py --name "DEKEKU Landing Page"

Perintah di atas membuat folder projects/dekeku-landing-page/. Untuk lokasi lain:

    python scripts/bootstrap_project.py --name "API Internal" --output ../workspace

Periksa target terlebih dahulu tanpa membuat file:

    python scripts/bootstrap_project.py --name "Proyek Percobaan" --dry-run

Lihat semua opsi:

    python scripts/bootstrap_project.py --help

## Yang dilakukan script

1. Mengubah nama menjadi slug folder yang aman (huruf kecil, angka, dan tanda hubung).
2. Menyalin template, termasuk instruksi AI, dokumen, aset, dan metadata proyek.
3. Mengganti placeholder nama dan slug proyek pada file teks UTF-8.
4. Menolak nama kosong, template yang tidak ditemukan, serta folder tujuan yang sudah ada.
5. Tidak menimpa file/folder yang ada dan tidak menjalankan perintah Git, install dependency, atau deployment.

Script tidak membuat repository Git terpisah. Proyek baru tetap berada di dalam repository utama
agar mengikuti struktur dan tata kelola proyek_ai.

## CI dan dependency

CI dan Dependabot dikelola secara terpusat oleh repository root:

- .github/workflows/project-matrix.yml mendeteksi manifest proyek di projects/*,
  menjalankan test Node.js/Python/PHP, dan memvalidasi HTML, CSS, serta referensi aset lokal.
- .github/workflows/validate.yml menjalankan pemeriksaan kualitas repository.
- .github/workflows/dependency-security.yml menjalankan OSV-Scanner secara rekursif.
- .github/dependabot.yml memantau GitHub Actions, dependency CI, serta dependency
  proyek pada direktori /projects/*.

Jangan membuat workflow CI atau .github/dependabot.yml di dalam folder proyek.
GitHub Actions dan Dependabot untuk monorepo ini dikendalikan dari root. Metadata
.project-meta.json mencatat nama, slug, versi template, dan lokasi orkestrator.

Stack yang didukung otomatis saat ini:
- Node.js: package.json + package-lock.json; script test wajib.
- Python: pyproject.toml atau requirements.txt; test dijalankan dengan pytest.
- PHP: composer.json + composer.lock; script Composer test wajib.

Stack lain memerlukan adapter CI sebelum dianggap diuji otomatis. Pemeriksaan HTML/CSS/aset berlaku untuk semua folder proyek, termasuk proyek tanpa stack aplikasi yang dikenali.

## Setelah bootstrap

- Lengkapi README.md dan docs/PROJECT_BRIEF.md.
- Tinjau AGENTS.md, arsitektur, task, keputusan, dan strategi testing.
- Pilih stack; tambahkan manifest dan lockfile yang sesuai.
- Pastikan perintah test cocok dengan workflow CI.
- Periksa secret, dependency, dan perubahan sebelum membuat PR.
- Tambahkan entri ke docs/PROJECT_INDEX.md setelah proyek benar-benar diterima sebagai proyek aktif.

## Pengujian bootstrap

Jalankan:

    python -m unittest discover -s scripts/tests -v

Tes mencakup slug, penyalinan dan penggantian placeholder, pencegahan overwrite,
mode dry-run, metadata template, serta discovery proyek dan stack CI. Tes end-to-end
menjalankan CLI bootstrap pada direktori sementara, memeriksa kelengkapan scaffold,
memastikan proyek ditemukan oleh matriks CI, lalu menjalankan validator web pada
fixture HTML/CSS/SVG/aset dan membuktikan referensi aset yang rusak ditolak.
