# Brand System Tests

Baseline source berada di `versions/v1.1/source/Dekeku/` dan tidak boleh diubah. Skrip pemeriksaan otomatis disimpan di folder ini dan hanya membaca baseline.

## Validasi aset

Jalankan dari root repository:

`python projects/dekeku/brand-system/tests/validate_assets.py`

Validator memeriksa integritas PNG (signature, chunk, CRC, dan data terkompresi), struktur XML dan `viewBox` SVG, atribut aksesibilitas dasar maskot, kelengkapan 10 varian SVG/PNG, serta duplikasi raster maskot. Tidak membutuhkan dependency pihak ketiga.

PNG maskot baseline v1.1 yang diketahui rusak/identik dicatat sebagai pengecualian historis berbasis SHA-256 dan menghasilkan peringatan, bukan dianggap aset sehat. Jika file tersebut berubah, pengecualian tidak berlaku lagi dan pemeriksaan duplikasi kembali ketat. Simpan perbaikan pada versi aset baru, bukan dengan mengubah baseline.

CI root menjalankan validator ini secara otomatis. Pemeriksaan visual (kontras, komposisi, keterbacaan dan tampilan lintas ukuran) tetap merupakan review manual.