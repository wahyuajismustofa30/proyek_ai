# Instruksi Pengembangan Termux

Instruksi ini berlaku untuk seluruh kode di `projects/termux/`. Tujuannya adalah memastikan setiap program sesuai dengan lingkungan Termux Android yang benar-benar digunakan, bukan mengasumsikan Linux desktop atau server Linux biasa.

## 1. Sumber kebenaran dan prioritas

- Gunakan implementasi repository, hasil audit Termux terbaru, dan hasil pengujian perangkat sebagai sumber kebenaran.
- Laporan audit bertanggal **2026-11-14 18:14:32 WIB**, versi audit **1.0.1**, adalah baseline perangkat saat itu, bukan nilai permanen atau konfigurasi yang boleh di-hardcode.
- Sebelum mengubah kode, baca instruksi repository, file terkait, dependensi, pemanggil program, dan konfigurasi yang tersedia.
- Periksa perubahan lokal dan pertahankan pekerjaan pengguna. Jangan mengubah file di luar `projects/termux/`.
- Jangan menganggap informasi audit selalu mutakhir. Deteksi kemampuan saat runtime dan sediakan fallback.

## 2. Profil perangkat yang telah terverifikasi

Gunakan informasi ini untuk mengarahkan desain dan pengujian, bukan sebagai asumsi mutlak:

| Komponen | Kondisi saat audit |
|---|---|
| Perangkat | Samsung SM-A055F (Galaxy A05), codename `a05m` |
| Android | 15, SDK 35 |
| ABI / arsitektur | `arm64-v8a` / `aarch64` |
| Kernel | `15` |
| UID | `10082` |
| Hak akses | Tanpa root |
| HOME | `/data/data/com.termux/files/home` |
| PREFIX | `/data/data/com.termux/files/usr` |
| Shell | Bash di dalam PREFIX |
| Python | 3.14.10 |
| CPU | 8 core terdeteksi |
| RAM | Total sekitar 3661.8 MiB; MemAvailable sekitar 971.2 MiB |
| Swap | Total 4096 MiB |
| Paket | 200 paket terdeteksi |
| Shared storage | `~/storage/shared` tersedia pada saat audit |
| Direktori kerja | `~/projects` dan `~/bin` tersedia pada saat audit |

### Tool yang tersedia pada saat audit

- Tersedia: Bash, sh, Python/python3, pip, Git, curl, jq, rsync, SSH, PHP 8.5, Clang, make, ip, ifconfig, lsof, ps, df, du, pkg, apt, dpkg-query, cloudflared, Go, dan gitleaks.
- Tidak terdeteksi di PATH: wget, Node.js/node, npm, proot, termux-battery-status.
- Ketersediaan tool dapat berubah. Selalu periksa dengan `command -v`, `shutil.which()`, atau pemeriksaan setara sebelum digunakan.
- Jangan memasang paket secara otomatis. Jika dependensi wajib belum tersedia, jelaskan paket yang diperlukan dan minta persetujuan sebelum mengubah lingkungan pengguna.

## 3. Batasan Android dan Termux yang wajib diperhatikan

### Hak akses dan filesystem

- Program berjalan sebagai aplikasi Android biasa, bukan root. Jangan mengandalkan akses root, `sudo`, atau kemampuan mengubah konfigurasi sistem Android.
- Akses baca ke `/proc` pernah terdeteksi, tetapi bukan berarti semua file di dalamnya dapat dibaca.
- Akses `/sys` tidak tersedia pada saat audit. Jangan menjadikan `/sys` sebagai dependensi wajib.
- Pembacaan `/proc/net/tcp` dan `/proc/net/tcp6` pernah ditolak oleh permission Android. Jangan mengandalkan tabel tersebut untuk menemukan port atau proses.
- Shared storage tersedia melalui `~/storage/shared`, tetapi izin dapat berubah atau belum diberikan. Periksa keberadaan path dan kemampuan baca/tulis sebelum menggunakannya.
- Gunakan `$HOME`, `$PREFIX`, dan path yang ditemukan saat runtime. Hindari hardcode path instalasi Termux.
- Bedakan storage privat Termux, shared storage Android, dan filesystem sistem Android. Jangan menganggap seluruh output `df` sebagai kapasitas penyimpanan yang dapat digunakan pengguna Termux.

