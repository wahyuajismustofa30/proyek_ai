#!/usr/bin/env python3
"""
Audit bukti kompatibilitas GoWA <-> Gemini Bridge (read-only).

- Tidak menjalankan/mengubah service.
- Tidak mengirim request ke GoWA/Gemini.
- Tidak membaca nilai .env atau environment rahasia.
- Menyimpan snapshot JSON + Markdown agar hasil pemeriksaan dapat ditinjau ulang.
- --show-latest membaca snapshot terakhir tanpa memindai source lagi.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR
DEFAULT_STATE = Path.home() / ".local" / "state" / "proyek_ai" / "whatsapp-audit"

# Cari indikator kontrak dan alur webhook, bukan seluruh isi source.
GO_PATTERNS = {
    "webhook_dispatch": r"(?i)webhook|http\.post|http\.newrequest|client\.do\(",
    "event_and_message": r"(?i)is_from_me|chat_id|message_id|message\.id|\.body|event",
    "device_and_identity": r"(?i)device_id|deviceid|jid|sender|from_me|pushname",
    "signature_and_hmac": r"(?i)hmac|sha256|signature|x-hub-signature|webhook.?secret",
    "retry_and_timeout": r"(?i)retry|backoff|timeout|deadline|http\.client",
}
BRIDGE_PATTERNS = {
    "device_and_owner": r"deviceId|device_id|ownerJid|OWNER_JID|GOWA_DEVICE_ID",
    "event_and_message": r"data\.event|data\.payload|chat_id|is_from_me|msg\.from|msg\.body|msg\.id",
    "signature": r"x-hub-signature-256|createHmac|timingSafeEqual|verifySignature",
    "routing_and_dedup": r"isOwnerSelfChat|CUSTOMER|OWNER|rememberMessage|processingMessages",
}
SENSITIVE_ASSIGNMENT = re.compile(
    r"(?i)(secret|token|password|passwd|api[_-]?key|private[_-]?key)\s*[:=]"
)
GO_EXTENSIONS = {".go", ".yaml", ".yml", ".json", ".toml", ".env.example"}
MAX_FILES = 3000
MAX_MATCHES_PER_CATEGORY = 80
MAX_FILE_BYTES = 2 * 1024 * 1024


def run(args: list[str], cwd: Path | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(
            args, cwd=cwd, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=10, check=False,
        )
        return p.returncode, p.stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, type(exc).__name__


def sha256_file(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def safe_line(line: str) -> str:
    """Redaksi nilai assignment sensitif dan batasi panjang bukti."""
    if SENSITIVE_ASSIGNMENT.search(line):
        return "[REDACTED: baris mengandung assignment sensitif]"
    line = line.strip()
    return line[:240] + ("…" if len(line) > 240 else "")


def scan_tree(root: Path, patterns: dict[str, str], allowed: set[str]) -> dict[str, Any]:
    output: dict[str, Any] = {"root": str(root), "exists": root.is_dir(), "files_scanned": 0,
                              "matches": {}, "truncated": False}
    if not root.is_dir():
        return output

    compiled = {name: re.compile(pattern) for name, pattern in patterns.items()}
    excluded = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv"}
    file_count = 0

    for path in root.rglob("*"):
        if not path.is_file() or any(part in excluded for part in path.parts):
            continue
        if path.suffix.lower() not in allowed and path.name not in {"Dockerfile", "docker-compose.yml"}:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        file_count += 1
        if file_count > MAX_FILES:
            output["truncated"] = True
            break

        relative = str(path.relative_to(root))
        for category, regex in compiled.items():
            for number, line in enumerate(text.splitlines(), 1):
                if regex.search(line):
                    rows = output["matches"].setdefault(category, [])
                    if len(rows) >= MAX_MATCHES_PER_CATEGORY:
                        output["truncated"] = True
                        continue
                    rows.append({
                        "file": relative,
                        "line": number,
                        "evidence": safe_line(line),
                        "file_sha256": sha256_file(path),
                    })

    output["files_scanned"] = min(file_count, MAX_FILES)
    return output


def git_metadata(path: Path) -> dict[str, str | None]:
    if not path.exists():
        return {"exists": "false"}
    code, branch = run(["git", "-C", str(path), "branch", "--show-current"])
    _, head = run(["git", "-C", str(path), "rev-parse", "HEAD"])
    _, status = run(["git", "-C", str(path), "status", "--short", "--branch"])
    status_lines = status.splitlines() if code == 0 else []
    changed_lines = [line for line in status_lines if not line.startswith("## ")]
    return {
        "exists": "true",
        "is_git": "true" if code == 0 else "false",
        "branch": branch if code == 0 else None,
        "head": head if code == 0 else None,
        "status_summary": "clean" if code == 0 and not changed_lines else "changes_present",
        "status_output": status[:2000] if code == 0 else None,
    }


def bridge_config_audit(bridge: Path) -> dict[str, Any]:
    """Ambil nama variabel konfigurasi saja; tidak membaca nilai .env."""
    result: dict[str, Any] = {"env_file_present": False, "env_variable_names": [],
                              "missing_names": [], "env_permissions": None}
    env_file = bridge / ".env"
    if env_file.is_file():
        result["env_file_present"] = True
        try:
            result["env_permissions"] = oct(env_file.stat().st_mode & 0o777)
            names = set()
            for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
                match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
                if match:
                    names.add(match.group(1))
            result["env_variable_names"] = sorted(names)
            required = {"WEBHOOK_SECRET", "OWNER_JID", "GOWA_DEVICE_ID",
                        "GEMINI_API_KEY", "GEMINI_MODEL"}
            result["missing_names"] = sorted(required - names)
        except OSError:
            result["read_error"] = "Tidak dapat membaca metadata/nama variabel .env"
    else:
        result["note"] = ".env tidak ditemukan; nilai environment tidak diperiksa."
    return result


def collect(root: Path, bridge: Path, gowa: Path) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "host": {"platform": platform.platform(), "machine": platform.machine(),
                 "python": platform.python_version()},
        "paths": {"whatsapp_root": str(root), "bridge": str(bridge), "gowa": str(gowa)},
        "git": {"repository": git_metadata(root.parents[1] if len(root.parents) > 1 else root),
                "gowa": git_metadata(gowa), "bridge": git_metadata(bridge)},
        "bridge": {
            "source_scan": scan_tree(bridge, BRIDGE_PATTERNS, {".js", ".cjs", ".mjs"}),
            "config_names_only": bridge_config_audit(bridge),
        },
        "gowa": {
            "source_scan": scan_tree(gowa, GO_PATTERNS, GO_EXTENSIONS),
        },
        "limitations": [
            "Pencarian pola berbasis pola teks; bukan bukti semantik atau kompatibilitas runtime.",
            "File rahasia dan nilai environment tidak dikumpulkan.",
            "Tidak ada service, endpoint, atau API eksternal yang dipanggil.",
            "GoWA yang tidak tersedia menghasilkan NOT VERIFIED, bukan dianggap kompatibel.",
        ],
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Snapshot Audit Bukti GoWA ↔ Gemini Bridge", "",
        f"- Waktu UTC: {report['generated_at_utc']}",
        f"- Host: {report['host']['platform']} ({report['host']['machine']})",
        f"- Bridge: `{report['paths']['bridge']}`",
        f"- GoWA: `{report['paths']['gowa']}`", "",
        "## Status awal",
    ]
    gowa = report["gowa"]["source_scan"]
    bridge = report["bridge"]["source_scan"]
    lines += [
        f"- Source GoWA tersedia: **{'YA' if gowa['exists'] else 'TIDAK'}**",
        f"- File GoWA dipindai: **{gowa['files_scanned']}**",
        f"- File Bridge dipindai: **{bridge['files_scanned']}**",
        f"- GoWA scan terpotong: **{gowa['truncated']}**",
        f"- `.env` tersedia: **{report['bridge']['config_names_only']['env_file_present']}**",
        "",
        "> Snapshot ini mengumpulkan bukti untuk audit manual. Hasil pencarian pola tidak otomatis membuktikan kompatibilitas.", "",
    ]
    for title, key, section in [
        ("Bukti GoWA", "gowa", gowa),
        ("Bukti Bridge", "bridge", bridge),
    ]:
        lines += [f"## {title}", ""]
        matches = section.get("matches", {})
        if not matches:
            lines += ["Tidak ada kecocokan pola atau source tidak tersedia.", ""]
        for category, entries in matches.items():
            lines += [f"### {category}", ""]
            for item in entries:
                lines.append(
                    f"- `{item['file']}:{item['line']}` "
                    f"(SHA-256 `{item['file_sha256'] or 'unavailable'}`): "
                    f"`{item['evidence'].replace(chr(96), chr(39))}`"
                )
            lines.append("")
    env = report["bridge"]["config_names_only"]
    lines += ["## Konfigurasi (nama variabel saja)", "",
              f"- Permission `.env`: `{env.get('env_permissions') or 'NOT AVAILABLE'}`",
              f"- Nama variabel: {', '.join(env.get('env_variable_names', [])) or 'NOT AVAILABLE'}",
              f"- Nama wajib yang belum ditemukan: {', '.join(env.get('missing_names', [])) or 'tidak ada/tidak dapat ditentukan'}",
              "", "## Batasan dan tindak lanjut", ""]
    lines.extend(f"- {item}" for item in report["limitations"])
    lines += [
        "- Cocokkan `device_id` dengan `GOWA_DEVICE_ID` berdasarkan pembentukan field di GoWA.",
        "- Cocokkan `OWNER_JID` dengan JID akun/pengirim/chat berdasarkan source GoWA.",
        "- Pastikan event, arah pesan, message ID, chat ID, dan isi pesan sama bentuknya.",
        "- Buktikan algoritma, raw body, secret, nama header, dan encoding signature pada kedua sisi.",
        "- Jangan aktifkan endpoint pengiriman atau mengirim pesan untuk keperluan audit ini.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot audit read-only GoWA ↔ Bridge.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                        help="Direktori projects/whatsapp.")
    parser.add_argument("--bridge", type=Path, default=None)
    parser.add_argument("--gowa", type=Path, default=None)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE,
                        help="Lokasi snapshot lokal di luar repository.")
    parser.add_argument("--show-latest", action="store_true",
                        help="Tampilkan snapshot terakhir tanpa memindai source.")
    parser.add_argument("--refresh", action="store_true",
                        help="Buat snapshot baru (default jika bukan --show-latest).")
    args = parser.parse_args()

    state_dir = args.state_dir.expanduser().resolve()
    latest_json = state_dir / "latest.json"
    latest_md = state_dir / "latest.md"

    if args.show_latest:
        if not latest_json.is_file():
            print("Snapshot belum tersedia. Jalankan script tanpa --show-latest.", file=sys.stderr)
            return 2
        try:
            report = json.loads(latest_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print("Snapshot JSON tidak dapat dibaca.", file=sys.stderr)
            return 2
        print(latest_md.read_text(encoding="utf-8") if latest_md.is_file()
              else json.dumps(report, indent=2, ensure_ascii=False))
        print(f"\nSnapshot tersimpan di: {state_dir}")
        return 0

    root = args.root.expanduser().resolve()
    bridge = (args.bridge or root / "gowa-gemini-bridge").expanduser().resolve()
    gowa = (args.gowa or root / "gowa").expanduser().resolve()
    report = collect(root, bridge, gowa)
    rendered = markdown(report)

    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        latest_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        latest_md.write_text(rendered + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Gagal menyimpan snapshot: {type(exc).__name__}", file=sys.stderr)
        return 2

    print(rendered)
    print(f"\nSnapshot JSON: {latest_json}")
    print(f"Snapshot Markdown: {latest_md}")
    return 0 if report["gowa"]["source_scan"]["exists"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
