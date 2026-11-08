# Dependabot dan pemantauan dependency

## Konfigurasi aktif

Dependabot dikonfigurasi terpusat di .github/dependabot.yml. Jangan menambahkan
konfigurasi Dependabot di dalam folder proyek monorepo.

| Ecosystem | Direktori yang dipantau | Jadwal WIB |
|---|---|---:|
| GitHub Actions | / | Senin 02.00 |
| pip tooling repository | / | Senin 02.15 |
| npm | /projects/* | Senin 02.30 |
| pip proyek | /projects/* | Senin 02.45 |
| Composer | /projects/* | Senin 03.00 |

Semua pembaruan diarahkan ke main, menggunakan label ecosystem, dan dibatasi jumlah
PR terbuka per konfigurasi. Pembaruan minor dan patch GitHub Actions serta npm
dikelompokkan; pembaruan major tetap terpisah agar breaking changes dapat ditinjau.

Kunci directories mendukung beberapa direktori dan wildcard *. Dependabot akan
memproses direktori proyek yang cocok dan memiliki manifest yang relevan. Penambahan
proyek baru tidak memerlukan perubahan konfigurasi Dependabot selama proyek berada
langsung di bawah projects/.

Security updates mengikuti fitur security updates bawaan Dependabot GitHub. Status
aktif/nonaktif harus diverifikasi pada Settings → Security → Code security and analysis;
konfigurasi version updates tidak mengaktifkannya secara otomatis.

## Manifest dependency Python root

File requirements-ci.txt adalah manifest dependency Python untuk tooling validasi
repository. Dependabot ecosystem pip pada direktori root memantau file tersebut.
Jika dependency CI ditambahkan atau diubah, perbarui manifest ini dan pastikan workflow
validasi tetap lulus.

## Manifest dependency proyek

Setiap proyek dikelola dari direktori masing-masing:

- Node.js / npm: package.json dan lockfile yang didukung npm ecosystem.
- Python / pip: pyproject.toml, requirements.txt, atau manifest pip lain yang didukung.
- PHP / Composer: composer.json dan composer.lock.

Dependabot menggunakan pola /projects/*; tidak perlu membuat satu entry untuk setiap
slug proyek. Pastikan manifest dan lockfile berada langsung di folder proyek, bukan
hanya di subfolder aplikasi. Jika struktur proyek berbeda, ubah pola direktori secara
sengaja dan uji konfigurasi sebelum merge.

Ecosystem lain (Docker, Go, Rust, Java, Ruby, dan lainnya) ditambahkan saat proyek
pertama yang menggunakannya hadir dan format manifestnya sudah ditetapkan.

## Pinning GitHub Actions

Semua referensi Action yang dijalankan dalam workflow harus menggunakan commit SHA
penuh (40 karakter), disertai komentar versi rilis agar mudah dibaca. Hindari tag
bergerak seperti @v4 atau @v5 sebagai referensi eksekusi.

- SHA pin mengunci kode Action ke satu commit tertentu dan mengurangi risiko tag dipindahkan.
- Komentar versi membantu reviewer mengenali versi rilis yang dimaksud.
- Dependabot memantau referensi SHA dan dapat mengusulkan pembaruan ke commit rilis yang lebih baru.
- Setiap pembaruan SHA harus ditinjau melalui diff/changelog, kompatibilitas runtime, dan hasil CI sebelum digabungkan.

## Review pembaruan

1. Periksa changelog dan breaking changes dependency.
2. Tinjau pembaruan major secara khusus; jangan menganggap perubahan major otomatis kompatibel.
3. Jalankan CI, test, lint, dan build proyek terkait.
4. Periksa advisory keamanan serta kompatibilitas runtime.
5. Pastikan pemeriksaan wajib pada branch tujuan berhasil.
6. Merge hanya setelah hasil pemeriksaan relevan lulus.

## OSV-Scanner

Workflow .github/workflows/dependency-security.yml menjalankan OSV-Scanner
secara rekursif dari root repository. Cakupan ini mencakup dependency root,
template, dan proyek di bawah projects/.

Dependabot dan OSV-Scanner saling melengkapi:
- Dependabot mengusulkan pembaruan dependency.
- OSV-Scanner memeriksa apakah dependency yang digunakan memiliki advisory kerentanan yang diketahui.

Lulus pemindaian OSV bukan jaminan bahwa dependency bebas dari seluruh risiko; hasilnya
terbatas pada advisory yang tersedia dan cakupan file yang dipindai.
