#!/usr/bin/env python3
"""Read-only Termux inventory; writes a private Markdown report."""
from __future__ import annotations

import argparse
import datetime as dt
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

VERSION = "1.0.1"
HOME = Path.home()


def run(args: list[str], timeout: int = 10) -> tuple[str, str]:
    exe = shutil.which(args[0])
    if not exe:
        return "", "NOT AVAILABLE"
    try:
        result = subprocess.run(
            [exe, *args[1:]], text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=timeout, check=False,
            env={**os.environ, "LC_ALL": "C"},
        )
        return (result.stdout or result.stderr).strip(), (
            "PASS" if result.returncode == 0 else f"EXIT {result.returncode}"
        )
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT"
    except OSError as exc:
        return "", f"ERROR: {type(exc).__name__}"


def read(path: str, limit: int = 12000) -> str:
    try:
        return Path(path).read_text(errors="replace")[:limit].strip()
    except OSError:
        return ""


def cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\r", "").replace("\n", "<br>").strip() or "Tidak tersedia"


def table(rows: list[tuple[object, object]]) -> str:
    return "| Item | Informasi |\n|---|---|\n" + "\n".join(
        f"| {cell(k)} | {cell(v)} |" for k, v in rows
    )


def section(name: str, body: str) -> str:
    return f"\n## {name}\n\n{body.strip() or 'Tidak tersedia atau akses dibatasi.'}\n"


def prop(key: str) -> str:
    value, status = run(["getprop", key])
    return value if status == "PASS" and value else "Tidak tersedia"


