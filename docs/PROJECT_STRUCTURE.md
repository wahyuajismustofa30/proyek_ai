# Aturan Direktori dan Struktur Proyek

Dokumen ini menetapkan batas minimal monorepo. Struktur internal proyek mengikuti teknologi dan kebutuhan masing-masing.

## Lokasi dan nama

- Proyek dapat berada di projects/<slug>/ atau di dalam folder kategori, misalnya projects/whatsapp/gowa-gemini-bridge/.
- Nama setiap direktori proyek menggunakan lowercase ASCII, angka, dan tanda hubung: [a-z0-9]+(?:-[a-z0-9]+)*.
- Symlink pada path proyek yang didaftarkan ditolak.
- Root projects/ hanya menyimpan direktori dan README.md; file katalog berada di docs/project-catalog.json.
- Folder kategori bukan proyek kecuali secara eksplisit didaftarkan sebagai proyek.

## Struktur internal

Tidak ada scaffold atau struktur folder wajib. README, AGENTS, src/, tests/, docs/, aset, manifest, lockfile, dan konfigurasi AI bersifat opsional.

AI harus memeriksa source, konfigurasi, dan dokumentasi yang benar-benar tersedia. Jangan menganggap file tertentu ada atau membuat dokumentasi tanpa kebutuhan.

## Discovery dan CI

scripts/discover_projects.py saat ini menemukan direktori proyek tingkat pertama. Manifest Node.js, Python, dan PHP mengaktifkan adapter pemeriksaan yang sesuai. Proyek bertingkat yang belum masuk discovery CI tidak boleh dianggap telah diuji oleh matrix CI hanya karena tercantum di indeks.

Status NOTICE berarti pemeriksaan aplikasi tidak tersedia/tidak dikonfigurasi; bukan bukti bahwa tes berhasil. Kesalahan nyata dan tes yang gagal tetap menggagalkan CI.

## Indeks proyek

docs/project-catalog.json adalah sumber kebenaran daftar proyek aktif, tooling, dan kategori. docs/PROJECT_INDEX.md dihasilkan oleh scripts/update_project_index.py; jangan mengedit hasilnya secara manual.

- Tambahkan atau ubah entri katalog ketika status/lokasi proyek berubah.
- README bersifat opsional dan hanya ditautkan jika tersedia.
- Setelah mengubah katalog atau struktur, jalankan python3 scripts/update_project_index.py --write lalu --check.

CI memeriksa kesesuaian indeks dan keberadaan path katalog; CI tidak melakukan commit otomatis.

## Alur sederhana

1. Siapkan source dengan workflow pilihan Anda.
2. Letakkan di direktori proyek yang sesuai.
3. Daftarkan path proyek pada docs/project-catalog.json.
4. Perbarui indeks dan periksa hasil discovery CI secara terpisah.
5. Minta AI mempelajari source serta dokumentasi yang tersedia.
6. Kembangkan sesuai kebijakan repository.
