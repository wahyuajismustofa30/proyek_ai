# Ruang Kerja Proyek

Folder ini menampung proyek aplikasi dan tooling yang dipelihara di repository.
Tidak semua direktori di bawah projects/ merupakan proyek mandiri: sebagian
berfungsi sebagai kategori atau wadah untuk proyek bertingkat.

## Klasifikasi

Daftar resmi dipelihara di [katalog proyek](../docs/project-catalog.json) dan
ditampilkan melalui [indeks proyek](../docs/PROJECT_INDEX.md).

- **Proyek** adalah unit kerja mandiri dengan tujuan dan siklus pemeliharaan sendiri.
- **Kategori/wadah** mengelompokkan proyek terkait. Contohnya projects/whatsapp/
  yang menaungi gowa-gemini-bridge/; folder kategori bukan proyek aplikasi.
- **Tooling** berisi utilitas pengembangan atau operasional, bukan aplikasi produk.
  Contohnya projects/termux/.

Proyek boleh berada langsung di bawah projects/ atau di dalam folder kategori.
Tambahkan lokasi proyek yang sebenarnya ke docs/project-catalog.json; jangan
mendaftarkan subfolder halaman, aset, fixture, dependency, cache, atau hasil build.

## Struktur dan bootstrap

Gunakan nama direktori lowercase ASCII, angka, dan tanda hubung. Hindari direktori
tersembunyi untuk draft/arsip. Direktori konfigurasi tersembunyi di dalam proyek,
seperti .github/ atau .config/, diperbolehkan.

Setiap proyek mengikuti [aturan struktur proyek](../docs/PROJECT_STRUCTURE.md).
Bootstrap saat ini membuat proyek di tingkat pertama projects/<slug>/.
Untuk proyek dalam kategori, buat direktori pada lokasi kategori yang sesuai,
lalu daftarkan path lengkapnya pada katalog. Jangan menganggap bootstrap telah
mendukung nested path.

## Batasan root

Jangan menaruh fixture, arsip, backup, file sementara, cache, dependency, log,
hasil build, laporan, atau artefak pengujian langsung di root projects/.
Gunakan direktori sementara sistem/CI untuk kebutuhan pengujian dan output yang
dapat dibuat ulang.
