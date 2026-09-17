#!/usr/bin/env python3
from pathlib import Path
import binascii
import struct
import zlib

PALETTE = [
    (0, 0, 0),
    (33, 54, 35),
    (74, 112, 63),
    (112, 153, 83),
    (158, 190, 112),
    (104, 78, 48),
    (145, 108, 68),
    (189, 151, 94),
    (213, 195, 143),
    (56, 73, 48),
    (236, 229, 192),
    (44, 44, 39),
    (126, 92, 52),
    (174, 128, 72),
    (90, 132, 80),
    (202, 175, 112),
]


def _chunk(kind: bytes, payload: bytes) -> bytes:
    crc = binascii.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)


def write_indexed_png(path: Path, pixels, width: int, height: int):
    path.parent.mkdir(parents=True, exist_ok=True)
    if len(pixels) != height or any(len(row) != width for row in pixels):
        raise ValueError("pixel matrix dimensions do not match output dimensions")
    if any(value < 0 or value > 15 for row in pixels for value in row):
        raise ValueError("4-bit indexed PNG supports palette indices 0..15")

    packed_rows = []
    for row in pixels:
        packed = bytearray([0])
        for x in range(0, width, 2):
            packed.append((row[x] << 4) | row[x + 1])
        packed_rows.append(bytes(packed))

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 4, 3, 0, 0, 0)
    plte = b"".join(bytes(rgb) for rgb in PALETTE)
    trns = bytes([0] + [255] * 15)
    idat = zlib.compress(b"".join(packed_rows), level=9)
    path.write_bytes(
        signature
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"PLTE", plte)
        + _chunk(b"tRNS", trns)
        + _chunk(b"IDAT", idat)
        + _chunk(b"IEND", b"")
    )


def _canvas(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]


def _ellipse(canvas, cx, cy, rx, ry, colour):
    height = len(canvas)
    width = len(canvas[0])
    for y in range(max(0, cy - ry), min(height, cy + ry + 1)):
        for x in range(max(0, cx - rx), min(width, cx + rx + 1)):
            if ((x - cx) * (x - cx)) / (rx * rx) + ((y - cy) * (y - cy)) / (ry * ry) <= 1:
                canvas[y][x] = colour


def _rect(canvas, x0, y0, x1, y1, colour):
    for y in range(max(0, y0), min(len(canvas), y1 + 1)):
        for x in range(max(0, x0), min(len(canvas[0]), x1 + 1)):
            canvas[y][x] = colour


def _outline_ellipse(canvas, cx, cy, rx, ry, outline, fill):
    _ellipse(canvas, cx, cy, rx + 2, ry + 2, outline)
    _ellipse(canvas, cx, cy, rx, ry, fill)


def _front_sprite():
    canvas = _canvas(64, 64)
    _outline_ellipse(canvas, 31, 39, 18, 12, 1, 3)
    _outline_ellipse(canvas, 27, 36, 13, 10, 11, 6)
    _ellipse(canvas, 27, 35, 9, 7, 7)
    _rect(canvas, 19, 31, 35, 33, 12)
    _rect(canvas, 20, 34, 22, 43, 12)
    _rect(canvas, 34, 34, 36, 43, 12)
    _outline_ellipse(canvas, 45, 31, 9, 8, 1, 4)
    _ellipse(canvas, 50, 29, 1, 1, 11)
    _rect(canvas, 49, 29, 49, 29, 10)
    _ellipse(canvas, 39, 38, 5, 3, 2)
    _ellipse(canvas, 42, 40, 4, 2, 14)
    _outline_ellipse(canvas, 20, 49, 5, 3, 1, 2)
    _outline_ellipse(canvas, 39, 49, 5, 3, 1, 2)
    _rect(canvas, 24, 29, 30, 30, 15)
    _rect(canvas, 43, 25, 46, 26, 8)
    return canvas


def _back_sprite():
    canvas = _canvas(64, 64)
    _outline_ellipse(canvas, 32, 40, 18, 12, 1, 3)
    _outline_ellipse(canvas, 31, 35, 15, 12, 11, 6)
    _ellipse(canvas, 31, 34, 11, 9, 7)
    _rect(canvas, 30, 25, 32, 45, 5)
    _rect(canvas, 21, 33, 41, 35, 5)
    _rect(canvas, 21, 28, 23, 44, 12)
    _rect(canvas, 39, 28, 41, 44, 12)
    _outline_ellipse(canvas, 44, 31, 8, 7, 1, 4)
    _ellipse(canvas, 41, 27, 3, 2, 8)
    _outline_ellipse(canvas, 21, 50, 5, 3, 1, 2)
    _outline_ellipse(canvas, 40, 50, 5, 3, 1, 2)
    return canvas


def _icon_sprite():
    canvas = _canvas(32, 64)
    for frame, yoff in enumerate((0, 32)):
        bob = 0 if frame == 0 else 1
        _outline_ellipse(canvas, 15, yoff + 18 + bob, 10, 7, 1, 3)
        _outline_ellipse(canvas, 13, yoff + 16 + bob, 7, 6, 11, 6)
        _outline_ellipse(canvas, 23, yoff + 13 + bob, 5, 4, 1, 4)
        _rect(canvas, 22, yoff + 12 + bob, 22, yoff + 12 + bob, 11)
        _rect(canvas, 10, yoff + 12 + bob, 16, yoff + 13 + bob, 12)
    return canvas


def generate_tartrek_assets(root: Path):
    root = Path(root)
    outputs = [
        (root / "graphics/frontspr/gFrontSprite1268RCTartrek.png", _front_sprite(), 64, 64),
        (root / "graphics/backspr/gBackSprite1268RCTartrek.png", _back_sprite(), 64, 64),
        (root / "graphics/pokeicon/gIconSprite1268RCTartrek.png", _icon_sprite(), 32, 64),
    ]
    written = []
    for path, pixels, width, height in outputs:
        write_indexed_png(path, pixels, width, height)
        written.append(path)
    return written


def main():
    root = Path(__file__).resolve().parents[1]
    for path in generate_tartrek_assets(root):
        print(path.relative_to(root))


if __name__ == "__main__":
    main()
