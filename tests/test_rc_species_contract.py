from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = (ROOT / "include/species.h").read_text(encoding="utf-8")
RC_SPECIES = (ROOT / "include/release_candidate_species.h").read_text(encoding="utf-8")
DEFINES = (ROOT / "src/defines.h").read_text(encoding="utf-8")

REQUIRED = [
    "SPECIES_RC_TURTLE_01",
    "SPECIES_RC_FROG_01",
    "SPECIES_RC_FIREFOX_01",
    "SPECIES_RC_CAGLIARI_WILD_01",
    "SPECIES_RC_CAGLIARI_WILD_02",
]


class ReleaseCandidateSpeciesContractTest(unittest.TestCase):
    def test_rc_species_are_reserved_in_extension_header(self):
        for name in REQUIRED:
            self.assertIn(name, RC_SPECIES)

    def test_extension_does_not_rewrite_upstream_species(self):
        for name in REQUIRED:
            self.assertNotIn(name, UPSTREAM)

    def test_num_species_is_extended_after_rc_ids(self):
        for name in REQUIRED:
            self.assertLess(RC_SPECIES.index(name), RC_SPECIES.index("#define NUM_SPECIES"))

    def test_dpe_sources_include_extension_after_upstream_species(self):
        upstream_include = '#include "../include/species.h"'
        rc_include = '#include "../include/release_candidate_species.h"'
        self.assertIn(upstream_include, DEFINES)
        self.assertIn(rc_include, DEFINES)
        self.assertLess(DEFINES.index(upstream_include), DEFINES.index(rc_include))


if __name__ == "__main__":
    unittest.main()
