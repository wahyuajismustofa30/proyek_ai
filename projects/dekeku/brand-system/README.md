# DEKEKU Brand System

## Tujuan
Sumber acuan visual bersama untuk proyek website DEKEKU dan undangan online.

## Struktur
- versions/v1.1/source/Dekeku/: file sumber hasil ekstraksi paket v1.1, dipertahankan tanpa modifikasi.
- archives/: arsip ZIP asli.
- docs/: dokumentasi pengembangan brand system berikutnya (tambahkan bila diperlukan).

## Baseline
- Versi baseline repository: v1.1 (label arsip yang ditetapkan pemilik).
- Metadata internal paket masih menyebut v1.5 pada beberapa dokumen. Jangan menyamakan kedua label secara otomatis.
- Gunakan source v1.1 sebagai referensi, bukan tempat eksperimen.
- Untuk pembaruan, buat versions/v1.2 atau folder kerja terpisah setelah requirement disepakati.

## Area penting
- tokens/: design tokens JSON dan CSS.
- assets/logo/: logo horizontal dan compact.
- assets/icon/: ikon brand.
- assets/maskot/: maskot SVG/PNG.
- public/: favicon dan metadata PWA.
- referensi/: halaman referensi tema.
- scripts/: skrip pembangun aset/token.

## Catatan pemeriksaan
- PNG maskot dalam paket awal sebelumnya terdeteksi memiliki isi/hash identik; validasi visual sebelum dipakai sebagai variasi pose.
- Halaman referensi mengandung konten contoh; jangan anggap sebagai data bisnis produksi.
- Form demo pada referensi perlu integrasi backend/WhatsApp sebelum dipakai produksi.
