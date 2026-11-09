#!/usr/bin/env bash
# Safe GitHub sync helper for Termux and the proyek_ai monorepo.
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
[[ -n "$BRANCH" ]] || fail "HEAD detached. Pindah ke branch terlebih dahulu."

# Preserve the user's existing index; stage only when the index is empty.
git_cmd diff --cached --quiet || fail "Ada perubahan yang sudah di-stage. Commit atau unstage secara manual sebelum menjalankan github-sync; staging pengguna tidak akan disentuh."

info "${GREEN}DEKEKU — GITHUB SYNC (TERMUX)${RESET}"
info "Repository : $REPO"
info "Branch     : $BRANCH"
info "Remote     : $REMOTE (URL disembunyikan untuk menghindari kebocoran credential)"
info ""

# Refuse ambiguous repository state; never stash, reset, clean, or force-push.
git_cmd fetch --prune "$REMOTE" || fail "Fetch gagal. Periksa koneksi dan autentikasi GitHub."
git_cmd show-ref --verify --quiet refs/remotes/origin/main || fail "origin/main tidak ditemukan."
REMOTE_MAIN="$(git_cmd rev-parse refs/remotes/origin/main)"
LOCAL_MAIN="$(git_cmd rev-parse refs/heads/main 2>/dev/null)" || fail "Branch lokal main tidak ditemukan."

if [[ "$BRANCH" == "main" ]]; then
  [[ "$LOCAL_MAIN" == "$REMOTE_MAIN" ]] || fail "main lokal tidak identik dengan origin/main. Sinkronkan main secara terpisah sebelum memakai tool ini."
  NEW_BRANCH="feat/termux-sync-$(date '+%Y%m%d-%H%M%S')"
  git_cmd switch -c "$NEW_BRANCH" "$REMOTE/main" || fail "Tidak dapat membuat branch fitur. Periksa konflik atau perubahan lokal."
  BRANCH="$NEW_BRANCH"
  info "${GREEN}Branch fitur dibuat:${RESET} $BRANCH"
else
  [[ "$BRANCH" != "main" ]] || fail "Operasi langsung pada main ditolak."
  git_cmd merge-base --is-ancestor "$REMOTE/main" HEAD || fail "Branch ini belum memuat origin/main terbaru. Perbarui branch secara aman terlebih dahulu; tidak ada perubahan yang dipaksakan."
fi

# Guard against common credential/private-key filenames before staging.
if git_cmd status --porcelain | grep -Eiq '(^|/)(\.env|\.env\.[^e]|id_rsa|id_ed25519|credentials(\.json)?|secrets?)(/|$)|\.(pem|key|p12|pfx)$'; then
  fail "Ada file berpotensi rahasia pada perubahan. Periksa .gitignore dan status; tidak ada file yang di-stage otomatis."
fi

info ""
git_cmd status --short
if ! git_cmd diff --quiet || ! git_cmd diff --cached --quiet || [[ -n "$(git_cmd ls-files --others --exclude-standard)" ]]; then
  info ""
  info "${YELLOW}Perhatian:${RESET} semua perubahan non-ignored akan masuk staging."
  git_cmd add -A
  git_cmd diff --cached --stat
  git_cmd diff --cached --name-only
  if ! confirm "Lanjutkan membuat commit dari daftar file di atas?"; then
    git_cmd reset --quiet
    info "Dibatalkan. File kerja tetap ada; staging yang dibuat tool ini dibersihkan."
    exit 0
  fi
  git_cmd diff --cached --check || fail "Whitespace error pada staging. Perbaiki sebelum commit."
  if [[ -n "$(git_cmd diff --cached --name-only | grep -E '(^|/)\.env($|\.)|(^|/)(id_rsa|id_ed25519|credentials(\.json)?|secrets?)(/|$)|\.(pem|key|p12|pfx)$' || true)" ]]; then
    fail "Nama file berpotensi rahasia terdeteksi di staging. Commit dibatalkan."
  fi
  read -r -p "Pesan commit (kosong = Auto sync Termux): " MESSAGE || true
  MESSAGE="${MESSAGE:-Auto sync Termux}"
  git_cmd commit -m "$MESSAGE" || fail "Commit gagal."
fi

if git_cmd show-ref --verify --quiet "refs/remotes/$REMOTE/$BRANCH"; then
  PUSH_BASE="$REMOTE/$BRANCH"
else
  PUSH_BASE="$REMOTE/main"
fi
AHEAD="$(git_cmd rev-list --count "$PUSH_BASE"..HEAD)"
if [[ "$AHEAD" == "0" ]]; then
  info "${GREEN}Tidak ada commit baru untuk dikirim.${RESET}"
  exit 0
fi

info ""
info "Commit yang akan dikirim:"
git_cmd --no-pager log --oneline "$PUSH_BASE"..HEAD
if ! confirm "Push branch '$BRANCH' ke origin?"; then
  info "Push dibatalkan. Commit lokal tetap tersimpan."
  exit 0
fi

git_cmd push --set-upstream "$REMOTE" "$BRANCH" || fail "Push gagal. Tidak ada force-push yang dilakukan."
URL="$(git_cmd remote get-url "$REMOTE")"
URL="${URL%.git}"
URL="${URL#git@github.com:}"
URL="${URL#https://github.com/}"
if [[ "$URL" == */* ]]; then
  info "${GREEN}Push berhasil.${RESET}"
  info "Buat/periksa PR: https://github.com/$URL/compare/main...$BRANCH?expand=1"
else
  info "${GREEN}Push berhasil.${RESET} Buat Pull Request dari branch $BRANCH ke main."
fi
