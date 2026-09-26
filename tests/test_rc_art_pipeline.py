from pathlib import Path
import copy
import importlib.util
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_rc_art_pipeline.py"
MANIFEST = ROOT / "release_candidate" / "starter_art_manifest.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("rc_art_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RCArtPipelineTest(unittest.TestCase):
    def test_current_manifest_is_valid_but_explicitly_bootstrap(self):
        validator = load_validator()
        manifest = validator.load_manifest(MANIFEST)
        self.assertEqual(validator.validate(manifest), [])
        self.assertEqual(validator.overall_status(manifest), "BOOTSTRAP")

    def test_starter_slots_match_stable_species_ids(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        actual = {
            item["species_id"]: (item["slot_hex"], item["slot_decimal"])
            for item in manifest["starters"]
        }
        self.assertEqual(
            actual,
            {
                "SPECIES_RC_TURTLE_01": ("0x050E", 1294),
                "SPECIES_RC_FROG_01": ("0x050F", 1295),
                "SPECIES_RC_FIREFOX_01": ("0x0510", 1296),
            },
        )

    def test_cannot_claim_production_ready_with_pending_stages(self):
        validator = load_validator()
        manifest = validator.load_manifest(MANIFEST)
        broken = copy.deepcopy(manifest)
        broken["starters"][0]["production_ready"] = True
        errors = validator.validate(broken)
        self.assertIn("production_ready requires every stage approved", "\n".join(errors))

    def test_strict_cli_contract_rejects_bootstrap_manifest(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(MANIFEST.read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual(validator.run(path, require_approved=True), 1)


if __name__ == "__main__":
    unittest.main()
