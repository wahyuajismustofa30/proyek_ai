# Testing — Preview

## Pemeriksaan otomatis

Jalankan validasi referensi ikon dan aset CSS lokal dengan `python3 projects/preview/tests/test_asset_paths.py`. Tes ini menyelesaikan URL mask ikon dari direktori stylesheet dan memastikan file SVG yang dirujuk tersedia.

Jalankan pemeriksaan kontrak fitur profil dan audio dengan `python3 projects/preview/tests/test_profile_audio.py`. Jalankan pemeriksaan identitas kandidat dengan `python3 projects/preview/tests/test_profile_identity.py`. Jalankan simulasi runtime audio (Node.js bawaan, tanpa dependency tambahan) dengan `node projects/preview/tests/test_audio_runtime.js`.

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
- [ ] Refresh memulai state audio baru, mencoba autoplay satu kali, dan memasang fallback gesture kembali tanpa menyimpan state audio ke storage/cookie.
- [ ] Lifecycle saat `play()` tertunda memanggil `pause()` walaupun `audio.paused` masih true; Promise lama tidak dapat mengaktifkan audio kembali.
- [ ] Listener fallback sudah aktif sebelum autoplay dicoba; interaksi pertama (pointerdown/touchstart termasuk awal swipe) tidak terlewat meskipun Promise autoplay belum selesai.
- [ ] Jika fallback gesture ditolak browser, listener dipasang kembali untuk kesempatan interaksi berikutnya; status audio tidak dianggap terinisialisasi sebelum playback berhasil.
- [ ] Volume default audio adalah 0.30 (30%) sebelum playback dimulai.
- [ ] Ikon, aria-label, title, dan status aksesibel berubah sesuai kondisi Play, mute, dan unmute.
- [ ] Setelah musik berhasil dimulai atau tombol musik ditekan, listener fallback dilepas; klik/swipe konten berikutnya tidak mengubah audio.
- [ ] Jika file audio tidak tersedia/gagal dimuat, status kegagalan diumumkan secara aksesibel dan JavaScript halaman tetap berjalan.
- [ ] `NotAllowedError` saat autoplay menampilkan petunjuk fallback; `NotSupportedError`/`NotFoundError` menampilkan masalah sumber/format dan tidak memasang fallback.
- [ ] `AbortError` dan error lain tidak dilaporkan sebagai pembatasan autoplay.
- [ ] Error media (`MEDIA_ERR_ABORTED`, `MEDIA_ERR_NETWORK`, `MEDIA_ERR_DECODE`, `MEDIA_ERR_SRC_NOT_SUPPORTED`) menghasilkan pesan yang sesuai.
- [ ] Pause lifecycle mempertahankan alasan tab/halaman tidak aktif setelah event `pause`; event pause tertunda tidak menimpa playback yang sudah berjalan kembali.
- [ ] Tombol tunggal: saat musik berjalan klik membisukan; saat mute klik mengaktifkan suara; saat berhenti klik memulai ulang. Mute bukan pause.
- [ ] Pause event non-lifecycle dianggap pause manual; fallback tidak boleh menyalakan musik kembali.
- [ ] Tab yang ditinggalkan menghentikan pemutaran tanpa resume saat tab/fokus kembali.
- [ ] Uji autoplay bersuara dan fallback gesture secara manual pada Chrome, Firefox, Safari, dan browser mobile; catat hasil aktual.
- [ ] Semua gambar dan ikon tampil; alt text tersedia.
- [ ] Link internal dan canonical/domain diverifikasi bila deployment berubah.

## Batas bukti

CI dan regression test kontrak tidak dapat membuktikan kebijakan autoplay browser. Autoplay bersuara dapat ditolak oleh kebijakan browser/perangkat; verifikasi fallback dan lifecycle tetap memerlukan pengujian manual pada browser nyata. Browser E2E belum disiapkan/dijalankan.
