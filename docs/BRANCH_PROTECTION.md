# Perlindungan Branch `main`

Dokumen ini mencatat konfigurasi ruleset **Protect main** yang diverifikasi saat audit terakhir. Ruleset dikelola di GitHub Settings → Rules → Rulesets; periksa kembali UI GitHub jika aturan diubah.

## Konfigurasi ruleset

| Aturan | Nilai terverifikasi |
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

## Kebijakan maintainer tunggal

GitHub tidak mengizinkan penulis PR menyetujui PR miliknya sendiri. Karena repository ini dikelola oleh satu maintainer, required approval dan Code Owner review tetap nonaktif agar PR pemilik repository tidak terkunci.

CODEOWNERS tetap mendokumentasikan kepemilikan area file. Jika reviewer tepercaya kedua bergabung, evaluasi kembali satu approval dan Code Owner review.

## Peran required checks

Ketiga check di atas adalah merge gate. `Project matrix tests` merupakan job agregat stabil yang menunggu pengujian proyek, validasi web, dan pengujian bootstrap Node.js/Python/PHP. Job agregat harus gagal jika salah satu pekerjaan wajib gagal.

CI juga harus menolak proyek nyata yang tidak memiliki manifest stack yang didukung. Sentinel `__no_projects__` hanya digunakan ketika `projects/` benar-benar kosong dan tidak boleh dianggap sebagai proyek aplikasi.

## Cara memeriksa atau mengubah

1. Buka repository → **Settings → Rules → Rulesets**.
2. Pilih **Protect main**.
3. Pastikan enforcement aktif dan target hanya `refs/heads/main`.
4. Pastikan tiga required checks tercantum.
5. Pertahankan bypass actors kosong, strict status checks, dan squash-only sesuai kebijakan.
6. Simpan perubahan dan uji melalui PR.

Perbarui dokumen ini setiap kali konfigurasi GitHub berubah. Nilai di atas adalah snapshot hasil pemeriksaan, bukan sinkronisasi otomatis dari GitHub Settings.
