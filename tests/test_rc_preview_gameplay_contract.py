from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "release_candidate" / "preview_species.json"


class RCPreviewGameplayContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads(SPEC.read_text(encoding="utf-8"))
        cls.by_id = {item["id"]: item for item in payload["species"]}

    def test_preview_species_ids_are_complete_and_unique(self):
        expected = {
            "SPECIES_RC_TURTLE_01",
            "SPECIES_RC_FROG_01",
            "SPECIES_RC_FIREFOX_01",
            "SPECIES_RC_CAGLIARI_WILD_01",
        }
        self.assertEqual(set(self.by_id), expected)

    def test_each_starter_can_attack_immediately_at_level_five(self):
        damaging = {
            "SPECIES_RC_TURTLE_01": {"MOVE_TACKLE", "MOVE_VINEWHIP"},
            "SPECIES_RC_FROG_01": {"MOVE_POUND", "MOVE_WATERGUN"},
            "SPECIES_RC_FIREFOX_01": {"MOVE_SCRATCH", "MOVE_EMBER"},
        }
        for species_id, expected_moves in damaging.items():
            learned = {move for level, move in self.by_id[species_id]["learnset"] if int(level) <= 5}
            self.assertTrue(expected_moves <= learned, f"{species_id} lost its level-5 battle kit")

    def test_starter_secondary_types_are_distinct(self):
        types = {
            species_id: tuple(self.by_id[species_id]["types"])
            for species_id in (
                "SPECIES_RC_TURTLE_01",
                "SPECIES_RC_FROG_01",
                "SPECIES_RC_FIREFOX_01",
            )
        }
        self.assertEqual(types["SPECIES_RC_TURTLE_01"], ("TYPE_GRASS", "TYPE_GROUND"))
        self.assertEqual(types["SPECIES_RC_FROG_01"], ("TYPE_WATER", "TYPE_ELECTRIC"))
        self.assertEqual(types["SPECIES_RC_FIREFOX_01"], ("TYPE_FIRE", "TYPE_DARK"))

    def test_mistrillo_is_ready_for_the_first_field_encounter(self):
        mistrillo = self.by_id["SPECIES_RC_CAGLIARI_WILD_01"]
        self.assertEqual(mistrillo["display_name"], "Mistrillo")
        learned_at_three = {move for level, move in mistrillo["learnset"] if int(level) <= 3}
        self.assertIn("MOVE_GUST", learned_at_three)
        self.assertGreaterEqual(int(mistrillo["catch_rate"]), 150)


if __name__ == "__main__":
    unittest.main()
