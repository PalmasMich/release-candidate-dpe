#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ROOT / "release_candidate" / "preview_species.json"


class RCPlayableSpeciesContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads(SPECIES.read_text(encoding="utf-8"))
        cls.by_id = {entry["id"]: entry for entry in payload["species"]}

    def test_preview_has_three_starters_and_first_cagliari_wild(self):
        self.assertTrue({
            "SPECIES_RC_TURTLE_01",
            "SPECIES_RC_FROG_01",
            "SPECIES_RC_FIREFOX_01",
            "SPECIES_RC_CAGLIARI_WILD_01",
        }.issubset(self.by_id))

    def test_tartrek_is_battle_ready_at_level_five(self):
        tartrek = self.by_id["SPECIES_RC_TURTLE_01"]
        self.assertEqual(tartrek["types"], ["TYPE_GRASS", "TYPE_GROUND"])
        available = [move for level, move in tartrek["learnset"] if level <= 5]
        self.assertIn("MOVE_TACKLE", available)
        self.assertIn("MOVE_VINEWHIP", available)
        self.assertGreaterEqual(len(available), 3)

    def test_each_starter_has_a_stab_move_by_level_five(self):
        expected = {
            "SPECIES_RC_TURTLE_01": "MOVE_VINEWHIP",
            "SPECIES_RC_FROG_01": "MOVE_WATERGUN",
            "SPECIES_RC_FIREFOX_01": "MOVE_EMBER",
        }
        for species_id, move in expected.items():
            available = [m for level, m in self.by_id[species_id]["learnset"] if level <= 5]
            self.assertIn(move, available, species_id)

    def test_mistrillo_is_valid_as_an_early_field_encounter(self):
        mistrillo = self.by_id["SPECIES_RC_CAGLIARI_WILD_01"]
        self.assertGreaterEqual(mistrillo["catch_rate"], 150)
        level_one_moves = [move for level, move in mistrillo["learnset"] if level == 1]
        self.assertIn("MOVE_GUST", level_one_moves)
        self.assertLessEqual(sum(mistrillo["base_stats"].values()), 300)


if __name__ == "__main__":
    unittest.main()
