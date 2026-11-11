#!/usr/bin/env bash
# Direct-to-main GitHub sync helper for Termux.
set -Eeuo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RESET='\033[0m'
info(){ printf '%b\n' "$*"; }
fail(){ info "${RED}ERROR:${RESET} $*" >&2; exit 1; }
confirm(){
  local answer
  read -r -p "$1 [y/N] " answer || return 1
  [[ "$answer" =~ ^([yY]|[yY][eE][sS])$ ]]
}
git_cmd(){ git -C "$REPO" "$@"; }

command -v git >/dev/null 2>&1 || fail "Git belum terpasang. Jalankan: pkg install git"
REPO="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "Jalankan github-sync dari dalam repository Git."
REMOTE=origin
git_cmd remote get-url "$REMOTE" >/dev/null 2>&1 || fail "Remote 'origin' tidak ditemukan."
BRANCH="$(git_cmd branch --show-current)"
[[ "$BRANCH" == "main" ]] || fail "Branch aktif adalah '$BRANCH'. Pindah ke main secara manual; tool tidak membuat atau mengganti branch."

info "${GREEN}DEKEKU — GITHUB SYNC (DIRECT COMMIT TO MAIN)${RESET}"
info "Repository : $REPO"
info "Branch     : main"
info "Remote     : origin (URL disembunyikan untuk menghindari kebocoran credential)"
info ""

git_cmd fetch origin || fail "Fetch gagal. Periksa koneksi dan autentikasi GitHub."
git_cmd show-ref --verify --quiet refs/remotes/origin/main || fail "origin/main tidak ditemukan."
REMOTE_MAIN="$(git_cmd rev-parse refs/remotes/origin/main)"
LOCAL_HEAD="$(git_cmd rev-parse HEAD)"

if [[ "$LOCAL_HEAD" != "$REMOTE_MAIN" ]]; then
  if git_cmd merge-base --is-ancestor "$LOCAL_HEAD" "$REMOTE_MAIN"; then
    [[ -z "$(git_cmd status --porcelain)" ]] || fail "main lokal tertinggal dari origin/main sementara working tree memiliki perubahan. Perubahan dipertahankan; sinkronkan setelah meninjau perubahan lokal."
    git_cmd merge --ff-only origin/main || fail "Fast-forward gagal. Periksa status Git; tidak ada reset atau force-push."
    info "${GREEN}main diperbarui dengan fast-forward.${RESET}"
  elif git_cmd merge-base --is-ancestor "$REMOTE_MAIN" "$LOCAL_HEAD"; then
    info "main lokal memiliki commit yang belum dikirim ke origin."
  else
    fail "main lokal dan origin/main divergen. Tinjau riwayat dan selesaikan secara manual; tool tidak melakukan merge/rebase/reset otomatis."
  fi
fi

# Regenerate the project index whenever project source changes.
if [[ -n "$(git_cmd status --porcelain -- projects/)" ]]; then
  if ! git_cmd diff --quiet -- docs/PROJECT_INDEX.md; then
    fail "docs/PROJECT_INDEX.md memiliki perubahan lokal. Tinjau perubahan tersebut sebelum regenerasi otomatis."
  fi
  command -v python3 >/dev/null 2>&1 || fail "Python 3 diperlukan untuk memperbarui docs/PROJECT_INDEX.md ketika projects/ berubah."
  python3 "$REPO/scripts/update_project_index.py" --write || fail "Pembaruan indeks proyek gagal."
  info "Indeks proyek diperbarui otomatis."
fi

if git_cmd status --porcelain | grep -Eiq '(^|[[:space:]])([^[:space:]]*/)?(\.env(\.[^/]*)?|id_rsa|id_ed25519|credentials(\.json)?|secrets?)(/|$)|\.(pem|key|p12|pfx)$'; then
  fail "Nama file yang berpotensi rahasia terdeteksi. Periksa status dan .gitignore; tidak ada file yang di-stage otomatis."
fi

info ""
git_cmd status --short

if ! git_cmd diff --cached --quiet; then
  info "${YELLOW}Staging yang sudah ada akan dipertahankan.${RESET}"
  info "Hanya perubahan yang sudah staged yang akan dipindai dan di-commit."
  if ! git_cmd diff --quiet || [[ -n "$(git_cmd ls-files --others --exclude-standard)" ]]; then
    info "Perubahan unstaged/untracked akan tetap di luar commit ini."
  fi
else
  if ! git_cmd diff --quiet || [[ -n "$(git_cmd ls-files --others --exclude-standard)" ]]; then
    info ""
    info "${YELLOW}Perhatian:${RESET} perubahan berikut dapat dimasukkan ke staging."
    git_cmd status --short
    if ! confirm "Stage semua perubahan di atas?"; then
      info "Staging dibatalkan. File kerja dan staging tetap dipertahankan."
      exit 0
    fi
    git_cmd add -A
  fi
fi

if ! git_cmd diff --cached --quiet; then
  info ""
  info "Ringkasan staging:"
  git_cmd diff --cached --stat
  info "Daftar file staged:"
  git_cmd diff --cached --name-only
  git_cmd diff --cached --check || fail "Whitespace error pada staging. Perbaiki sebelum commit."
  if [[ -n "$(git_cmd diff --cached --name-only | grep -E '(^|/)\.env($|\.)|(^|/)(id_rsa|id_ed25519|credentials(\.json)?|secrets?)(/|$)|\.(pem|key|p12|pfx)$' || true)" ]]; then
    fail "Nama file berpotensi rahasia terdeteksi di staging. Commit dibatalkan."
  fi

  if ! confirm "Commit perubahan staged yang sudah ditampilkan ke main?"; then
    info "Commit dibatalkan. File kerja dan staging tetap dipertahankan."
    exit 0
  fi
  read -r -p "Pesan commit (kosong = Auto sync Termux): " MESSAGE || true
  [[ -n "${MESSAGE:-}" ]] || MESSAGE="Auto sync Termux"
  git_cmd commit -m "$MESSAGE" || fail "Commit gagal. Perubahan lokal tetap tersedia."
else
  info "Tidak ada perubahan staged untuk di-commit."
fi

git_cmd fetch origin || fail "Fetch ulang sebelum push gagal."
REMOTE_MAIN="$(git_cmd rev-parse refs/remotes/origin/main)"
if ! git_cmd merge-base --is-ancestor "$REMOTE_MAIN" HEAD; then
  fail "origin/main menerima perubahan baru atau tidak termasuk riwayat lokal. Commit lokal tetap tersimpan; sinkronkan dan tinjau sebelum mencoba lagi."
fi

AHEAD="$(git_cmd rev-list --count origin/main..HEAD)"
if [[ "$AHEAD" == "0" ]]; then
  info "${GREEN}Tidak ada commit baru untuk dikirim.${RESET}"
  exit 0
fi

info ""
info "Commit yang akan dikirim:"
git_cmd --no-pager log --oneline origin/main..HEAD
if ! confirm "Push commit langsung ke origin/main?"; then
  info "Push dibatalkan. Commit lokal tetap tersimpan di main."
  exit 0
fi

git_cmd push origin main || fail "Push ke origin/main gagal. Commit lokal tetap tersimpan; tidak ada force-push."
info "${GREEN}Push langsung ke origin/main berhasil.${RESET}"