### Jaringan

- Perintah `ip` tersedia, tetapi pengambilan alamat interface dan routing melalui Netlink pernah gagal dengan `Cannot bind netlink socket: Permission denied`.
- Perlakukan informasi interface, routing, dan koneksi sebagai data opsional. Tangani permission error, output kosong, timeout, dan tool yang tidak tersedia tanpa membuat program crash.
- Jangan mengasumsikan akses root, manipulasi interface, firewall sistem, atau konfigurasi jaringan Android.
- Untuk pemeriksaan konektivitas, utamakan uji koneksi aplikasi yang sederhana dan memiliki timeout; jangan menyimpulkan seluruh jaringan mati hanya dari kegagalan Netlink.

### Proses dan port

- Implementasi `ps` Termux tidak selalu menerima format output yang lazim dipakai pada distribusi Linux lain. Audit sebelumnya gagal pada format `PID,PPID,USER,STAT,NAME`.
- Jangan mengasumsikan opsi `ps`, `ss`, `fuser`, atau akses detail proses identik dengan Linux desktop.
- Uji opsi command pada perangkat atau deteksi format yang didukung. Jika gagal, tampilkan status NOTICE dan lanjutkan dengan fitur lain.
- Jangan mengandalkan parsing `/proc/net/*` atau pencocokan deskriptor file untuk mengelola proses.
- Untuk program server yang dibuat oleh aplikasi sendiri, simpan identitas proses yang diluncurkan sendiri (misalnya PID dan metadata proses) secara terpisah. Validasi bahwa PID masih merujuk ke proses yang benar sebelum menghentikannya.
- Hentikan hanya proses yang dimiliki/diluncurkan program tersebut. Jangan membunuh proses berdasarkan nomor port atau nama umum tanpa verifikasi kepemilikan.
- Setiap proses server yang diluncurkan harus dapat dilacak dan dihentikan secara independen tanpa mengganggu server atau proses pengguna lain.

### Resource dan lifecycle Android

- Pertimbangkan RAM terbatas, konsumsi baterai, thermal throttling, dan pembatasan proses latar belakang Android.
- Hindari polling rapat, loop tanpa jeda, proses daemon yang tidak diperlukan, dan pemindaian filesystem besar berulang.
- Berikan timeout untuk operasi eksternal, tangani sinyal/interrupt, dan lakukan cleanup resource yang dimiliki program.
- Jangan menjanjikan layanan latar belakang selalu aktif; Android dapat menghentikan proses aplikasi.

## 4. Aturan implementasi

- Utamakan Python standard library atau utilitas bawaan Termux jika sudah cukup. Hindari dependency berat dan dependency baru tanpa alasan kuat.
- Untuk shell script, gunakan Bash yang tersedia atau POSIX sh bila fitur Bash tidak diperlukan. Tetapkan interpreter secara eksplisit.
- Periksa command sebelum dipanggil. Jangan mengasumsikan `node`, `npm`, `wget`, `proot`, atau Termux:API tersedia.
- Jalankan subprocess dengan argumen berbentuk array/list, bukan menyusun command dari input pengguna melalui shell.
- Validasi input, path, nama file, port, dan konfigurasi. Cegah path traversal, command injection, dan penghapusan di luar direktori target.
- Jangan membaca, menampilkan, menyalin, atau mencatat credential, token, password, API key, private key, maupun riwayat shell.
- Jangan memasukkan alamat IP, identitas perangkat, UID, daftar paket, atau data privat lain ke log/repository kecuali benar-benar diperlukan dan telah disamarkan.
- Operasi yang mengubah atau menghapus data harus menjelaskan target dan dampaknya. Gunakan dry-run dan konfirmasi eksplisit untuk operasi berisiko.
- Jangan melakukan instalasi paket, perubahan permission, perubahan konfigurasi Android, atau operasi root secara otomatis.
- Pertahankan kompatibilitas CLI, environment variable, konfigurasi, format data, lokasi file, dan perilaku program yang sudah digunakan.

## 5. Arsitektur repository dan sinkronisasi ke `~/bin`

