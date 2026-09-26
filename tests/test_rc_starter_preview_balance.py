import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ROOT / "release_candidate" / "preview_species.json"


class RCStarterPreviewBalanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads(SPECIES.read_text(encoding="utf-8"))
        cls.by_id = {entry["id"]: entry for entry in payload["species"]}

    def test_preview_has_exactly_three_starter_roles(self):
        starters = [entry for entry in self.by_id.values() if entry["role"].startswith("starter_")]
        self.assertEqual(
            {entry["id"] for entry in starters},
            {"SPECIES_RC_TURTLE_01", "SPECIES_RC_FROG_01", "SPECIES_RC_FIREFOX_01"},
        )

    def test_starters_have_comparable_base_stat_totals(self):
        totals = {}
        for species_id in ("SPECIES_RC_TURTLE_01", "SPECIES_RC_FROG_01", "SPECIES_RC_FIREFOX_01"):
            totals[species_id] = sum(self.by_id[species_id]["base_stats"].values())
        self.assertLessEqual(max(totals.values()) - min(totals.values()), 12, totals)

    def test_each_starter_gets_primary_stab_by_level_five(self):
        expected = {
            "SPECIES_RC_TURTLE_01": "MOVE_VINEWHIP",
            "SPECIES_RC_FROG_01": "MOVE_WATERGUN",
            "SPECIES_RC_FIREFOX_01": "MOVE_EMBER",
        }
        for species_id, move in expected.items():
            early_moves = {move_id for level, move_id in self.by_id[species_id]["learnset"] if level <= 5}
            self.assertIn(move, early_moves, f"{species_id} needs usable STAB by level 5")

    def test_all_starters_have_two_level_one_actions(self):
        for species_id in ("SPECIES_RC_TURTLE_01", "SPECIES_RC_FROG_01", "SPECIES_RC_FIREFOX_01"):
            level_one = [move for level, move in self.by_id[species_id]["learnset"] if level == 1]
            self.assertGreaterEqual(len(level_one), 2, f"{species_id} should not enter the KPI rival battle with a one-move kit")


if __name__ == "__main__":
    unittest.main()
