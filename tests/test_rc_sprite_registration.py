from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "scripts" / "apply_release_candidate_overlay.py"


def load_overlay():
    spec = importlib.util.spec_from_file_location("rc_overlay", OVERLAY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseCandidateSpriteRegistrationTest(unittest.TestCase):
    def test_overlay_tracks_sprite_registration_tables(self):
        overlay = load_overlay()
        expected = {
            ROOT / "src" / "Front_Pic_Table.c",
            ROOT / "src" / "Back_Pic_Table.c",
            ROOT / "src" / "Icon_Table.c",
            ROOT / "src" / "Palette_Table.c",
            ROOT / "src" / "Shiny_Palette_Table.c",
            ROOT / "src" / "Icon_Palette_Table.c",
            ROOT / "src" / "Front_Pic_Coords_Table.c",
            ROOT / "src" / "Back_Pic_Coords_Table.c",
            ROOT / "include" / "sprite_data.h",
        }
        self.assertTrue(expected.issubset(set(overlay.TARGETS)))

    def test_tartrek_registration_uses_generated_symbols(self):
        overlay = load_overlay()
        species = overlay.load_species()
        rendered = overlay.render_sprite_registration(species)
        combined = "\n".join(rendered.values())

        self.assertIn(
            "[SPECIES_RC_TURTLE_01] = {gFrontSprite1294RCTartrekTiles",
            combined,
        )
        self.assertIn(
            "[SPECIES_RC_TURTLE_01] = {gBackShinySprite1294RCTartrekTiles",
            combined,
        )
        self.assertIn(
            "[SPECIES_RC_TURTLE_01] = gIconSprite1294RCTartrekTiles",
            combined,
        )
        self.assertIn("gFrontSprite1294RCTartrekPal", combined)
        self.assertIn("gBackShinySprite1294RCTartrekPal", combined)
        self.assertIn("[SPECIES_RC_TURTLE_01] = 0x0", combined)
        self.assertIn(".size = 0x66", combined)

    def test_registration_patch_is_idempotent(self):
        overlay = load_overlay()
        species = overlay.load_species()
        rendered = overlay.render_sprite_registration(species)
        source = "const int table[] = {\n};\n"
        entry = rendered["front_table"]
        once = overlay.patch_before_final_terminator(source, entry, overlay.FRONT_TABLE_MARKER)
        twice = overlay.patch_before_final_terminator(once, entry, overlay.FRONT_TABLE_MARKER)
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
