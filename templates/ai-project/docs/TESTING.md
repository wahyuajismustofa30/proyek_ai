# Strategi Testing — [NAMA PROYEK]

> Salin dan sesuaikan dokumen ini untuk setiap proyek. Hapus instruksi dalam tanda kurung setelah diisi.

## Tujuan dan risiko
- Jenis proyek: [website / aplikasi / API / CLI / design system / dokumentasi]
- Alur/fitur paling kritis: [isi]
- Risiko utama jika gagal: [isi]
- Data yang digunakan saat test: [dummy / fixture / factory; jelaskan]

## Lingkup testing
| Lapisan | Digunakan? | Tool / lokasi | Alasan atau cakupan |
|---|---|---|---|
| Static / lint | [Ya/Tidak] | [isi] | [isi] |
| Unit | [Ya/Tidak] | [isi] | [isi] |
| Integration | [Ya/Tidak] | [isi] | [isi] |
| Contract / API | [Ya/Tidak] | [isi] | [isi] |
| E2E | [Ya/Tidak] | [isi] | [isi] |
| Visual / accessibility | [Ya/Tidak] | [isi] | [isi] |
| Security | [Ya/Tidak] | [isi] | [isi] |
| Manual acceptance | Ya | [checklist / lokasi] | [isi] |

## Prasyarat dan environment
- Runtime dan versi: [isi]
- Instalasi dependency: [isi]
- Environment test: [isi]
- Database/service test: [isi atau N/A]
- Variabel environment: gunakan nilai dummy dari `.env.example`; jangan gunakan secret produksi.

## Perintah standar
| Tujuan | Perintah |
|---|---|
| Install dependency | [isi] |
| Lint / static check | [isi] |
| Unit + integration test | [isi] |
| E2E | [isi atau N/A] |
| Build | [isi atau N/A] |

## Skenario kritis
| ID | Skenario | Hasil yang diharapkan | Otomatis / Manual |
|---|---|---|---|
| T-001 | [alur sukses utama] | [hasil] | [jenis] |
| T-002 | [input tidak valid / kegagalan] | [hasil] | [jenis] |
| T-003 | [akses tanpa izin / batas] | [hasil] | [jenis] |

## Aturan data dan keamanan
- [ ] Seluruh data test sintetis dan bukan data pengguna/produksi.
- [ ] Test tidak menghubungi atau mengubah layanan produksi.
- [ ] Credential hanya dummy dan tidak disimpan di repository.
- [ ] Resource sementara dibersihkan setelah test.
- [ ] Kasus akses ditolak dan input tidak valid ikut diuji.

## CI
- Workflow: [path]
- Trigger: [pull request / push / schedule]
- Required checks: [isi]
- Cara membaca hasil: [isi]

## Hasil verifikasi terakhir
| Tanggal | Commit | Perintah / skenario | Status | Catatan |
|---|---|---|---|---|
| [YYYY-MM-DD] | [SHA] | [isi] | [PASS/FAIL/BLOCKED/NOT RUN] | [isi] |

## Pengecualian
Tuliskan lapisan yang tidak digunakan beserta alasan dan pemeriksaan penggantinya. Jangan hanya menandai N/A tanpa penjelasan.