- Isi `projects/termux/` merupakan source/mirror untuk direktori `~/bin` di perangkat Termux.
- Arah mirror default adalah **repository `projects/termux/` → `~/bin`**.
- `repo-sync` juga menyediakan sinkronisasi arah sebaliknya (`target` → `source`) untuk pasangan yang dipilih. Arah ini harus disimulasikan terlebih dahulu dan selalu memerlukan konfirmasi eksplisit karena `--delete-delay` dapat menghapus file di direktori source konfigurasi.
- Jangan menjalankan sinkronisasi terbalik secara otomatis atau menganggapnya sebagai sinkronisasi dua arah/merge; operasi tersebut tetap mirror satu arah pada saat dipilih.
- Program yang ditambahkan ke repository harus mempertimbangkan bahwa file akan dijalankan dari `~/bin`, bukan dari direktori clone repository.
- Jangan mengasumsikan current working directory sama dengan lokasi script. Untuk Python, gunakan lokasi file script bila perlu; untuk shell, gunakan path script atau `BASH_SOURCE` secara aman.
- Menu di `~/bin/menu` menemukan program executable secara otomatis.
- Jangan mengubah mekanisme menu, konfigurasi `repo-sync`, atau arah sinkronisasi tanpa kebutuhan yang jelas.
- Perhatikan bahwa mirror `repo-sync` memakai `rsync -a --delete-delay`: file di target yang tidak ada di source dapat terhapus saat sinkronisasi nyata. Jangan mengubah source/target atau menjalankan sinkronisasi destruktif tanpa konfirmasi pengguna.
- Jangan menyimpan konfigurasi privat perangkat di repository. Pisahkan source program dari konfigurasi dan data runtime pengguna.

## 6. Penggunaan hasil audit

Hasil audit Termux adalah petunjuk kemampuan lingkungan, bukan jaminan semua operasi diizinkan.

- `termux-info` pernah timeout; jangan jadikan command ini syarat agar program lain dapat berjalan.
- Battery API tidak tersedia pada saat audit; fitur baterai harus opsional.
- Output `df` menunjukkan banyak mount Android dengan penggunaan 100%. Jangan salah mengartikan partisi image sistem tersebut sebagai disk Termux yang penuh.
- Inventaris paket yang berjumlah 200 adalah snapshot. Jangan mengunci program pada jumlah atau versi paket tersebut.
- Jika data tidak tersedia karena permission atau API, gunakan status yang jelas seperti PASS, NOTICE, FAIL, atau NOT RUN. NOTICE bukan PASS.
- Jangan menyimpulkan kerusakan perangkat hanya karena informasi tertentu kosong atau dibatasi Android.

## 7. Validasi dan pengujian

Setiap perubahan harus divalidasi secara proporsional:

1. Periksa sintaks bahasa dan import/dependensi.
2. Periksa command eksternal yang dipakai benar-benar tersedia atau memiliki fallback.
3. Uji input normal, input kosong/tidak valid, permission ditolak, command tidak tersedia, timeout, dan proses dihentikan.
4. Untuk fitur proses/server, uji start, pemeriksaan status, stop, start ulang, beberapa instance, serta perlindungan agar proses lain tidak ikut dihentikan.
5. Gunakan test otomatis yang sudah ada jika tersedia; jangan menambah framework besar hanya untuk pemeriksaan sederhana.
6. Bedakan pengujian host/simulasi dengan pengujian langsung di perangkat Android/Termux.
7. Jangan menyatakan kompatibel penuh dengan Termux sebelum diuji pada Termux. Laporkan keterbatasan pengujian secara eksplisit.

Gunakan status:
- **PASS** — pemeriksaan dijalankan dan memenuhi kriteria.
- **NOTICE** — command, permission, API, atau lingkungan tidak tersedia/terbatas.
- **FAIL** — ditemukan kesalahan nyata.
- **NOT RUN** — pemeriksaan belum dijalankan.

## 8. Prinsip perubahan

**Termux-first · Android-aware · Runtime-detected · Least-privilege · Lightweight · Data-safe · Backward-compatible · Independently-managed-processes · Evidence-based.**

Pilih implementasi paling sederhana yang bekerja pada kondisi perangkat aktual, memiliki fallback yang aman, dan tidak mengganggu proses maupun data pengguna.
