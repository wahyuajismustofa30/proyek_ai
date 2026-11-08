# Dependabot dan pemantauan dependency

## Konfigurasi aktif

Dependabot dikonfigurasi terpusat di `.github/dependabot.yml`. Jangan menambahkan
konfigurasi Dependabot di dalam folder proyek monorepo.

Setiap entri stack proyek menggunakan `directories: ["/projects/*"]`. Wildcard
ini mencakup setiap direktori proyek satu tingkat di bawah `projects/`. Dependabot
hanya membuat pembaruan untuk direktori yang berisi manifest/lockfile yang dikenali
oleh ecosystem terkait; entri untuk stack yang belum digunakan bersifat siap pakai
dan tidak memerlukan manifest palsu.

| Ecosystem | Stack / manifest umum | Direktori | Jadwal WIB |
|---|---|---|---:|
| GitHub Actions | workflow dan action metadata | / | Senin 02.00 |
| pip | requirements-ci.txt (tooling repository) | / | Senin 02.15 |
| npm | package.json, npm lockfiles | /projects/* | Senin 02.30 |
| pip | requirements.txt, pyproject.toml | /projects/* | Senin 02.45 |
| Composer | composer.json / composer.lock | /projects/* | Senin 03.00 |
| Bundler | Gemfile / Gemfile.lock | /projects/* | Senin 03.15 |
| Go modules | go.mod / go.sum | /projects/* | Senin 03.30 |
| Cargo | Cargo.toml / Cargo.lock | /projects/* | Senin 03.45 |
| Maven | pom.xml | /projects/* | Senin 04.00 |
| Gradle | build.gradle(.kts) | /projects/* | Senin 04.15 |
| NuGet | *.csproj, packages.config, *.sln | /projects/* | Senin 04.30 |
| .NET SDK | global.json | /projects/* | Senin 04.45 |
| Mix | mix.exs / mix.lock | /projects/* | Senin 05.00 |
| Pub | pubspec.yaml / pubspec.lock | /projects/* | Senin 05.15 |
| Swift | Package.swift / Package.resolved | /projects/* | Senin 05.30 |
| Terraform | *.tf, .terraform.lock.hcl | /projects/* | Senin 05.45 |
| OpenTofu | *.tf, .terraform.lock.hcl | /projects/* | Senin 06.00 |
| Docker | Dockerfile | /projects/* | Senin 06.15 |
| Docker Compose | compose.yaml / docker-compose.yml | /projects/* | Senin 06.30 |
| Dev containers | devcontainer.json | /projects/* | Senin 06.45 |
| Helm | Chart.yaml | /projects/* | Senin 07.00 |
| Bazel | MODULE.bazel / WORKSPACE | /projects/* | Senin 07.15 |
| Nix | flake.nix | /projects/* | Senin 07.30 |
| pre-commit | .pre-commit-config.yaml | /projects/* | Senin 07.45 |
| Bun | bun.lock / bun.lockb | /projects/* | Senin 08.00 |
| Deno | deno.json / deno.jsonc | /projects/* | Senin 08.15 |
| uv | pyproject.toml / uv.lock | /projects/* | Senin 08.30 |
| Rust toolchain | rust-toolchain.toml | /projects/* | Senin 08.45 |
| Git submodules | .gitmodules | /projects/* | Senin 09.00 |

Jadwal memakai zona waktu `Asia/Jakarta`. Semua pembaruan diarahkan ke `main`,
menggunakan label stack, dan memiliki batas jumlah PR terbuka per konfigurasi.
Pembaruan minor/patch npm dan GitHub Actions dikelompokkan; major tetap terpisah
agar perubahan berisiko dapat ditinjau sendiri.

## Aturan struktur monorepo

1. Letakkan setiap proyek langsung di `projects/<slug>/`.
2. Simpan manifest dan lockfile di direktori proyek tersebut atau sesuaikan cakupan
   `directories` secara eksplisit jika manifest berada di subfolder.
3. Jangan menambahkan file `.github/dependabot.yml` di dalam proyek.
4. Bila memakai ecosystem yang belum tercantum, tambahkan satu entri terpusat
   berdasarkan dokumentasi resmi GitHub sebelum proyek bergantung padanya.
5. Bila satu proyek memakai beberapa stack, setiap ecosystem yang relevan akan
   memindai direktori yang sama; Dependabot membuat PR sesuai dependency yang ditemukan.

## Version updates dan security updates

Konfigurasi ini mengatur version updates terjadwal. Dependabot security updates
berjalan melalui fitur repository GitHub yang terpisah. Pastikan fitur tersebut
aktif di Settings → Security → Code security and analysis. File `dependabot.yml`
tidak otomatis mengaktifkan Dependabot alerts atau security updates.

## Manifest dependency Python root

File `requirements-ci.txt` adalah manifest dependency Python untuk tooling validasi
repository. Dependabot ecosystem pip pada direktori root memantau file tersebut.
Jika dependency CI ditambahkan atau diubah, perbarui manifest ini dan pastikan workflow
validasi tetap lulus.

## Pinning GitHub Actions

Semua referensi Action dalam workflow harus menggunakan commit SHA penuh (40 karakter),
disertai komentar versi rilis. Dependabot memantau referensi SHA dan dapat mengusulkan
pembaruan. Tinjau changelog, kompatibilitas runtime, dan hasil CI sebelum merge.

## Review pembaruan

1. Periksa changelog dan breaking changes dependency.
2. Tinjau pembaruan major secara khusus.
3. Jalankan CI, test, lint, dan build proyek terkait.
4. Periksa advisory keamanan serta kompatibilitas runtime.
5. Pastikan pemeriksaan wajib pada branch tujuan berhasil.
6. Merge hanya setelah pemeriksaan relevan lulus.

## OSV-Scanner

Workflow `.github/workflows/dependency-security.yml` menjalankan OSV-Scanner
secara rekursif dari root repository. Cakupan ini melengkapi Dependabot:

- Dependabot mengusulkan pembaruan dependency.
- OSV-Scanner memeriksa advisory kerentanan yang diketahui.

Lulus pemindaian OSV bukan jaminan bahwa dependency bebas dari seluruh risiko;
hasilnya terbatas pada advisory yang tersedia dan cakupan file yang dipindai.
