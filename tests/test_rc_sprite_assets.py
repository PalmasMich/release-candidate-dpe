from pathlib import Path
import importlib.util
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_rc_sprite_assets.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("rc_sprite_generator", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_png_header(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path} is not a PNG")
    assert data[12:16] == b"IHDR"
    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    return width, height, bit_depth, color_type


class ReleaseCandidateSpriteAssetTest(unittest.TestCase):
    def test_tartrek_generator_writes_dpe_ready_indexed_assets(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            written = generator.generate_tartrek_assets(out)
            self.assertEqual(
                {p.relative_to(out).as_posix() for p in written},
                {
                    "graphics/frontspr/gFrontSprite1294RCTartrek.png",
                    "graphics/backspr/gBackShinySprite1294RCTartrek.png",
                    "graphics/pokeicon/gIconSprite1294RCTartrek.png",
                },
            )
            self.assertEqual(read_png_header(out / "graphics/frontspr/gFrontSprite1294RCTartrek.png"), (64, 64, 4, 3))
            self.assertEqual(read_png_header(out / "graphics/backspr/gBackShinySprite1294RCTartrek.png"), (64, 64, 4, 3))
            self.assertEqual(read_png_header(out / "graphics/pokeicon/gIconSprite1294RCTartrek.png"), (32, 64, 4, 3))

    def test_frobyte_generator_writes_dpe_ready_indexed_assets(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            written = generator.generate_frobyte_assets(out)
            self.assertEqual(
                {p.relative_to(out).as_posix() for p in written},
                {
                    "graphics/frontspr/gFrontSprite1295RCFrobyte.png",
                    "graphics/backspr/gBackShinySprite1295RCFrobyte.png",
                    "graphics/pokeicon/gIconSprite1295RCFrobyte.png",
                },
            )
            self.assertEqual(read_png_header(out / "graphics/frontspr/gFrontSprite1295RCFrobyte.png"), (64, 64, 4, 3))

    def test_emberfox_generator_writes_dpe_ready_indexed_assets(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            written = generator.generate_emberfox_assets(out)
            self.assertEqual(
                {p.relative_to(out).as_posix() for p in written},
                {
                    "graphics/frontspr/gFrontSprite1296RCEmberfox.png",
                    "graphics/backspr/gBackShinySprite1296RCEmberfox.png",
                    "graphics/pokeicon/gIconSprite1296RCEmberfox.png",
                },
            )
            self.assertEqual(read_png_header(out / "graphics/frontspr/gFrontSprite1296RCEmberfox.png"), (64, 64, 4, 3))

    def test_mistrillo_generator_writes_dpe_ready_indexed_assets(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            written = generator.generate_mistrillo_assets(out)
            self.assertEqual(
                {p.relative_to(out).as_posix() for p in written},
                {
                    "graphics/frontspr/gFrontSprite1297RCMistrillo.png",
                    "graphics/backspr/gBackShinySprite1297RCMistrillo.png",
                    "graphics/pokeicon/gIconSprite1297RCMistrillo.png",
                },
            )
            self.assertEqual(read_png_header(out / "graphics/frontspr/gFrontSprite1297RCMistrillo.png"), (64, 64, 4, 3))
            self.assertEqual(read_png_header(out / "graphics/backspr/gBackShinySprite1297RCMistrillo.png"), (64, 64, 4, 3))
            self.assertEqual(read_png_header(out / "graphics/pokeicon/gIconSprite1297RCMistrillo.png"), (32, 64, 4, 3))


if __name__ == "__main__":
    unittest.main()
