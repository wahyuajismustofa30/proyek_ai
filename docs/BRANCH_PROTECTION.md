# Perlindungan Branch `main`

Dokumen ini mencatat konfigurasi aktual dan rekomendasi untuk ruleset **Protect main**.
Ruleset dikelola di GitHub Settings → Rules → Rulesets.

## Konfigurasi untuk maintainer tunggal

| Aturan | Nilai |
|---|---|
| Target | `refs/heads/main` |
| Enforcement | Active |
| Require a pull request before merging | Aktif |
| Required approvals | 0 |
| Dismiss stale pull request approvals | Aktif |
| Require review from Code Owners | Nonaktif |
| Require approval of the most recent reviewable push | Nonaktif |
| Require conversation resolution | Aktif |
| Require branches to be up to date | Aktif (strict required status checks) |
| Required checks saat audit | Validate JSON, Python, Markdown, links, and whitespace; Scan dependencies with OSV-Scanner |
| Required check tambahan untuk monorepo | **Project matrix tests** — perlu ditambahkan setelah check muncul pada PR |
| Require linear history | Aktif |
| Restrict force pushes | Aktif (non-fast-forward ditolak) |
| Restrict deletions | Aktif |
| Allowed merge method | Squash saja |
| Bypass actors | Tidak ada |

## Mengapa approval wajib dinonaktifkan

GitHub tidak mengizinkan penulis PR menyetujui PR miliknya sendiri. Karena repository ini dikelola oleh satu maintainer, mewajibkan approval atau Code Owner review akan mengunci merge PR yang dibuat oleh maintainer tersebut.

CODEOWNERS tetap digunakan untuk mendokumentasikan kepemilikan area file. Jika kelak ada reviewer tepercaya kedua, pertimbangkan mengaktifkan kembali satu approval dan Code Owner review setelah memastikan reviewer tersebut dapat memenuhi kebijakan.

## Menambahkan gate CI monorepo

Workflow root `.github/workflows/project-matrix.yml` memiliki job agregat dengan nama stabil
**Project matrix tests**. Job ini gagal jika discovery atau salah satu test stack gagal,
sehingga branch protection tidak perlu bergantung pada nama job matrix yang berubah-ubah
sesuai jumlah proyek.

Setelah check tersebut muncul pada PR:

1. Buka repository → **Settings → Rules → Rulesets**.
2. Pilih **Protect main**.
3. Pada **Require status checks to pass**, tambahkan **Project matrix tests**.
4. Pertahankan dua check yang sudah diwajibkan.
5. Simpan perubahan dan pastikan ketiga check menjadi required.

Koneksi GitHub yang digunakan untuk perubahan repository ini hanya menyediakan pembacaan
ruleset, bukan pengubahan aturan administrasi. Karena itu, penambahan required check
tersebut harus dilakukan melalui Settings oleh pemilik repository. Sampai langkah ini
dilakukan, Project matrix tests tetap berjalan pada PR tetapi belum menjadi merge gate.

## Cara memeriksa atau mengubah

1. Buka repository → **Settings → Rules → Rulesets**.
2. Pilih **Protect main**.
3. Sesuaikan pengaturan dengan tabel di atas.
4. Pastikan enforcement tetap **Active**, bypass actors kosong, dan semua required checks dipilih.
5. Simpan perubahan.
6. Uji melalui PR dan pastikan CI wajib lulus sebelum merge.

Perbarui dokumen ini setiap kali ruleset berubah agar kebijakan tertulis tetap sesuai dengan konfigurasi GitHub yang aktif.
