# Perlindungan Branch `main`

Dokumen ini memisahkan **snapshot ruleset yang pernah diverifikasi** dari
status konfigurasi GitHub saat ini. Pada audit lanjutan 2026-11-09, koneksi
GitHub yang tersedia tidak mengizinkan pembacaan endpoint ruleset/branch
protection. Karena itu, nilai berikut adalah rekaman historis, bukan jaminan
bahwa konfigurasi masih aktif.

Snapshot paling lengkap tercatat pada perubahan dokumentasi di PR #55
(branch `docs/factual-dependabot-branch-protection`, commit
`4f8f18d7b32d9b0aa3e9f2184259c9f8de7d6050`). PR #55 ditutup tanpa merge.
Jangan memperlakukan snapshot itu sebagai konfigurasi live tanpa pemeriksaan
ulang melalui GitHub Settings → Rules → Rulesets.

## Snapshot ruleset Protect main yang pernah diverifikasi

| Aturan | Nilai pada snapshot terdahulu |
|---|---|
| Target | `refs/heads/main` |
| Enforcement | Active |
| Require a pull request before merging | Aktif |
| Required approvals | 0 |
| Dismiss stale pull request approvals | Aktif |
| Require review from Code Owners | Nonaktif |
| Require approval of the most recent reviewable push | Nonaktif |
| Require extra approval for unattributed Copilot pull requests | Aktif (`require_extra_approval_for_unattributed_changes: true`) |
| Require conversation resolution | Aktif |
| Require branches to be up to date | Aktif (strict required status checks) |
| Required status checks | `Validate JSON, Python, Markdown, links, and whitespace`; `Scan dependencies with OSV-Scanner`; `Project matrix tests` |
| Require linear history | Aktif |
| Block force pushes / non-fast-forward updates | Aktif |
| Restrict deletions | Aktif |
| Allowed merge method | Squash saja |
| Bypass actors | Tidak ada |

## Dampak pengaturan Copilot

Snapshot terdahulu mencatat `require_extra_approval_for_unattributed_changes`
aktif. Pengaturan ini meminta persetujuan tambahan untuk pull request Copilot
yang tidak teratribusi ke kolaborator manusia. Namun, snapshot tersebut juga
mencatat required approvals = 0. Menurut catatan pemeriksaan sebelumnya,
pengaturan persetujuan tambahan tidak menambah persyaratan approval ketika
jumlah approval yang diwajibkan adalah nol. Verifikasi kembali perilaku dan
ketersediaan fitur ini pada GitHub karena status preview dan kebijakannya dapat
berubah.

## Kebijakan maintainer tunggal

Catatan kebijakan sebelumnya menyebut required approval dan Code Owner review
nonaktif karena repository dikelola oleh satu maintainer. Ini adalah alasan
kebijakan yang tercatat, bukan bukti kondisi konfigurasi terkini.

## Required checks dan workflow

Workflow root saat ini mendefinisikan job bernama:

- `Validate JSON, Python, Markdown, links, and whitespace` di
  `.github/workflows/validate.yml`;
- `Scan dependencies with OSV-Scanner` di
  `.github/workflows/dependency-security.yml`;
- `Project matrix tests` sebagai job agregat di
  `.github/workflows/project-matrix.yml`.

Keberadaan job dalam source workflow tidak membuktikan bahwa job tersebut
terdaftar sebagai required status checks pada ruleset GitHub. Pastikan
kecocokan nama dan status required melalui Settings → Rules → Rulesets.

## Cara memeriksa atau mengubah

1. Buka repository → **Settings → Rules → Rulesets**.
2. Pilih **Protect main** jika ruleset tersebut masih ada.
3. Verifikasi enforcement, target `refs/heads/main`, aturan PR, approval,
   pengaturan Copilot, required checks, bypass actors, dan metode merge.
4. Pastikan required checks merujuk nama job yang benar-benar diproduksi workflow.
5. Catat tanggal pemeriksaan dan sumber verifikasi setelah pembacaan live berhasil.

Perbarui dokumen ini setiap kali konfigurasi GitHub berubah. Dokumen ini adalah
snapshot manual, bukan sinkronisasi otomatis dari GitHub Settings.
