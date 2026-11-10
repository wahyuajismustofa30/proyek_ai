# Instruksi Induk Repository

Instruksi ini adalah aturan utama untuk seluruh repository `proyek_ai`, termasuk semua direktori di bawah `projects/`. Baca dan terapkan sebelum bekerja. **Jangan meminta pengguna mengulang instruksi ini pada setiap proyek dan jangan menyalin ulang aturan umum ke AGENTS.md proyek.**

## 1. Prioritas dan cakupan instruksi

1. Instruksi sistem/platform dan instruksi keselamatan yang berlaku.
2. File ini (`/AGENTS.md`) sebagai instruksi induk repository.
3. `AGENTS.md` pada direktori target atau direktori induk terdekat sebagai tambahan/pengecualian khusus proyek.
4. README, brief, standar, keputusan, dan dokumentasi proyek sebagai sumber konteks dan kebutuhan.

Instruksi lokal hanya memuat aturan yang benar-benar khusus untuk proyeknya. Jika ada konflik, ikuti instruksi dengan prioritas lebih tinggi; jelaskan konflik yang memengaruhi hasil. Jangan menduplikasi aturan induk.

## 2. Pemeriksaan awal

Sebelum mengubah file:

1. Periksa repository, branch aktif, commit dasar, status perubahan, dan pull request terkait.
2. Baca `README.md`, `docs/PROJECT_INDEX.md`, `docs/STANDARDS.md`, serta dokumentasi workflow/struktur yang relevan.
3. Untuk pekerjaan di `projects/<slug>/`, baca README, brief, arsitektur, daftar tugas, strategi pengujian, keputusan, changelog, dan instruksi lokal yang tersedia sesuai relevansi.
4. Periksa implementasi, dependensi, riwayat, dan konvensi file yang akan disentuh.
5. Jangan mengasumsikan isi file atau hasil pemeriksaan yang belum benar-benar dibaca/dijalankan.

Jika permintaan menyebut proyek tertentu, pastikan slug dan statusnya melalui indeks serta struktur repository. Jangan membuat proyek baru kecuali diminta secara eksplisit.

## 3. Isolasi dan batas perubahan

- Kerjakan hanya proyek dan file yang diperlukan untuk tugas.
- Jangan mencampur source, aset, konfigurasi, atau data antarproyek.
- Jangan mengubah proyek lain, Dependabot, atau konfigurasi root kecuali memang diperlukan untuk memenuhi permintaan.
- Jika perubahan lintas proyek atau menyentuh aturan/konfigurasi global diperlukan, jelaskan alasan, dampak, file yang terdampak, dan alternatif yang lebih sempit; minta persetujuan sebelum melanjutkan.
- Jangan melakukan refactor luas untuk permintaan yang dapat diselesaikan dengan perubahan terfokus.
- Pertahankan kompatibilitas path, nama file, API, format, dan perilaku yang sudah digunakan kecuali perubahan tersebut merupakan tujuan tugas.
- Jangan menghapus atau menimpa arsip, baseline, maupun pekerjaan pengguna yang sudah ada.
- Jangan membuat data fiktif seolah-olah nyata (harga, testimoni, alamat, kontak, statistik, kredensial, atau klaim).
- Pisahkan demo/prototipe dari produksi dan tandai placeholder secara jelas.
- Hindari dependency baru bila kemampuan bawaan atau solusi yang lebih sederhana sudah memadai.
- Jangan menyimpan secret, token, password, private key, credential, data pribadi sensitif, atau file environment berisi rahasia.
- Jangan mengubah deployment atau layanan produksi tanpa instruksi eksplisit.

## 4. Pahami jenis tugas

Tentukan pendekatan sesuai permintaan, tanpa meminta pengguna mengulang konteks repository:

- **AUDIT/REVIEW:** periksa kondisi aktual; laporkan temuan berdasarkan bukti, tingkat dampak, lokasi, dan rekomendasi. Jangan mengubah file kecuali diminta.
- **PLANNING:** susun tahapan, dependensi, risiko, dan kriteria penerimaan; jangan mengimplementasikan.
- **FIX/DEVELOPMENT:** lakukan perubahan terfokus dan tambahkan/perbarui tes regresi yang relevan.
- **TESTING:** jalankan tes yang diminta, diagnosis kegagalan, dan jangan mengubah source kecuali diminta.
- **MAINTENANCE:** lakukan pemeliharaan kecil sesuai ruang lingkup dan standar repository.

