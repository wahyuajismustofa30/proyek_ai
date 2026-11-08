# Testing — DEKEKU Brand System

## Status
Baseline v1.1 bersifat read-only. Pemeriksaan dilakukan tanpa mengubah source baseline.

## Strategi
- **Static/data:** parse `tokens/tokens.json`, validasi sintaks CSS token, dan periksa konsistensi nama token.
- **Asset integrity:** pastikan file logo, ikon, maskot, favicon, dan referensi yang ditautkan benar-benar tersedia serta formatnya dapat dibaca.
- **Documentation:** validasi tautan internal dan contoh penggunaan token.
- **Visual/manual:** periksa light/dark, kontras, skala logo, keterbacaan, ukuran mobile/desktop, dan konsistensi antarvarian.
- **Regression:** saat versi baru dibuat, bandingkan token dan aset terhadap baseline sebelumnya; jangan mengubah baseline untuk memperbaiki test.

## Perintah saat ini
Dari root repository:
- `python -m json.tool projects/dekeku/brand-system/versions/v1.1/source/Dekeku/tokens/tokens.json`
- `python scripts/check_internal_links.py`
- `python -m compileall -q projects templates scripts`

Pemeriksaan CSS dan visual dilakukan manual sampai pipeline khusus design-token ditambahkan. Jangan menyatakan pemeriksaan visual otomatis telah dilakukan.

## Kriteria penerimaan
- Token JSON valid dan tidak ada referensi token yang tidak dikenal.
- Semua aset yang dipakai tersedia dan formatnya valid.
- Kontras dan keterbacaan telah ditinjau pada konteks light/dark yang didukung.
- Perubahan hanya berada pada versi baru, bukan source baseline.
- Hasil dan pengecualian dicatat di laporan task.
