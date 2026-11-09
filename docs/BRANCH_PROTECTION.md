# Perlindungan Branch `main`

Dokumen ini menyimpan snapshot konfigurasi ruleset **Protect main** yang pernah
dicatat. Nilai di bawah **belum dapat diverifikasi ulang pada audit 2026-11-09**
karena koneksi GitHub yang digunakan tidak memiliki izin untuk membaca endpoint
ruleset/branch protection. Karena itu, jangan menganggap tabel ini sebagai
konfigurasi GitHub yang dipastikan masih aktif. Verifikasi melalui GitHub
Settings → Rules → Rulesets sebelum mengandalkannya sebagai merge gate.

## Snapshot konfigurasi yang tercatat

| Aturan | Nilai dalam snapshot terdahulu |
|---|---|
| Target | `refs/heads/main` |
| Enforcement | Active |
| Require a pull request before merging | Aktif |
| Required approvals | 0 (kebijakan maintainer tunggal) |
| Dismiss stale pull request approvals | Aktif |
| Require review from Code Owners | Nonaktif |
| Require approval of the most recent reviewable push | Nonaktif |
| Require conversation resolution | Aktif |
| Require branches to be up to date | Aktif (strict required status checks) |
| Required status checks | `Validate JSON, Python, Markdown, links, and whitespace`; `Scan dependencies with OSV-Scanner`; `Project matrix tests` |
| Require linear history | Aktif |
| Restrict force pushes | Aktif |
| Restrict deletions | Aktif |
| Allowed merge method | Squash saja |
| Bypass actors | Tidak ada |

## Kebijakan maintainer tunggal (catatan kebijakan)

Catatan sebelumnya menyebut required approval dan Code Owner review nonaktif
karena repository dikelola oleh satu maintainer. Ini merupakan alasan kebijakan
yang tercatat, bukan hasil verifikasi konfigurasi terkini.

## Peran required checks (berdasarkan workflow)

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
3. Verifikasi enforcement, target `refs/heads/main`, aturan PR, required checks,
   bypass actors, dan metode merge.
4. Pastikan required checks merujuk nama job yang benar-benar diproduksi workflow.
5. Perbarui snapshot ini setelah pemeriksaan langsung berhasil, termasuk tanggal
   pemeriksaan dan sumber verifikasinya.

Perbarui dokumen ini setiap kali konfigurasi GitHub berubah. Dokumentasi ini
bukan sinkronisasi otomatis dari GitHub Settings.
