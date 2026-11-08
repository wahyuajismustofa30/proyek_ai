# DEKEKU Brand System

## Tujuan
Sumber acuan visual bersama untuk website bisnis dan undangan online DEKEKU.

## Struktur
- `versions/v1.1/source/Dekeku/`: source baseline hasil ekstraksi paket v1.1, dipertahankan tanpa modifikasi.
- `docs/`: dokumentasi pengembangan brand system berikutnya.
- `archives/`: tidak digunakan untuk salinan paket; arsip asli dipusatkan di root `/archives`.

## Baseline
- Versi baseline repository: v1.1 (label arsip yang ditetapkan pemilik).
- Metadata internal paket masih menyebut v1.5 pada beberapa dokumen. Jangan menyamakan kedua label secara otomatis.
- Source v1.1 adalah referensi read-only.
- Untuk pembaruan, buat versi baru seperti `versions/v1.2/` setelah requirement dan perubahan disepakati.

## Area penting
- `tokens/`: design tokens JSON dan CSS.
- `assets/logo/`: logo horizontal dan compact.
- `assets/icon/`: ikon brand.
- `assets/maskot/`: maskot SVG/PNG.
- `public/`: favicon dan metadata PWA.
- `referensi/`: halaman referensi tema.
- `scripts/`: skrip pembangun aset/token.

## Identitas logo resmi
Paket logo yang diberikan pemilik ditetapkan sebagai acuan identitas visual untuk pekerjaan DEKEKU berikutnya. Aturan, inventaris, warna, dan catatan teknis: [OFFICIAL_LOGO_PACKAGE.md](docs/OFFICIAL_LOGO_PACKAGE.md). Aset baseline v1.1 tidak ditimpa.

## Catatan pemeriksaan
- PNG maskot pada paket master tema awal terdeteksi memiliki hash identik; validasi visual sebelum dipakai sebagai variasi pose.
- Halaman referensi mengandung konten contoh; jangan anggap sebagai data bisnis produksi.
- Form demo pada referensi perlu integrasi backend/WhatsApp sebelum dipakai produksi.

## Audit aset maskot
Laporan pemeriksaan visual seluruh aset maskot: [MASCOT_ASSET_AUDIT.md](docs/MASCOT_ASSET_AUDIT.md). SVG layak digunakan dengan aturan kontras; seluruh PNG baseline harus diekspor ulang sebelum digunakan.

## Testing
Strategi pemeriksaan baseline dan aset: [docs/TESTING.md](docs/TESTING.md). Folder [tests/](tests/README.md) menjadi tempat skrip validasi versi pengembangan.
