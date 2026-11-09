# Testing — Preview

## Pemeriksaan otomatis

Jalankan pemeriksaan kontrak fitur profil dan audio dengan `python3 projects/preview/tests/test_profile_audio.py`.

Workflow monorepo mendeteksi proyek sebagai static site melalui `index.html` di root proyek dan menjalankan validasi HTML/CSS/aset lokal serta HTTP smoke test. Pada commit main yang diaudit, check `projects/preview / static` berstatus sukses.

## Cara uji lokal

Dari root repository:

```bash

python scripts/check_static_site.py projects/preview
python scripts/validate_web_projects.py

```

Catatan: gunakan opsi/parameter sesuai `--help` pada script bila berbeda; periksa `docs/MONOREPO_CI.md` untuk cara CI resmi.

Untuk preview browser, jalankan server static dari root proyek (contoh):

```bash

python -m http.server 8000 --directory projects/preview

```

Lalu buka `http://127.0.0.1:8000`.

## Checklist manual

- [ ] Desktop dan viewport mobile: layout, nav, spacing, typography.
- [ ] Hamburger: buka/tutup dan navigasi section.
- [ ] Panel visi: expand/collapse dan state aksesibilitas.
- [ ] Kartu misi: detail benar dan fokus/scroll wajar.
- [ ] Program mengarah ke misi yang tepat.
- [ ] Galeri: buka/tutup, prev/next, keyboard, backdrop.
- [ ] Scroll progress dan back-to-top.
- [ ] `prefers-reduced-motion` mengurangi animasi.
- [ ] Console browser bebas error.
- [ ] Pendidikan menampilkan tiga sekolah sesuai data.
- [ ] Pekerjaan menampilkan empat entri kronologis dan status 2024–Sekarang.
- [ ] Audio tidak autoplay; Play/Pause, mute, dan volume dapat digunakan dengan keyboard.
- [ ] Tanpa file audio, status menjelaskan bahwa audio belum tersedia dan tidak ada error halaman.
- [ ] Tab yang ditinggalkan menghentikan pemutaran tanpa memulai ulang otomatis.
- [ ] Semua gambar dan ikon tampil; alt text tersedia.
- [ ] Link internal dan canonical/domain diverifikasi bila deployment berubah.

## Batas bukti

CI green bukan bukti penuh UX, aksesibilitas, konten faktual, atau kesesuaian lintas-browser. Browser E2E belum disiapkan/dijalankan pada audit awal.
