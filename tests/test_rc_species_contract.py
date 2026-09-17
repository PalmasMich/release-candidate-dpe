from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPECIES = (ROOT / "include/species.h").read_text(encoding="utf-8")

REQUIRED = [
    "SPECIES_RC_TURTLE_01",
    "SPECIES_RC_FROG_01",
    "SPECIES_RC_FIREFOX_01",
    "SPECIES_RC_CAGLIARI_WILD_01",
    "SPECIES_RC_CAGLIARI_WILD_02",
]


class ReleaseCandidateSpeciesContractTest(unittest.TestCase):
    def test_rc_species_are_reserved(self):
        for name in REQUIRED:
            self.assertIn(name, SPECIES)

    def test_rc_species_are_before_num_species(self):
        num_species = SPECIES.index("#define NUM_SPECIES")
        for name in REQUIRED:
            self.assertLess(SPECIES.index(name), num_species)


if __name__ == "__main__":
    unittest.main()
