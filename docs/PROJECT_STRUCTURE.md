# Aturan Direktori dan Struktur Proyek

Dokumen ini menetapkan batas minimal monorepo. Struktur internal proyek mengikuti teknologi dan kebutuhan masing-masing.

## Lokasi dan nama

- Setiap proyek berada langsung di `projects/<slug>/`.
- Nama direktori menggunakan lowercase ASCII, angka, dan tanda hubung: `[a-z0-9]+(?:-[a-z0-9]+)*`.
- Contoh: `website`, `web-app`, `api-v2`, `dekeku`.
- Symlink langsung di dalam `projects/` ditolak.
- Hanya `projects/README.md` yang boleh berupa file langsung di root `projects/`.

## Struktur internal

Tidak ada scaffold atau struktur folder wajib. README, AGENTS, `src/`, `tests/`, `docs/`, aset, manifest, lockfile, dan konfigurasi AI bersifat opsional.

AI harus memeriksa source, konfigurasi, dan dokumentasi yang benar-benar tersedia. Jangan menganggap file tertentu ada atau membuat dokumentasi tanpa kebutuhan.

## Discovery dan CI

`scripts/discover_projects.py` menemukan direktori proyek tingkat pertama. Manifest Node.js, Python, dan PHP mengaktifkan adapter pemeriksaan yang sesuai. Proyek tanpa adapter tetap ditemukan dan tidak diblokir hanya karena teknologinya belum didukung.

- Node.js: jalankan script `lint`, `test`, dan `build` yang tersedia. Lockfile digunakan jika ada; ketiadaannya menghasilkan NOTICE bila instalasi diperlukan.
- Python: tes dijalankan jika file tes Python ditemukan. Tanpa tes, CI memberikan NOTICE.
- PHP: validasi Composer dijalankan; script `test` dijalankan jika dikonfigurasi.
- Website statis: file HTML di root dikenali sebagai entrypoint. `index.html` dipilih lebih dahulu; jika tidak ada, CI memakai nama file HTML pertama secara alfabetis.

Status NOTICE berarti pemeriksaan aplikasi tidak tersedia/tidak dikonfigurasi; bukan bukti bahwa tes berhasil. Kesalahan nyata dan tes yang gagal tetap menggagalkan CI.

Validasi HTML, CSS, referensi aset lokal, secret, dan dependency tetap dijalankan sesuai cakupan workflow repository.

## Indeks proyek

`docs/PROJECT_INDEX.md` dihasilkan oleh `scripts/update_project_index.py`; jangan mengedit tabelnya secara manual.

- GitHub Sync Termux memperbarui indeks ketika `projects/` berubah.
- Untuk upload atau pengembangan melalui jalur lain, jalankan `python3 scripts/update_project_index.py --write`.
- CI menjalankan `--check` dan memberi tahu jika indeks belum diperbarui.

## Alur sederhana

1. Siapkan source dengan workflow pilihan Anda.
2. Letakkan di `projects/<slug>/`.
3. Periksa indeks dan hasil discovery.
4. Minta AI mempelajari source serta dokumentasi yang tersedia.
5. Kembangkan pada branch terpisah dan ajukan PR.