Jika tujuan atau batas perubahan tidak jelas dan berpotensi menyebabkan kehilangan data, perubahan lintas proyek, perubahan keamanan, atau dampak produksi, ajukan satu pertanyaan klarifikasi yang paling penting. Untuk ambiguitas kecil, pilih opsi paling aman dan nyatakan asumsi.

## 5. Git dan pull request

- Jangan pernah bekerja langsung pada `main`; gunakan branch khusus dari `main` terbaru.
- Sebelum membuat branch, periksa branch dan PR terbuka agar tidak membuat pekerjaan duplikat.
- Gunakan nama branch deskriptif dan sesuai konvensi repository.
- Jangan menimpa branch, commit, atau perubahan yang sudah ada tanpa pemeriksaan dan alasan yang jelas.
- Jangan force-push, menghapus branch, atau melakukan reset destruktif.
- Buat commit yang fokus; satu commit per unit tugas yang koheren bila memungkinkan.
- Ajukan perubahan melalui pull request ke `main`, dengan judul, ringkasan, alasan, cakupan, pengujian, dan risiko yang akurat.
- Periksa apakah branch tertinggal dari `main`; sinkronkan dengan cara aman dan jalankan ulang pemeriksaan yang terdampak.
- Jangan menyatakan PR siap jika required checks pada commit terbaru belum selesai/lulus.
- Jangan melakukan approval atas nama reviewer atau merge PR kecuali pengguna secara eksplisit memerintahkannya.

## 6. Implementasi, tes, dan dokumentasi

- Buat perubahan sekecil mungkin yang memenuhi kebutuhan dan acceptance criteria.
- Untuk perubahan script atau perilaku, tambahkan/perbarui regression test; bila sesuai, pastikan tes gagal pada kondisi lama dan lulus setelah perbaikan.
- Gunakan fixture sintetis dan terisolasi; jangan memakai kredensial atau data produksi.
- Jalankan tes spesifik proyek dan validasi root/CI yang relevan. Ikuti perintah resmi dalam README dan dokumentasi proyek.
- Periksa diff akhir untuk perubahan tak disengaja, whitespace, file sementara, secret, dependensi, link, dan aset yang hilang.
- Perbarui README, brief, TASKS, CHANGELOG, keputusan, atau dokumentasi lain hanya bila perubahan memengaruhi informasi tersebut.
- Jangan mengurangi assertion, coverage, atau validasi hanya agar CI hijau.
- Jika pemeriksaan tidak dapat dijalankan, jangan mengklaim lulus; sebutkan hambatan dan dampaknya.

## 7. Pelaporan hasil

Berikan laporan ringkas dalam bahasa Indonesia yang memuat:

1. Ringkasan tujuan dan hasil.
2. File yang diubah beserta alasan.
3. Tes/perintah yang benar-benar dijalankan dan hasilnya.
4. Status setiap pemeriksaan: **PASS**, **FAIL**, **BLOCKED**, atau **NOT RUN**.
5. Risiko, asumsi, keterbatasan, dan pekerjaan tersisa.
6. Branch dan tautan PR bila perubahan diajukan.

Bedakan fakta yang diverifikasi dari dugaan atau rekomendasi. Jangan mengklaim commit, push, PR, approval, merge, atau keberhasilan tes sebelum tindakan tersebut benar-benar berhasil.

## 8. Aturan khusus repository

- projects/ adalah ruang kerja source proyek; lihat indeks otomatis di docs/PROJECT_INDEX.md.
- Setiap proyek berada di projects/<slug>/ dengan nama direktori yang valid; struktur internalnya fleksibel dan tidak memerlukan scaffold tertentu.
- Jangan mengasumsikan README, metadata, manifest, source directory, atau tests directory tersedia. Pelajari file yang benar-benar ada. Ikuti docs/PROJECT_STRUCTURE.md, docs/MONOREPO_CI.md, dan docs/TESTING_STANDARDS.md untuk aturan monorepo dan pengujian.
- Arsip historis tidak boleh diubah kecuali pengguna secara eksplisit meminta perubahan arsip.
- Jika dokumentasi berbeda dari kondisi aktual repository, laporkan ketidaksesuaian dan jangan memperluas cakupan untuk memperbaikinya tanpa kebutuhan/persetujuan.
