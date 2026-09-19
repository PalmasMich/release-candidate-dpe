from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPECIES_FILE = ROOT / "release_candidate" / "preview_species.json"


class RCPreviewBattleReadinessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.species = {item["id"]: item for item in json.loads(SPECIES_FILE.read_text())["species"]}

    def test_preview_species_have_usable_level_one_moves(self):
        for species_id, item in self.species.items():
            level_one = [move for level, move in item["learnset"] if level == 1]
            self.assertGreaterEqual(len(level_one), 2, species_id)
            self.assertTrue(any(move not in {"MOVE_GROWL", "MOVE_WITHDRAW", "MOVE_TAILWHIP"} for move in level_one), species_id)

    def test_starters_gain_a_typed_attack_by_level_five(self):
        expected = {
            "SPECIES_RC_TURTLE_01": "MOVE_VINEWHIP",
            "SPECIES_RC_FROG_01": "MOVE_WATERGUN",
            "SPECIES_RC_FIREFOX_01": "MOVE_EMBER",
        }
        for species_id, move in expected.items():
            learned = {known_move for level, known_move in self.species[species_id]["learnset"] if level <= 5}
            self.assertIn(move, learned, species_id)

    def test_mistrillo_is_immediately_battle_ready_for_first_field_test(self):
        mistrillo = self.species["SPECIES_RC_CAGLIARI_WILD_01"]
        level_one = {move for level, move in mistrillo["learnset"] if level == 1}
        self.assertIn("MOVE_GUST", level_one)
        self.assertEqual(mistrillo["role"], "cagliari_wild")


if __name__ == "__main__":
    unittest.main()
