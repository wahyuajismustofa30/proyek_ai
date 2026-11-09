# Changelog

## [Unreleased]

### Fixed

- Memindahkan SVG ke bawah document root agar URL aset tidak menghasilkan 404 saat server dijalankan dari `src/`.
- Memastikan navigasi mobile tetap tersedia saat JavaScript tidak aktif.
- Memperketat validasi format email.
- Mencegah form melakukan native submit jika JavaScript tidak tersedia; tombol submit diaktifkan setelah handler siap.

### Added

- Regression test untuk resolusi aset berbasis URL HTTP.
- Test perilaku menu dan formulir menggunakan DOM stub tanpa dependency eksternal.
- Test memastikan handler form membatalkan submit browser default.

## [0.1.0] — 2026-11-09

### Added

- Inisialisasi proyek dari template standar repository.
- Landing page demo responsif dan simulasi form lokal.
