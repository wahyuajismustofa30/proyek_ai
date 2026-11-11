# Perlindungan Branch `main`

Dokumen ini mencatat konfigurasi ruleset GitHub yang diverifikasi secara langsung
pada **11 November 2026**. Ruleset dapat berubah sewaktu-waktu; periksa kembali
GitHub Settings → Rules → Rulesets sebelum mengandalkan snapshot ini untuk
keputusan operasional.

## Snapshot ruleset aktif

Ruleset **Protect main** (ID `26797557`) berstatus **Active** dan menargetkan
`refs/heads/main`.

| Aturan | Konfigurasi terverifikasi |
|---|---|
| Require a pull request before merging | Aktif |
| Required approvals | 0 |
| Dismiss stale pull request approvals | Aktif |
| Require review from Code Owners | Nonaktif |
| Require approval of the most recent reviewable push | Nonaktif |
| Require extra approval for unattributed Copilot changes | Aktif |
| Require conversation resolution | Aktif |
| Require branches to be up to date | Aktif (strict required status checks) |
| Required status checks | Tiga job pada tabel berikut |
| Require linear history | Aktif |
| Block force pushes / non-fast-forward updates | Aktif |
| Restrict deletions | Aktif |
| Allowed merge method | Squash saja |
| Bypass actors | Tidak ada |

### Required status checks

| Nama check | Workflow |
|---|---|
| `Validate JSON, Python, Markdown, links, and whitespace` | `.github/workflows/validate.yml` |
| `Scan dependencies with OSV-Scanner` | `.github/workflows/dependency-security.yml` |
| `Project matrix tests` | `.github/workflows/project-matrix.yml` |

Ketiga nama tersebut cocok dengan job yang didefinisikan dalam workflow pada
snapshot ini. Ruleset mewajibkan ketiganya dan menerapkan kebijakan strict agar
branch tujuan harus mutakhir terhadap base branch.

## Persetujuan dan kebijakan maintainer

Required approvals bernilai **0**. Karena itu, aturan PR tidak mewajibkan
approval reviewer biasa. Code Owner review dan approval atas push terbaru juga
nonaktif pada snapshot ini.

Pengaturan persetujuan tambahan untuk perubahan Copilot yang tidak teratribusi
tercatat aktif. Jangan menyimpulkan bahwa pengaturan tersebut menggantikan
atau menambah jumlah approval biasa; perilaku akhirnya mengikuti kebijakan
GitHub yang berlaku dan perlu diperiksa kembali bila fitur berubah.

## Cara memeriksa

1. Buka repository → **Settings → Rules → Rulesets**.
2. Pilih **Protect main**.
3. Verifikasi status enforcement, target branch, aturan PR, jumlah approval,
   conversation resolution, required checks, bypass actors, dan metode merge.
4. Cocokkan nama required checks dengan job yang benar-benar dihasilkan workflow.
5. Perbarui tanggal dan isi snapshot ini setelah verifikasi live berikutnya.

Ruleset adalah konfigurasi GitHub yang terpisah dari file repository. Dokumen
ini merupakan catatan manual dan tidak tersinkron otomatis dengan GitHub
Settings.

## Kebijakan validasi yang disederhanakan

Mulai perubahan CI pada November 2026, nama tiga required checks di atas
dipertahankan agar ruleset tidak perlu diubah. Beban pemeriksaan dibedakan
berdasarkan konteks:

- **Pull request:** JSON yang berubah, Markdown yang berubah, kompilasi Python,
  unit test repository, validasi project matrix, pemindaian secret, dependency
  security, dan whitespace.
- **Push ke `main`, jadwal mingguan, atau run manual:** pemeriksaan repository
  lengkap, termasuk seluruh JSON, seluruh Markdown, tautan internal, dan
  validasi HTML/CSS/aset web rekursif.
- **Web validation pada PR:** dilewati sementara karena validator rekursif
  saat ini turut memeriksa direktori referensi/arsip yang bukan target website
  aktif. Pemeriksaan lengkap tetap berjalan pada push ke `main`, jadwal, dan
  run manual. Hasil `skipped` pada job web tidak menggagalkan aggregate
  `Project matrix tests`; discovery dan application tests tetap wajib lulus.

Pemindaian Gitleaks dan OSV-Scanner tetap berjalan pada PR. Kesalahan nyata
pada file yang berubah tetap menggagalkan validasi. Pemeriksaan penuh tetap
tersedia untuk menangkap masalah lintas-file yang tidak tercakup oleh diff PR.
