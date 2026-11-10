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

# Preserve the user's existing index; staging is never modified by this tool.
git_cmd diff --cached --quiet || fail "Ada perubahan yang sudah di-stage. Commit atau unstage secara manual sebelum menjalankan github-sync; staging pengguna tidak akan disentuh."

info "${GREEN}DEKEKU — GITHUB SYNC (TERMUX)${RESET}"
info "Repository : $REPO"
info "Branch     : $BRANCH"
info "Remote     : $REMOTE (URL disembunyikan untuk menghindari kebocoran credential)"
info ""

# Fetch updates, but never reset, clean, stash, or force-push.
git_cmd fetch --prune "$REMOTE" || fail "Fetch gagal. Periksa koneksi dan autentikasi GitHub."
git_cmd show-ref --verify --quiet "refs/remotes/$REMOTE/main" || fail "$REMOTE/main tidak ditemukan."
REMOTE_MAIN="$(git_cmd rev-parse "refs/remotes/$REMOTE/main")"
LOCAL_MAIN="$(git_cmd rev-parse refs/heads/main 2>/dev/null)" || fail "Branch lokal main tidak ditemukan."

if [[ "$BRANCH" == "main" ]]; then
  [[ "$LOCAL_MAIN" == "$REMOTE_MAIN" ]] || fail "main lokal tidak identik dengan $REMOTE/main. Sinkronkan main secara terpisah sebelum memakai tool ini."
  NEW_BRANCH="feat/termux-sync-$(date '+%Y%m%d-%H%M%S')"
  git_cmd switch -c "$NEW_BRANCH" "$REMOTE/main" || fail "Tidak dapat membuat branch fitur. Periksa konflik atau perubahan lokal."
  BRANCH="$NEW_BRANCH"
  info "${GREEN}Branch fitur dibuat:${RESET} $BRANCH"
else
  # Bring an existing feature branch up to date safely. Fast-forward when
  # possible; otherwise create a normal merge commit. No history is rewritten.
  if ! git_cmd merge-base --is-ancestor "$REMOTE_MAIN" HEAD; then
    if git_cmd merge-base --is-ancestor HEAD "$REMOTE_MAIN"; then
      SYNC_MODE="fast-forward"
      SYNC_DESCRIPTION="Branch lokal hanya tertinggal dari $REMOTE/main."
    else
      SYNC_MODE="merge"
      SYNC_DESCRIPTION="Branch lokal dan $REMOTE/main memiliki commit masing-masing."
    fi

    info "${YELLOW}$SYNC_DESCRIPTION${RESET}"
    if ! confirm "Integrasikan $REMOTE/main ke branch '$BRANCH' sekarang?"; then
      info "Sinkronisasi dibatalkan. Working tree dan branch tetap dipertahankan."
      exit 0
    fi

    if [[ "$SYNC_MODE" == "fast-forward" ]]; then
      git_cmd merge --ff-only "$REMOTE_MAIN" || fail "Fast-forward gagal. Periksa git status; perubahan lokal tidak di-reset."
    else
      if ! git_cmd merge --no-edit "$REMOTE_MAIN"; then
        fail "Merge $REMOTE/main gagal atau mengalami konflik. Selesaikan konflik secara manual, commit hasil merge, lalu jalankan github-sync kembali. Tidak ada reset/abort otomatis."
      fi
    fi
    info "${GREEN}Branch berhasil diperbarui dari $REMOTE/main.${RESET}"
  fi
fi

# Regenerate the project index whenever project source changes.
if [[ -n "$(git_cmd status --porcelain -- projects/)" ]]; then
  if ! git_cmd diff --quiet -- docs/PROJECT_INDEX.md; then
    fail "docs/PROJECT_INDEX.md has local edits. Review or commit those edits before automatic regeneration."
  fi
  command -v python3 >/dev/null 2>&1 || fail "Python 3 is required to update docs/PROJECT_INDEX.md when projects/ changes."
  python3 "$REPO/scripts/update_project_index.py" --write || fail "Automatic project-index update failed."
  info "Indeks proyek diperbarui otomatis."
fi

# Guard common secret filenames in Git's porcelain status output.
if git_cmd status --porcelain | grep -Eiq '(^|[[:space:]])([^[:space:]]*/)?(\.env(\.[^/]*)?|id_rsa|id_ed25519|credentials(\.json)?|secrets?)(/|$)|\.(pem|key|p12|pfx)$'; then
  fail "Ada file dengan nama yang berpotensi rahasia pada perubahan. Periksa .gitignore dan status; tidak ada file yang di-stage otomatis."
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
  if ! git_cmd merge-base --is-ancestor "$PUSH_BASE" HEAD; then
    fail "Branch remote $REMOTE/$BRANCH memiliki commit yang belum ada di lokal. Integrasikan branch remote tersebut secara manual; push dibatalkan tanpa force-push."
  fi
else
  PUSH_BASE="$REMOTE/main"
  git_cmd merge-base --is-ancestor "$PUSH_BASE" HEAD || fail "HEAD belum memuat $REMOTE/main terbaru. Push dibatalkan."
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

# Build a PR URL only for recognized GitHub remote URL forms. Never print the
# raw remote URL because it may contain an embedded username or token.
REMOTE_URL="$(git_cmd remote get-url "$REMOTE")"
REPO_SLUG=""
case "$REMOTE_URL" in
  git@github.com:*) REPO_SLUG="${REMOTE_URL#git@github.com:}" ;;
  ssh://git@github.com/*) REPO_SLUG="${REMOTE_URL#ssh://git@github.com/}" ;;
  https://*|http://*)
    URL_PART="${REMOTE_URL#https://}"
    URL_PART="${URL_PART#http://}"
    URL_PART="${URL_PART#*@}"
    if [[ "$URL_PART" == github.com/* ]]; then
      REPO_SLUG="${URL_PART#github.com/}"
    fi
    ;;
esac
REPO_SLUG="${REPO_SLUG%.git}"
if [[ "$REPO_SLUG" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  info "${GREEN}Push berhasil.${RESET}"
  info "Buat/periksa PR: https://github.com/$REPO_SLUG/compare/main...$BRANCH?expand=1"
else
  info "${GREEN}Push berhasil.${RESET} Buat Pull Request dari branch $BRANCH ke main."
fi
