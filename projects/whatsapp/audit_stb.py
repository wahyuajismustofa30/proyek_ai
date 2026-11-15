#!/usr/bin/env python3
"""
Audit read-only proyek WhatsApp pada STB Armbian.
Tidak mengubah konfigurasi, service, proses, file proyek, atau Git.
Hanya membaca metadata dan menjalankan pemeriksaan diagnostik read-only.
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


class Auditor:
    def __init__(self, root: Path, bridge: Path, gowa: Path):
        self.root = root.resolve()
        self.bridge = bridge.resolve()
        self.gowa = gowa.resolve()
        self.results: list[dict] = []

    def add(self, area: str, status: str, detail: str, recommendation: str = ""):
        self.results.append({
            "area": area,
            "status": status,
            "detail": detail,
            "recommendation": recommendation,
        })

    @staticmethod
    def run(args: list[str], timeout: int = 8) -> tuple[int, str]:
        try:
            p = subprocess.run(
                args, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, timeout=timeout, check=False,
            )
            return p.returncode, p.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            return 127, type(exc).__name__

    def check_environment(self):
        self.add("OS", "INFO", f"{platform.system()} {platform.release()} | {platform.machine()}")
        if platform.machine() not in ("aarch64", "arm64"):
            self.add("Arsitektur", "NOTICE", f"Arsitektur terdeteksi: {platform.machine()}",
                     "Pastikan kompatibilitas target STB ARM64.")
        else:
            self.add("Arsitektur", "PASS", "ARM64 terdeteksi.")

        for cmd in ("python3", "node", "npm", "git", "ss", "systemctl"):
            path = shutil.which(cmd)
            if path:
                version_args = [cmd, "--version"] if cmd in ("python3", "node", "npm", "git") else [cmd, "--help"]
                _, output = self.run(version_args, timeout=4)
                first = output.splitlines()[0] if output else path
                self.add(f"Tool {cmd}", "PASS", first[:180])
            else:
                status = "NOTICE" if cmd in ("ss", "systemctl") else "WARN"
                self.add(f"Tool {cmd}", status, "Tidak ditemukan di PATH.",
                         "Pasang hanya jika memang dibutuhkan; audit ini tidak memasang paket.")

        code, output = self.run(["df", "-h", str(self.root)])
        self.add("Storage", "INFO" if code == 0 else "NOTICE",
                 output.splitlines()[-1] if output else "Informasi storage tidak tersedia.")

        code, output = self.run(["free", "-h"])
        if code == 0:
            lines = output.splitlines()
            mem = next((x for x in lines if x.lower().startswith("mem:")), "Informasi RAM tidak ditemukan.")
            self.add("RAM", "INFO", mem)
        else:
            self.add("RAM", "NOTICE", "Perintah free tidak tersedia.")

    def check_paths(self):
        for label, path in (("Root WhatsApp", self.root),
                            ("GoWA", self.gowa),
                            ("Bridge", self.bridge)):
            self.add(label, "PASS" if path.is_dir() else "WARN",
                     str(path) if path.is_dir() else f"Direktori tidak ditemukan: {path}")

        if self.bridge.is_dir():
            for filename in ("index.js", "gemini.js", "package.json"):
                p = self.bridge / filename
                self.add(f"Bridge/{filename}", "PASS" if p.is_file() else "WARN",
                         "File tersedia." if p.is_file() else "File tidak ditemukan.")

        if self.gowa.is_dir():
            markers = [".git", "go.mod", "main.go", "docker-compose.yml", "Dockerfile"]
            found = [name for name in markers if (self.gowa / name).exists()]
            self.add("Struktur GoWA", "INFO" if found else "NOTICE",
                     "Penanda: " + (", ".join(found) if found else "tidak ditemukan"),
                     "Periksa apakah path GoWA yang diaudit benar.")

    def check_git(self, label: str, path: Path):
        if not (path / ".git").exists():
            self.add(f"Git {label}", "NOTICE", "Bukan working tree Git atau metadata .git tidak tersedia.")
            return
        code, branch = self.run(["git", "-C", str(path), "branch", "--show-current"])
        _, commit = self.run(["git", "-C", str(path), "log", "-1", "--format=%h %s"])
        _, status = self.run(["git", "-C", str(path), "status", "--short"])
        if code == 0:
            self.add(f"Git {label}", "INFO",
                     f"branch={branch or '(detached)'}; HEAD={commit or 'tidak diketahui'}; "
                     f"working_tree={'bersih' if not status else 'ada perubahan lokal'}")
            if status:
                names = [line[3:] for line in status.splitlines()[:15]]
                self.add(f"Perubahan Git {label}", "NOTICE",
                         f"{len(status.splitlines())} entri perubahan; contoh path: " + ", ".join(names))
        else:
            self.add(f"Git {label}", "WARN", "Gagal membaca metadata Git.")

    def check_bridge(self):
        if not self.bridge.is_dir():
            return
        package = self.bridge / "package.json"
        if package.is_file():
            try:
                data = json.loads(package.read_text(encoding="utf-8"))
                test_script = data.get("scripts", {}).get("test", "")
                if "no test specified" in test_script.lower() or "exit 1" in test_script:
                    self.add("Bridge test script", "WARN", "npm test masih placeholder / selalu gagal.",
                             "Tambahkan test otomatis untuk webhook, signature, deduplikasi, dan isolasi route.")
                elif test_script:
                    self.add("Bridge test script", "INFO", f"Script test terdaftar: {test_script}")
                else:
                    self.add("Bridge test script", "WARN", "Tidak ada script test pada package.json.")
            except (json.JSONDecodeError, OSError):
                self.add("package.json", "FAIL", "JSON tidak valid atau tidak dapat dibaca.")

        for filename in ("index.js", "gemini.js"):
            p = self.bridge / filename
            if p.is_file() and shutil.which("node"):
                code, output = self.run(["node", "--check", str(p)], timeout=10)
                self.add(f"Sintaks {filename}", "PASS" if code == 0 else "FAIL",
                         "Sintaks Node.js valid." if code == 0 else output[:300])

        env_file = self.bridge / ".env"
        if env_file.exists():
            try:
                mode = env_file.stat().st_mode & 0o777
                self.add(".env", "PASS" if mode & 0o077 == 0 else "WARN",
                         f"File tersedia; permission={mode:04o}; nilai rahasia tidak dibaca/ditampilkan.",
                         "Batasi permission .env menjadi 600." if mode & 0o077 else "")
                required = {"WEBHOOK_SECRET", "OWNER_JID", "GOWA_DEVICE_ID",
                            "GEMINI_API_KEY", "GEMINI_MODEL"}
                present = set()
                for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
                    m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
                    if m:
                        present.add(m.group(1))
                missing = sorted(required - present)
                self.add("Kelengkapan .env", "PASS" if not missing else "WARN",
                         "Nama variabel wajib tersedia." if not missing else
                         "Nama variabel belum ditemukan: " + ", ".join(missing))
            except OSError:
                self.add(".env", "WARN", "File ada tetapi metadata/konten nama variabel tidak dapat dibaca.")
        else:
            self.add(".env", "NOTICE", ".env tidak ditemukan; nilai environment proses tidak diperiksa.",
                     "Pastikan konfigurasi runtime tersedia tanpa memasukkan secret ke Git.")

    def check_runtime(self):
        code, output = self.run(["ps", "-eo", "pid=,comm="])
        if code == 0:
            matches = [line.strip() for line in output.splitlines()
                       if re.search(r"(?i)(gowa|node|whatsapp)", line)]
            self.add("Proses terkait", "INFO",
                     "; ".join(matches[:15]) if matches else "Tidak ditemukan proses dengan nama terkait.")
        else:
            self.add("Proses terkait", "NOTICE", "Daftar proses tidak dapat dibaca.")

        if shutil.which("ss"):
            code, output = self.run(["ss", "-ltn"])
            if code == 0:
                listeners = [line.strip() for line in output.splitlines()[1:]]
                relevant = [line for line in listeners if re.search(r":(3001|3000|8080|8081|8082)\b", line)]
                self.add("TCP listener", "INFO",
                         "; ".join(relevant[:20]) if relevant else
                         "Tidak ada listener pada port umum 3001/3000/8080/8081/8082 yang terdeteksi.",
                         "Port GoWA aktual perlu dicocokkan dengan konfigurasi lokal.")
        if shutil.which("systemctl"):
            code, output = self.run(["systemctl", "list-units", "--type=service", "--all", "--no-legend", "--no-pager"])
            if code == 0:
                rows = [line.strip() for line in output.splitlines()
                        if re.search(r"(?i)(gowa|whatsapp|bridge)", line)]
                self.add("Systemd service", "INFO",
                         "; ".join(rows[:15]) if rows else
                         "Tidak ditemukan nama service yang mengandung gowa/whatsapp/bridge.",
                         "Nama service mungkin berbeda; audit tidak menghentikan atau mengubah service.")

    def run_all(self):
        self.check_environment()
        self.check_paths()
        self.check_git("WhatsApp", self.root)
        self.check_git("GoWA", self.gowa)
        self.check_git("Bridge", self.bridge)
        self.check_bridge()
        self.check_runtime()
        return self.results


def render_markdown(results: list[dict]) -> str:
    counts = {s: sum(1 for x in results if x["status"] == s)
              for s in ("PASS", "FAIL", "WARN", "NOTICE", "INFO")}
    lines = [
        "# Laporan Audit WhatsApp STB",
        "",
        f"- Waktu UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- Host: {platform.node()}",
        f"- Ringkasan: " + ", ".join(f"{k}={v}" for k, v in counts.items()),
        "",
        "| Status | Area | Hasil |",
        "|---|---|---|",
    ]
    for item in results:
        detail = item["detail"].replace("|", r"\|").replace("\n", " ")
        lines.append(f'| {item["status"]} | {item["area"]} | {detail} |')
        if item["recommendation"]:
            lines.append(f'|  | Rekomendasi | {item["recommendation"]} |')
    lines += ["", "> Audit read-only. Tidak ada konfigurasi atau service yang diubah.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit read-only proyek WhatsApp pada STB.")
    parser.add_argument("--root", type=Path, default=SCRIPT_DIR,
                        help="Direktori kategori WhatsApp (default: lokasi script).")
    parser.add_argument("--bridge", type=Path, default=None,
                        help="Path bridge (default: ROOT/gowa-gemini-bridge).")
    parser.add_argument("--gowa", type=Path, default=None,
                        help="Path GoWA (default: ROOT/gowa).")
    parser.add_argument("--output", type=Path, default=None,
                        help="Simpan laporan Markdown ke file (opsional).")
    parser.add_argument("--json", action="store_true", help="Cetak hasil dalam JSON.")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    bridge = (args.bridge or root / "gowa-gemini-bridge").expanduser()
    gowa = (args.gowa or root / "gowa").expanduser()

    auditor = Auditor(root, bridge, gowa)
    results = auditor.run_all()
    report = json.dumps(results, indent=2, ensure_ascii=False) if args.json else render_markdown(results)

    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report + "\n", encoding="utf-8")
        print(f"Laporan tersimpan: {output}")
    else:
        print(report)

    return 1 if any(x["status"] == "FAIL" for x in results) else 0


if __name__ == "__main__":
    sys.exit(main())
