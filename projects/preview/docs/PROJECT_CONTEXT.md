# Project Context — Preview

## Identitas

- Nama kerja: Landing Page Kampanye Slamet
- Lokasi: `projects/preview/`
- Jenis: static website
- Teknologi: HTML5, CSS3, JavaScript vanilla
- Target publikasi menurut README: GitHub Pages
- Kandidat/periode yang tertulis di materi: SLAMET — calon Kepala Desa Tlagayasa, 2027–2035

## Tujuan

Menyajikan profil, visi, misi, program, potensi desa, dan galeri dalam landing page yang responsif serta interaktif.

## Pengguna dan konteks

Pengunjung publik yang ingin mengenal kandidat dan materi kampanye. Informasi publik harus akurat, mudah dibaca, dan tidak menyesatkan.

## Ruang lingkup saat ini

- Profil kandidat, riwayat pendidikan, dan riwayat pekerjaan
- Kontrol musik latar manual (audio lokal opsional; file berlisensi belum disediakan)
- Tujuh misi interaktif
- Program yang terhubung ke misi
- Potensi desa
- Galeri delapan item
- Navigasi responsif, lightbox, scroll progress, tombol kembali ke atas, serta reduced-motion

## Di luar cakupan / belum dipastikan

- Backend, database, autentikasi, CMS, atau API
- Pengumpulan data pengunjung
- Formulir kontak/dukungan yang mengirim data
- Sumber data resmi dan verifikasi faktual konten
- Status produksi/domain/canonical terkini di luar konfigurasi repository

## Sumber kebenaran

- Struktur dan markup: `index.html`
- Data render: `js/data.js`
- Perilaku: `js/main.js`
- Tampilan: `css/style.css`, `css/improvements.css`, `css/icon-pack.css`
- Aset visual: `assets/`
- Instruksi: `docs/AI_GUIDELINES.md` dan root `/AGENTS.md`

## Data dan konten

README proyek menyebut sejumlah bagian profil sebagai placeholder karena data belum disediakan. Perlakukan data tersebut sebagai belum terverifikasi. Jangan mengubah placeholder menjadi klaim nyata tanpa sumber/konfirmasi pemilik.

## Status audit awal

Repository remote pada commit yang diaudit memiliki CI static-site untuk proyek ini. Audit belum melakukan browser E2E, verifikasi isi ZIP, atau konfirmasi deployment live.
