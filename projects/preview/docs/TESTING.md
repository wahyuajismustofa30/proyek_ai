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
- [ ] Scroll progress dan sticky header tetap berfungsi tanpa tombol Back to Top.
- [ ] `prefers-reduced-motion` mengurangi animasi.
- [ ] Console browser bebas error.
- [ ] Pendidikan menampilkan tiga sekolah sesuai data.
- [ ] Pekerjaan menampilkan empat entri kronologis dan status 2024–Sekarang.
- [ ] Hanya ada satu tombol musik mengambang di kanan bawah dan dapat dioperasikan dengan Tab, Enter, dan Space.
- [ ] Klik pertama memulai musik; saat berjalan klik membisukan; klik berikutnya mengaktifkan suara tanpa mengulang dari awal.
- [ ] Ikon, aria-label, title, dan status aksesibel berubah sesuai kondisi Play, mute, dan unmute.
- [ ] Audio tidak autoplay dan volume awal tetap 18%; tidak ada kontrol volume atau tombol mute terpisah.
- [ ] Jika file audio tidak tersedia/gagal dimuat, status kegagalan diumumkan secara aksesibel dan JavaScript halaman tetap berjalan.
- [ ] Tab yang ditinggalkan menghentikan pemutaran tanpa memulai ulang otomatis.
- [ ] Semua gambar dan ikon tampil; alt text tersedia.
- [ ] Link internal dan canonical/domain diverifikasi bila deployment berubah.

## Batas bukti

CI green bukan bukti penuh UX, aksesibilitas, konten faktual, atau kesesuaian lintas-browser. Browser E2E belum disiapkan/dijalankan pada audit awal.
