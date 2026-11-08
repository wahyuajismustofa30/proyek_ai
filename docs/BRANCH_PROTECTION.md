# Perlindungan Branch \`main\`

Dokumen ini mencatat konfigurasi yang direkomendasikan untuk ruleset **Protect main**.
Ruleset dikelola di GitHub Settings dan harus diperbarui di sana.

## Konfigurasi yang direkomendasikan

| Aturan | Nilai |
|---|---|
| Require a pull request before merging | Aktif |
| Required approvals | 1 |
| Dismiss stale pull request approvals | Aktif |
| Require review from Code Owners | Aktif |
| Require conversation resolution | Aktif |
| Require branches to be up to date | Aktif |
| Required checks | Validate repository; Scan dependencies with OSV-Scanner |
| Require linear history | Aktif |
| Restrict force pushes | Aktif |
| Restrict deletions | Aktif |
| Allowed merge method | Squash saja |
| Bypass actors | Tidak ada |

## Catatan untuk repository dengan satu maintainer

GitHub tidak mengizinkan penulis PR menyetujui PR miliknya sendiri. Jika hanya ada satu maintainer,
aturan satu approval dan Code Owner approval dapat membuat PR tidak bisa di-merge.

Sebelum mengaktifkan kedua persyaratan approval, tambahkan setidaknya satu reviewer tepercaya
yang berbeda dari penulis PR. Jika belum tersedia, jangan aktifkan aturan yang mengunci semua
merge; gunakan required checks dan review manual sampai reviewer kedua ditambahkan.

## Cara menerapkan

1. Buka repository → **Settings → Rules → Rulesets**.
2. Pilih **Protect main**.
3. Atur approval, stale review dismissal, Code Owner review, dan strict status checks sesuai tabel.
4. Simpan perubahan.
5. Pastikan enforcement tetap **Active**.
6. Uji dengan PR percobaan dan pastikan CI wajib lulus sebelum merge.

