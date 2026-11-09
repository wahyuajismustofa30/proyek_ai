# GitHub Sync untuk Termux

Tooling ini berada di `scripts/github-sync-termux.sh` dan berlaku untuk repository
Git apa pun yang memakai remote `origin` serta branch dasar `main`. Jalankan
dari direktori repository yang ingin disinkronkan.

## Instalasi di Termux

Pastikan Git tersedia:

```sh
pkg install git
mkdir -p "$HOME/bin"
```

Dari root clone repository `proyek_ai`, buat shortcut:

```sh
ln -sfn "$PWD/scripts/github-sync-termux.sh" "$HOME/bin/github-sync"
```

Pastikan `$HOME/bin` sudah ada di `PATH`. Jika belum, tambahkan ke
`~/.bashrc`:

```sh
export PATH="$HOME/bin:$PATH"
```

Muat ulang konfigurasi shell:

```sh
source ~/.bashrc
```

Kemudian dari repository mana pun:

```sh
cd ~/git-repos/nama-repository
github-sync
```

## Alur dan pengamanan

1. Memastikan perintah dijalankan di dalam repository Git dengan remote `origin`.
2. Menjalankan `git fetch --prune origin`; tidak mengubah working tree.
3. Jika berada di `main`, mensyaratkan `main` lokal identik dengan
   `origin/main`, lalu membuat branch `feat/termux-sync-YYYYMMDD-HHMMSS`.
   Perubahan unstaged/untracked yang ada tetap dibawa oleh Git saat branch dibuat.
4. Jika berada di branch fitur dan branch tersebut belum memuat `origin/main`,
   tool mengidentifikasi kondisi branch:
   - **Hanya tertinggal:** menawarkan fast-forward dengan
     `git merge --ff-only origin/main`.
   - **Divergen:** menawarkan merge normal dengan
     `git merge --no-edit origin/main`. Ini membuat merge commit dan tidak
     menulis ulang commit fitur.
   - **Ditolak pengguna:** keluar tanpa mengubah branch atau working tree.
5. Jika merge mengalami konflik, tool berhenti dan mempertahankan status konflik
   agar pengguna dapat menyelesaikannya secara manual. Tool tidak menjalankan
   `reset`, `clean`, `stash`, `rebase`, atau `merge --abort` otomatis.
6. Menolak index yang sudah berisi staging pengguna agar staging tersebut tidak
   tercampur atau terhapus.
7. Menampilkan perubahan, melakukan staging setelah konfirmasi, dan meminta
   konfirmasi terpisah sebelum commit dan push.
8. Sebelum push, memastikan remote feature branch tidak memiliki commit yang
   belum ada di lokal. Jika ada, push dihentikan tanpa force-push.
9. Push hanya ke branch fitur. Tool tidak melakukan push ke `main`, force-push,
   reset, clean, stash, rebase, atau menghapus branch.
10. Menampilkan tautan pembuatan Pull Request menuju `main` setelah push berhasil.
    URL hanya dibuat untuk format remote GitHub yang dikenali; URL remote mentah
    tidak ditampilkan.

## Batasan dan catatan

- Periksa daftar file sebelum menyetujui staging. Jangan ikutkan token, password,
  file `.env`, private key, atau data pribadi.
- Pemeriksaan nama file rahasia merupakan lapisan pencegahan sederhana, bukan
  pengganti secret scanner CI.
- Jika `main` lokal tertinggal/berbeda dari `origin/main`, sinkronkan secara
  terpisah dan periksa perubahan terlebih dahulu; tool sengaja tidak melakukan
  reset otomatis.
- Jika merge konflik, selesaikan konflik secara manual, buat commit merge,
  kemudian jalankan kembali `github-sync`.
- Setelah push, buka PR dan tunggu seluruh required checks repository lulus.
  Tool tidak membuat, menyetujui, atau merge PR secara otomatis.

## Pengujian

Dari root repository:

```sh
python -m unittest scripts.tests.test_github_sync_termux -v
bash -n scripts/github-sync-termux.sh
```