def report(include_packages: bool) -> str:
    now = dt.datetime.now().astimezone()
    prefix = os.environ.get("PREFIX", "")
    summary = [
        ("Waktu audit", now.strftime("%Y-%m-%d %H:%M:%S %Z")),
        ("Versi audit", VERSION), ("Hostname", platform.node()),
        ("User", os.environ.get("USER", str(os.getuid()))),
        ("HOME", HOME), ("PREFIX", prefix or "Tidak tersedia"),
        ("Shell", os.environ.get("SHELL", "Tidak tersedia")),
        ("Python", sys.version.split()[0]), ("Platform", platform.platform()),
        ("Kernel", platform.release()), ("Arsitektur", platform.machine()),
        ("Android", prop("ro.build.version.release")),
    ]
    android = [
        ("Produsen", "ro.product.manufacturer"), ("Merek", "ro.product.brand"),
        ("Model", "ro.product.model"), ("Perangkat", "ro.product.device"),
        ("Versi Android", "ro.build.version.release"),
        ("Android SDK", "ro.build.version.sdk"),
        ("Patch keamanan", "ro.build.version.security_patch"),
        ("Build ID", "ro.build.id"), ("ABI utama", "ro.product.cpu.abi"),
    ]
    cpu = [("Arsitektur Python", platform.machine()),
           ("Jumlah core", os.cpu_count() or "Tidak tersedia")]
    model = ""
    for line in read("/proc/cpuinfo").splitlines():
        if re.match(r"^(model name|Hardware|Processor)\s*:", line, re.I):
            model = line.split(":", 1)[1].strip()
            if model:
                break
    cpu.append(("Model CPU", model or "Tidak tersedia"))

    mem = []
    wanted = {"MemTotal", "MemAvailable", "MemFree", "Buffers", "Cached", "SwapTotal", "SwapFree"}
    for line in read("/proc/meminfo").splitlines():
        match = re.match(r"^(\w+):\s+(\d+)\s+kB", line)
        if match and match.group(1) in wanted:
            mem.append((match.group(1), f"{int(match.group(2)) / 1024:.1f} MiB"))

    storage, storage_status = run(["df", "-h", "-T"])
    if storage_status != "PASS" or not storage:
        storage, storage_status = run(["df", "-h"])
    if storage:
        lines = storage.splitlines()
        storage = "\n".join([lines[0]] + [
            line for line in lines[1:]
            if any(x in line for x in ("/data", "/storage", "/sdcard", "/system", "/vendor", "/"))
        ][:44])
    else:
        storage = f"Tidak dapat membaca penyimpanan ({storage_status})."

    net_parts = []
    for label, args in (
        ("Interface dan alamat lokal", ["ip", "-brief", "addr"]),
        ("Routing", ["ip", "route"]),
    ):
        value, status = run(args)
        net_parts.append(f"**{label}**\n\n```text\n{value or status}\n```")
    dns = read("/etc/resolv.conf", 4000)
    dns_lines = [x for x in dns.splitlines() if x.strip().startswith(("nameserver ", "search ", "domain "))]
    if dns_lines:
        net_parts.append("**DNS resolver**\n\n```text\n" + "\n".join(dns_lines) + "\n```")

    commands = [
        "bash", "sh", "python", "python3", "pip", "git", "curl", "wget",
        "jq", "rsync", "ssh", "php", "node", "npm", "clang", "make",
        "proot", "termux-info", "termux-battery-status", "termux-wake-lock",
        "termux-setup-storage", "ip", "ifconfig", "lsof", "ps", "df", "du",
        "pkg", "apt", "dpkg-query",
    ]
    tools = table([(name, shutil.which(name) or "Tidak ditemukan di PATH") for name in commands])

    if include_packages:
        packages, package_status = run(
            ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\n"], 25
        )
        if not packages:
            packages, package_status = run(["pkg", "list-installed"], 25)
        package_lines = sorted(set(x.strip() for x in packages.splitlines() if x.strip()))
        package_body = f"Jumlah paket terdeteksi: **{len(package_lines)}**\n\n" + "\n".join(
            f"- `{x}`" for x in package_lines
        ) if package_lines else f"Tidak dapat membaca daftar paket ({package_status})."
    else:
        package_body, package_status = "Dilewati sesuai opsi --no-packages.", "SKIPPED"

    processes, process_status = run(["ps", "-A", "-o", "PID,PPID,USER,STAT,NAME"])
    if not processes:
        processes, process_status = run(["ps", "-o", "PID,PPID,STAT,NAME"])
    process_body = "```text\n" + "\n".join(processes.splitlines()[:101]) + "\n```" if processes else process_status

    battery, battery_status = run(["termux-battery-status"])
    info, info_status = run(["termux-info"], 15)
    dirs = [
        ("HOME tersedia", HOME.is_dir()),
        ("PREFIX tersedia", Path(prefix).is_dir() if prefix else False),
        ("Shared storage ~/storage/shared", (HOME / "storage/shared").is_dir()),
        ("Direktori ~/projects", (HOME / "projects").is_dir()),
        ("Direktori ~/bin", (HOME / "bin").is_dir()),
        ("Akses /proc", os.access("/proc", os.R_OK)),
        ("Akses /sys", os.access("/sys", os.R_OK)),
        ("UID", os.getuid()), ("Root", os.getuid() == 0),
    ]

    parts = [
        "# Laporan Audit Termux",
        "> Inventarisasi read-only; bukan audit keamanan atau penetration test.",
        section("Ringkasan", table(summary)),
        section("Identitas Android", table([(k, prop(v)) for k, v in android])),
        section("CPU", table(cpu)), section("Memori", table(mem)),
        section("Penyimpanan", "```text\n" + storage + "\n```"),
        section("Jaringan", "\n\n".join(net_parts)),
        section("Direktori dan akses", table(dirs)),
        section("Command dan tool", tools),
        section("Paket Termux terpasang", package_body),
        section("Proses aktif", process_body),
        section("Baterai", "```json\n" + battery + "\n```" if battery and battery_status == "PASS" else f"NOTICE: tidak tersedia/diizinkan ({battery_status})."),
        section("Ringkasan termux-info", "```text\n" + info[:10000] + "\n```" if info and info_status == "PASS" else f"NOTICE: tidak tersedia/gagal ({info_status})."),
        section("Status pemeriksaan", table([
            ("Inventaris paket", package_status), ("termux-info", info_status),
            ("Battery API", battery_status),
            ("Shared storage", "PASS" if (HOME / "storage/shared").is_dir() else "NOTICE"),
        ])),
        section("Catatan keamanan", """
- Tidak membaca file credential, token, password, API key, private key, atau riwayat shell.
- Argumen command proses tidak dikumpulkan.
- Laporan dapat memuat alamat IP lokal, gateway, nama perangkat, dan inventaris aplikasi. Simpan secara pribadi sebelum membagikannya.
- Gunakan --no-packages untuk melewati inventaris paket.
- Informasi kosong dapat disebabkan pembatasan Android/Termux dan tidak otomatis menunjukkan kerusakan.
"""),
    ]
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit read-only Termux dan buat laporan Markdown.")
    parser.add_argument("-o", "--output", help="Lokasi file Markdown keluaran.")
    parser.add_argument("--stdout", action="store_true", help="Tampilkan laporan ke terminal.")
    parser.add_argument("--no-packages", action="store_true", help="Lewati inventaris paket terpasang.")
    args = parser.parse_args()
    content = report(not args.no_packages)
    if args.stdout:
        print(content, end="")
        return 0
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    target = Path(args.output).expanduser() if args.output else (
        HOME / ".local/share/termux-audit" / f"termux-audit-{stamp}.md"
    )
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        try:
            target.chmod(0o600)
            target.parent.chmod(0o700)
        except OSError:
            pass
    except OSError as exc:
        print(f"Gagal menyimpan laporan: {exc}", file=sys.stderr)
        return 1
    print("Audit Termux selesai.")
    print(f"Laporan: {target}")
    print("Simpan laporan secara pribadi sebelum membagikannya.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
