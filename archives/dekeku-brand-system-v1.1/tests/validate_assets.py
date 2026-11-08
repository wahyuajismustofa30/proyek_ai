#!/usr/bin/env python3
"""Validate DEKEKU brand assets without modifying the read-only v1.1 baseline.

Uses only Python's standard library so the check is reproducible in GitHub Actions.
"""
from __future__ import annotations

import hashlib
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "archives/dekeku-brand-system-v1.1/versions/v1.1/source/Dekeku"
ASSET_ROOTS = (SOURCE / "assets", SOURCE / "public")
MASCOT_SVG = SOURCE / "assets/maskot/svg"
MASCOT_PNG = SOURCE / "assets/maskot/png"

# Known, documented defect in the immutable v1.1 archive. Keep it visible as a
# warning until a corrected raster set is introduced in a new asset version.
KNOWN_BAD_MASCOT_PNG_SHA256 = (
    "e406ef3e5808f1c3336a06be0b44937790b30d3a9caf7f0f12146094c453562d"
)
EXPECTED_MASCOT_SVG = {
    f"maskot-{expression}{suffix}.svg"
    for expression in ("polos", "mikir", "senang", "oops", "sukses")
    for suffix in ("", "-white")
}
EXPECTED_MASCOT_PNG = {
    f"maskot-{expression}{suffix}-512.png"
    for expression in ("polos", "mikir", "senang", "oops", "sukses")
    for suffix in ("", "-white")
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_png(path: Path, errors: list[str]) -> tuple[int, int, str] | None:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        fail(errors, f"{path}: invalid PNG signature")
        return None

    offset = 8
    width = height = None
    idat = bytearray()
    saw_iend = False
    try:
        while offset < len(data):
            if offset + 12 > len(data):
                raise ValueError("truncated PNG chunk")
            length = struct.unpack(">I", data[offset:offset + 4])[0]
            kind = data[offset + 4:offset + 8]
            end = offset + 12 + length
            if end > len(data):
                raise ValueError("chunk exceeds file length")
            payload = data[offset + 8:offset + 8 + length]
            expected_crc = struct.unpack(">I", data[offset + 8 + length:end])[0]
            actual_crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
            if actual_crc != expected_crc:
                raise ValueError(f"CRC mismatch in {kind.decode('ascii', 'replace')}")
            if kind == b"IHDR":
                if length != 13 or width is not None:
                    raise ValueError("invalid IHDR")
                width, height = struct.unpack(">II", payload[:8])
                bit_depth, color_type, compression, filtering, interlace = payload[8:]
                if not width or not height:
                    raise ValueError("zero image dimension")
                if bit_depth not in (1, 2, 4, 8, 16) or color_type not in (0, 2, 3, 4, 6):
                    raise ValueError("unsupported PNG bit depth or color type")
                if compression != 0 or filtering != 0 or interlace not in (0, 1):
                    raise ValueError("invalid PNG method fields")
            elif kind == b"IDAT":
                idat.extend(payload)
            elif kind == b"IEND":
                if length != 0:
                    raise ValueError("invalid IEND")
                saw_iend = True
                offset = end
                break
            offset = end
        if width is None or height is None or not idat or not saw_iend:
            raise ValueError("missing IHDR, IDAT, or IEND")
        # Decode the compressed stream to catch truncated/corrupt raster data.
        zlib.decompress(bytes(idat))
        if offset != len(data):
            raise ValueError("unexpected bytes after IEND")
        return width, height, digest
    except (ValueError, zlib.error, struct.error) as exc:
        fail(errors, f"{path}: {exc}")
        return None


def validate_svg(path: Path, errors: list[str]) -> None:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        fail(errors, f"{path}: invalid SVG/XML: {exc}")
        return
    if not root.tag.endswith("svg"):
        fail(errors, f"{path}: root element is not <svg>")
    viewbox = root.attrib.get("viewBox")
    if not viewbox or len(viewbox.split()) != 4:
        fail(errors, f"{path}: missing or malformed viewBox")
    if path.parent == MASCOT_SVG:
        title = root.find("{http://www.w3.org/2000/svg}title")
        if not root.attrib.get("role") or not root.attrib.get("aria-label") or title is None:
            fail(errors, f"{path}: mascot SVG must include role, aria-label, and title")
    for element in root.iter():
        for attr in ("href", "{http://www.w3.org/1999/xlink}href"):
            value = element.attrib.get(attr, "")
            if value and not value.startswith(("#", "data:")):
                fail(errors, f"{path}: external or file reference is not allowed: {value}")


def main() -> int:
    errors: list[str] = []
    png_count = svg_count = 0
    for root in ASSET_ROOTS:
        if not root.is_dir():
            fail(errors, f"missing asset directory: {root}")
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() == ".png":
                png_count += 1
                validate_png(path, errors)
            elif path.suffix.lower() == ".svg":
                svg_count += 1
                validate_svg(path, errors)

    if not MASCOT_SVG.is_dir() or not MASCOT_PNG.is_dir():
        fail(errors, "mascot SVG/PNG directories are missing")
    else:
        actual_svg = {p.name for p in MASCOT_SVG.glob("*.svg")}
        actual_png = {p.name for p in MASCOT_PNG.glob("*.png")}
        if actual_svg != EXPECTED_MASCOT_SVG:
            fail(errors, f"mascot SVG inventory mismatch; missing={sorted(EXPECTED_MASCOT_SVG-actual_svg)}, extra={sorted(actual_svg-EXPECTED_MASCOT_SVG)}")
        if actual_png != EXPECTED_MASCOT_PNG:
            fail(errors, f"mascot PNG inventory mismatch; missing={sorted(EXPECTED_MASCOT_PNG-actual_png)}, extra={sorted(actual_png-EXPECTED_MASCOT_PNG)}")

        hashes: dict[str, list[str]] = {}
        for path in sorted(MASCOT_PNG.glob("*.png")):
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                hashes.setdefault(digest, []).append(path.name)
            except OSError as exc:
                fail(errors, f"{path}: cannot read file: {exc}")
        for digest, names in hashes.items():
            if len(names) > 1 and digest != KNOWN_BAD_MASCOT_PNG_SHA256:
                fail(errors, f"duplicate mascot PNG content detected ({digest}): {', '.join(names)}")
            elif len(names) > 1:
                print("WARNING: known broken v1.1 mascot PNG set remains identical; do not use these raster files.")

    print(f"Checked {svg_count} SVG and {png_count} PNG files under the DEKEKU v1.1 baseline.")
    if errors:
        print("Asset validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print("Asset file integrity, SVG structure, and mascot inventory checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
