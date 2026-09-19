from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ROOT / "release_candidate" / "preview_species.json"


class RCPlayablePreviewContractTest(unittest.TestCase):
    def setUp(self):
        data = json.loads(SPECIES.read_text(encoding="utf-8"))["species"]
        self.by_id = {item["id"]: item for item in data}

    def test_preview_species_namespace_is_complete(self):
        self.assertEqual(
            set(self.by_id),
            {
                "SPECIES_RC_TURTLE_01",
                "SPECIES_RC_FROG_01",
                "SPECIES_RC_FIREFOX_01",
                "SPECIES_RC_CAGLIARI_WILD_01",
            },
        )

    def test_every_starter_can_attack_immediately(self):
        expected = {
            "SPECIES_RC_TURTLE_01": "MOVE_TACKLE",
            "SPECIES_RC_FROG_01": "MOVE_POUND",
            "SPECIES_RC_FIREFOX_01": "MOVE_SCRATCH",
        }
        for species_id, move in expected.items():
            level_one = {entry[1] for entry in self.by_id[species_id]["learnset"] if entry[0] == 1}
            self.assertIn(move, level_one)

    def test_mistrillo_first_encounter_is_battle_ready(self):
        mistrillo = self.by_id["SPECIES_RC_CAGLIARI_WILD_01"]
        self.assertEqual(mistrillo["display_name"], "Mistrillo")
        self.assertEqual(mistrillo["types"], ["TYPE_FLYING", "TYPE_NORMAL"])
        level_one = {entry[1] for entry in mistrillo["learnset"] if entry[0] == 1}
        self.assertIn("MOVE_GUST", level_one)
        self.assertGreater(mistrillo["catch_rate"], 100)

    def test_preview_starters_keep_distinct_battle_identities(self):
        self.assertEqual(self.by_id["SPECIES_RC_TURTLE_01"]["types"], ["TYPE_GRASS", "TYPE_GROUND"])
        self.assertEqual(self.by_id["SPECIES_RC_FROG_01"]["types"], ["TYPE_WATER", "TYPE_ELECTRIC"])
        self.assertEqual(self.by_id["SPECIES_RC_FIREFOX_01"]["types"], ["TYPE_FIRE", "TYPE_DARK"])


if __name__ == "__main__":
    unittest.main()
