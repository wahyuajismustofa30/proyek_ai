#!/usr/bin/env python3
"""Create a new project by safely copying the repository's AI project template."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = REPOSITORY_ROOT / "templates" / "ai-project"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "projects"


def validate_project_name(name: str) -> str:
    """Validate and return a trimmed project name."""
    if any(unicodedata.category(char) == "Cc" for char in name):
        raise ValueError("Nama proyek tidak boleh memuat karakter kontrol.")
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Nama proyek tidak boleh kosong.")
    if len(clean_name) > 80:
        raise ValueError("Nama proyek maksimal 80 karakter.")
    return clean_name


def project_slug(name: str) -> str:
    """Convert a human-readable project name to a safe directory slug."""
    name = validate_project_name(name)
    normalized = unicodedata.normalize("NFKD", name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_name).strip("-").lower()
    if not slug or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Nama proyek harus menghasilkan slug yang valid.")
    if len(slug) > 63:
        raise ValueError("Slug proyek maksimal 63 karakter.")
    return slug


def bootstrap_project(
    name: str,
    output_root: Path,
    template_dir: Path = DEFAULT_TEMPLATE,
    *,
    dry_run: bool = False,
) -> Path:
    """Copy the template to output_root/<slug> and personalize project headings."""
    clean_name = validate_project_name(name)
    slug = project_slug(clean_name)
    source = template_dir.resolve()
    destination_root = output_root.expanduser().resolve()
    destination = destination_root / slug

    if not source.is_dir():
        raise FileNotFoundError(f"Template tidak ditemukan: {source}")
    if destination == source or source in destination.parents:
        raise ValueError("Lokasi tujuan tidak boleh berada di dalam folder template.")
    if destination.exists():
        raise FileExistsError(f"Folder tujuan sudah ada: {destination}")
    if dry_run:
        return destination

    destination_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    try:
        for path in destination.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            try:
                original = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            replacements = {
                "[NAMA PROYEK]": clean_name,
                "{{PROJECT_NAME}}": clean_name,
                "{{PROJECT_SLUG}}": slug,
            }
            updated = original
            for placeholder, value in replacements.items():
                replacement = (
                    json.dumps(value)[1:-1]
                    if path.suffix.lower() == ".json"
                    else value
                )
                updated = updated.replace(placeholder, replacement)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        raise
    return destination


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Buat proyek baru dari templates/ai-project."
    )
    parser.add_argument("--name", help="Nama proyek (akan diminta jika tidak diberikan).")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="Folder induk proyek (default: projects/).")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE,
                        help="Lokasi template sumber.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Tampilkan lokasi target tanpa membuat atau mengubah file.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    name = args.name if args.name is not None else input("Nama proyek baru: ")
    try:
        destination = bootstrap_project(
            name, args.output, args.template, dry_run=args.dry_run
        )
    except (ValueError, FileNotFoundError, FileExistsError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"[DRY RUN] Proyek akan dibuat di: {destination}")
    else:
        print(f"Proyek berhasil dibuat: {destination}")
        print("Langkah berikutnya:")
        print("1. Lengkapi README.md dan docs/PROJECT_BRIEF.md.")
        print("2. Tinjau AGENTS.md, docs/ARCHITECTURE.md, dan docs/TASKS.md.")
        print("3. Pilih stack, tambahkan manifest serta lockfile, lalu jalankan test.")
        print("4. Periksa secret, dependency, dan workflow CI sebelum push.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
