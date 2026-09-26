import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "release_candidate" / "preview_species.json"


class ReleaseCandidatePreviewPlayabilityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads(PREVIEW.read_text(encoding="utf-8"))
        cls.species = {entry["id"]: entry for entry in payload["species"]}

    def test_all_three_starters_have_two_level_one_moves(self):
        for species_id in (
            "SPECIES_RC_TURTLE_01",
            "SPECIES_RC_FROG_01",
            "SPECIES_RC_FIREFOX_01",
        ):
            level_one = [move for level, move in self.species[species_id]["learnset"] if level == 1]
            self.assertGreaterEqual(len(level_one), 2, species_id)

    def test_all_three_starters_can_deal_damage_before_first_rival_battle(self):
        expected_attack = {
            "SPECIES_RC_TURTLE_01": "MOVE_TACKLE",
            "SPECIES_RC_FROG_01": "MOVE_POUND",
            "SPECIES_RC_FIREFOX_01": "MOVE_SCRATCH",
        }
        for species_id, move in expected_attack.items():
            self.assertIn([1, move], self.species[species_id]["learnset"])

    def test_mistrillo_is_battle_ready_at_port_link_level(self):
        mistrillo = self.species["SPECIES_RC_CAGLIARI_WILD_01"]
        self.assertEqual(mistrillo["display_name"], "Mistrillo")
        self.assertIn([1, "MOVE_GUST"], mistrillo["learnset"])
        self.assertGreater(mistrillo["catch_rate"], 0)


if __name__ == "__main__":
    unittest.main()
