from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAKE = (ROOT / "scripts/make.py").read_text(encoding="utf-8")


class ReleaseCandidateMakeIntegrationTest(unittest.TestCase):
    def test_sprite_assets_are_generated_before_overlay_and_build(self):
        self.assertIn("def GenerateReleaseCandidateAssets()", MAKE)
        self.assertIn("scripts/generate_rc_sprite_assets.py", MAKE)
        self.assertIn("scripts/validate_rc_art_pipeline.py", MAKE)
        main_pos = MAKE.index("def main():")
        validate_call = MAKE.index("ValidateReleaseCandidateArtContract()", main_pos)
        generate_call = MAKE.index("GenerateReleaseCandidateAssets()", main_pos)
        overlay_call = MAKE.index("ApplyReleaseCandidateOverlay()", main_pos)
        self.assertLess(validate_call, generate_call)
        self.assertLess(generate_call, overlay_call)


if __name__ == "__main__":
    unittest.main()
