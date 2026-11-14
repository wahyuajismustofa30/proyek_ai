# Webport Termux

## Ringkasan

Webport menjalankan proyek PHP atau HTML sebagai server terpisah. Setiap server memiliki proses supervisor sendiri sehingga dapat tetap berjalan ketika menu Webport ditutup dan dapat dihentikan secara mandiri.

## Menentukan port proyek

Webport membaca konfigurasi berdasarkan urutan prioritas:

1. File `PORT` di dalam folder proyek (disarankan).
2. File `.webport` lama untuk kompatibilitas.

Isi file dapat berupa angka port, misalnya `8080`, atau `PORT=8080`. Jika keduanya tersedia, `PORT` yang digunakan. Jika belum ada, Webport meminta port dan menyimpan pilihan ke file `PORT`.

Deteksi server mempertahankan prioritas `index.php` lalu `index.html`. Jika keduanya tidak ada di root, Webport mencari file PHP, HTML, atau HTM di subfolder, dengan mengabaikan `.git`, `node_modules`, dan `__pycache__`.

## Proses dan metadata

Data runtime disimpan di direktori privat Termux:

- `$HOME/.webport/servers/<PORT>.json`: metadata server, PID supervisor, token identitas acak, PID server, status, dan informasi proyek.
- `$HOME/.webport/<PORT>.log`: output server.

Metadata ditulis secara atomik agar tidak mudah tertinggal dalam keadaan setengah tertulis. Supervisor diluncurkan dalam sesi proses terpisah dan mengelola proses server sebagai child process.

Untuk memverifikasi kepemilikan PID, Webport mencocokkan PID dan token acak pada argumen proses melalui `/proc/<PID>/cmdline`. Webport tidak memindai `/proc/net/tcp*`, tidak mengandalkan `ss`, `fuser`, atau `lsof`, dan tidak menghentikan proses berdasarkan nomor port atau nama proses umum.

Jika Android/Termux membatasi pembacaan `/proc/<PID>/cmdline`, identitas dianggap tidak dapat diverifikasi. Webport akan menolak mengirim sinyal, bukan mengambil risiko menghentikan proses lain.

## Start, status, dan stop

- **Start:** Webport memeriksa port dengan percobaan bind, meluncurkan supervisor, lalu menunggu proses server hidup dan koneksi lokal berhasil sebelum melaporkan server aktif.
- **Status:** daftar hanya mencakup server yang dikelola Webport dan metadata lama yang dapat dikenali. Ini bukan daftar semua listener pada perangkat.
- **Stop:** Webport memvalidasi token proses, mengirim SIGTERM, dan memberi waktu kepada supervisor untuk menghentikan child server. SIGKILL hanya menjadi langkah terakhir dan dibatasi pada process group khusus milik server tersebut.
- Metadata server yang berhenti dipertahankan sebagai riwayat; metadata rusak tidak dihapus otomatis.

## Kompatibilitas metadata lama

Versi sebelumnya menyimpan file `<PORT>.pid`, `<PORT>.engine`, dan `<PORT>.path` langsung di `$HOME/.webport`. Data tersebut tetap ditampilkan sebagai metadata legacy, tetapi tidak dianggap bukti kepemilikan proses karena tidak memiliki token identitas. Webport versi ini tidak akan menghentikan proses legacy secara otomatis. Periksa dan hentikan server lama secara manual dengan cara yang sesuai sebelum menghapus metadata lamanya.

## Batasan Android

Android dapat membatasi akses informasi proses dan dapat menghentikan aplikasi di latar belakang. Jika identitas proses tidak dapat diverifikasi, fungsi stop akan gagal dengan aman. Keberlangsungan server di latar belakang tetap bergantung pada kebijakan lifecycle dan pengelolaan baterai Android.
