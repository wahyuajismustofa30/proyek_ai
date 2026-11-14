# Perlindungan Branch `main`

Dokumen ini mencatat ruleset GitHub yang diverifikasi pada **11 November 2026**.
Konfigurasi GitHub dapat berubah tanpa perubahan pada repository; periksa kembali
GitHub Settings → Rules → Rulesets sebelum mengambil keputusan operasional.

## Ruleset aktif

Ruleset **Protect main** (ID `26797557`) berstatus **Active** dan menargetkan
`refs/heads/main`.

| Aturan | Status terverifikasi |
|---|---|
| Restrict deletions | Aktif |
| Block non-fast-forward updates | Aktif |
| Require linear history | Aktif |
| Require a pull request before merging | Tidak dikonfigurasi pada ruleset ini |
| Required status checks | Tidak dikonfigurasi pada ruleset ini |
| Required approvals | Tidak dikonfigurasi pada ruleset ini |

Ruleset tersebut tidak menetapkan kewajiban Pull Request, approval reviewer,
atau required status checks. Dengan demikian, alur kerja repository saat ini
mengizinkan commit langsung ke `main` selama pembaruan memenuhi aturan aktif
dan dilakukan tanpa force-push.

Endpoint branch protection klasik yang tersedia melaporkan branch `main`
sebagai protected, tetapi tidak menyediakan aturan required status checks
aktif. Dokumen ini merujuk pada aturan yang dapat diverifikasi secara langsung
dari ruleset **Protect main**; jangan menyimpulkan pengaturan lain yang tidak
terbaca dari endpoint tersebut.

## Kebijakan kerja

- Gunakan `main` sebagai branch kerja dan tujuan commit/push default.
- Commit langsung ke `main` diperbolehkan; feature branch dan Pull Request
  tidak diwajibkan kecuali pengguna secara eksplisit memintanya.
- Approval Pull Request bukan syarat untuk commit langsung ke `main`.
- Jangan force-push, menulis ulang riwayat, atau menghapus branch `main`.
- Pertahankan linear history dan gunakan pembaruan fast-forward.
- Jangan mengubah ruleset atau pengaturan keamanan GitHub tanpa persetujuan.

## CI dan required status checks

GitHub Actions berjalan pada push ke `main`. Workflow juga dapat berjalan
pada Pull Request ke `main`, jadwal mingguan, atau pemicu manual sesuai
konfigurasi masing-masing workflow.

CI tetap berfungsi sebagai pemeriksaan kualitas setelah push. Namun, hasil CI
tidak dikonfigurasi sebagai **required status checks** pada ruleset aktif
`Protect main`. Artinya, ruleset tersebut tidak menahan commit langsung
sampai seluruh workflow selesai.

Nama job yang ada di workflow saat snapshot ini:

| Nama job | Workflow |
|---|---|
| `Validate JSON, Python, Markdown, links, and whitespace` | `.github/workflows/validate.yml` |
| `Scan dependencies with OSV-Scanner` | `.github/workflows/dependency-security.yml` |
| `Project matrix tests` | `.github/workflows/project-matrix.yml` |

Nama-nama tersebut adalah job CI, bukan daftar required status checks.

## Cara memeriksa ulang

1. Buka repository → **Settings → Rules → Rulesets**.
2. Pilih **Protect main**.
3. Pastikan ruleset berstatus Active dan target mencakup `refs/heads/main`.
4. Periksa aturan deletion, non-fast-forward, dan linear history.
5. Periksa apakah ada aturan baru terkait Pull Request atau required status
   checks.
6. Cocokkan pemicu dan job CI dengan file workflow di `.github/workflows/`.

Ruleset adalah konfigurasi GitHub yang terpisah dari file repository.
Dokumen ini merupakan snapshot manual, bukan sinkronisasi otomatis dengan
GitHub Settings.
