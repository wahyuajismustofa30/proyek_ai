# Archives

Folder ini menyimpan paket asli atau snapshot historis yang dipertahankan untuk audit, referensi, dan pemulihan.

## Aturan
- Arsip bersifat immutable; jangan mengedit, menimpa, atau mengganti nama file sumber.
- Perubahan dilakukan pada salinan kerja atau versi pengembangan baru, bukan pada arsip.
- Catat nama file, versi/status yang ditetapkan, asal, tujuan penggunaan, dan catatan perbedaan metadata pada dokumentasi terkait.
- Jika aset arsip digunakan dalam proyek, dokumentasikan jalur sumber arsip dan aturan penggunaannya.

## DEKEKU

| Arsip | Status dan fungsi | Dokumentasi |
|---|---|---|
| `Master-tema-dekeku-v1.1.zip` | Paket master tema asli; ditetapkan sebagai baseline v1.1 dan dipertahankan tanpa modifikasi. Metadata internal paket memiliki beberapa label v1.5; jangan menyamakan label tersebut secara otomatis. | [Brand System README](dekeku-brand-system-v1.1/README.md) |
| `dekeku-logo-package.zip` | Paket logo resmi yang diberikan pemilik DEKEKU. Menjadi sumber arsip resmi untuk logo, maskot, ikon/favicon, aset media sosial, dan panduan identitas. | [Panduan Paket Logo Resmi](dekeku-brand-system-v1.1/docs/OFFICIAL_LOGO_PACKAGE.md) |
| `dekeku-brand-system-v1.1/` | Salinan hasil ekstraksi baseline v1.1 untuk referensi dan audit. Dipindahkan dari ruang kerja proyek; perlakukan seluruh isinya sebagai read-only. | [Brand System README](dekeku-brand-system-v1.1/README.md) |

### Aturan khusus paket logo
- File sumber: `archives/dekeku-logo-package.zip`.
- Jangan mengubah isi ZIP sumber. Jika diperlukan file siap pakai, ekstrak atau salin aset ke direktori aset aktif proyek dan catat asalnya.
- Panduan penggunaan dan inventaris paket berada di direktori Brand System arsip; panduan tersebut tidak menggantikan file biner sumber.
- SVG di dalam paket merupakan pembungkus SVG dengan PNG tertanam, bukan artwork vektor berbasis path. Pertimbangkan keterbatasan ini untuk kebutuhan cetak atau pengubahan bentuk.
- Jangan menganggap aset logo dalam arsip master tema v1.1 sebagai pengganti paket logo resmi yang lebih baru.
