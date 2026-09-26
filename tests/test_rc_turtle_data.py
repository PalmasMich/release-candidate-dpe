import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_release_candidate_overlay.py"
MANIFEST = ROOT / "release_candidate" / "preview_species.json"

spec = importlib.util.spec_from_file_location("rc_overlay", SCRIPT)
rc_overlay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc_overlay)


class ReleaseCandidateTurtleDataTest(unittest.TestCase):
    def setUp(self):
        self.species = json.loads(MANIFEST.read_text(encoding="utf-8"))["species"]
        self.turtle = next(mon for mon in self.species if mon["id"] == "SPECIES_RC_TURTLE_01")

    def test_turtle_preview_baseline(self):
        self.assertEqual(self.turtle["display_name"], "Tartrek")
        self.assertEqual(self.turtle["types"], ["TYPE_GRASS", "TYPE_GROUND"])
        self.assertEqual(
            self.turtle["base_stats"],
            {"hp": 48, "attack": 55, "defense": 60, "sp_attack": 42, "sp_defense": 55, "speed": 40},
        )
        self.assertEqual(self.turtle["catch_rate"], 45)
        self.assertIn([1, "MOVE_TACKLE"], self.turtle["learnset"])
        self.assertIn([5, "MOVE_VINEWHIP"], self.turtle["learnset"])

    def test_base_stats_overlay_is_idempotent(self):
        source = "const struct BaseStats gBaseStats[] =\n{\n\t[SPECIES_NONE] = {0},\n};\n"
        first = rc_overlay.patch_base_stats(source, [self.turtle])
        second = rc_overlay.patch_base_stats(first, [self.turtle])
        self.assertEqual(first, second)
        self.assertIn("SPECIES_RC_TURTLE_01", first)
        self.assertIn("TYPE_GRASS", first)
        self.assertIn("TYPE_GROUND", first)

    def test_learnset_overlay_adds_definition_and_table_entry_once(self):
        source = (
            "static const struct LevelUpMove sEmptyMoveset[] = { LEVEL_UP_END };\n\n"
            "const struct LevelUpMove* const gLevelUpLearnsets[NUM_SPECIES] =\n"
            "{\n\t[SPECIES_NONE] = sEmptyMoveset,\n};\n"
        )
        first = rc_overlay.patch_learnsets(source, [self.turtle])
        second = rc_overlay.patch_learnsets(first, [self.turtle])
        self.assertEqual(first, second)
        self.assertEqual(first.count("sTartrekLevelUpLearnset"), 2)
        self.assertIn("MOVE_VINEWHIP", first)

    def test_name_overlay_adds_display_name_once(self):
        source = "MAX_LENGTH=10\nFILL_FF=True\n\n#org @gSpeciesNames\n#org @NAME_SPECIES_NONE\n??????\n"
        first = rc_overlay.patch_names(source, [self.turtle])
        second = rc_overlay.patch_names(first, [self.turtle])
        self.assertEqual(first, second)
        self.assertIn("#org @NAME_RC_TURTLE_01", first)
        self.assertIn("Tartrek", first)


if __name__ == "__main__":
    unittest.main()
