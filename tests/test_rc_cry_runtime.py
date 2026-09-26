from pathlib import Path
import importlib.util
import unittest


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "scripts" / "apply_release_candidate_overlay.py"


def load_overlay():
    spec = importlib.util.spec_from_file_location("rc_overlay_cries", OVERLAY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RCCryRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.overlay = load_overlay()
        self.species = self.overlay.load_species()

    def test_overlay_tracks_both_runtime_cry_tables(self):
        self.assertIn(self.overlay.CRY_TABLE, self.overlay.TARGETS)
        self.assertIn(self.overlay.CRY_TABLE_2, self.overlay.TARGETS)

    def test_every_active_rc_species_gets_nonzero_cry_records(self):
        for table in (self.overlay.CRY_TABLE, self.overlay.CRY_TABLE_2):
            rendered = self.overlay.render_cry_table_entries(
                self.species,
                table.read_text(encoding="utf-8"),
            )
            for mon in self.species:
                self.assertIn(f"[{mon['id']}] =", rendered)
            self.assertNotIn(".wav = (u8*) 0x0", rendered)


if __name__ == "__main__":
    unittest.main()
