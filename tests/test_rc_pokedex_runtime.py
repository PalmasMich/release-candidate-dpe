from pathlib import Path
import importlib.util
import unittest


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "scripts" / "apply_release_candidate_overlay.py"


def load_overlay():
    spec = importlib.util.spec_from_file_location("rc_overlay_pokedex", OVERLAY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RCPokedexRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.overlay = load_overlay()
        self.species = self.overlay.load_species()

    def test_every_active_rc_species_has_unique_nonzero_national_dex_mapping(self):
        values = [item["national_dex"] for item in self.species]
        self.assertEqual(len(values), 4)
        self.assertTrue(all(value > 0 for value in values))
        self.assertEqual(len(values), len(set(values)))

        rendered = self.overlay.render_species_to_pokedex(self.species)
        for item in self.species:
            self.assertIn(
                f"[{item['id']} - 1] = {item['national_dex_symbol']}",
                rendered,
            )

    def test_overlay_tracks_every_custom_pokedex_target(self):
        self.assertIn(self.overlay.SPECIES_TO_POKEDEX, self.overlay.TARGETS)
        self.assertIn(self.overlay.POKEDEX_DATA, self.overlay.TARGETS)
        self.assertIn(self.overlay.POKEDEX_STRINGS, self.overlay.TARGETS)

    def test_overlay_renders_complete_pokedex_records_and_descriptions(self):
        records = self.overlay.render_pokedex_data(self.species)
        descriptions = self.overlay.render_pokedex_strings(self.species)
        for item in self.species:
            symbol = item["national_dex_symbol"]
            description_symbol = item["pokedex"]["description_symbol"]
            self.assertIn(f"[{symbol}] =", records)
            self.assertIn(f".description = {description_symbol}", records)
            self.assertIn(f"#org @{description_symbol}", descriptions)

    def test_table_patch_emits_each_overlay_marker_once(self):
        source = "const int table[] = {\n};\n"
        species_mapping = self.overlay.patch_before_final_terminator(
            source,
            self.overlay.render_species_to_pokedex(self.species),
            self.overlay.SPECIES_TO_POKEDEX_MARKER,
        )
        pokedex_data = self.overlay.patch_before_final_terminator(
            source,
            self.overlay.render_pokedex_data(self.species),
            self.overlay.POKEDEX_DATA_MARKER,
        )
        self.assertEqual(species_mapping.count(self.overlay.SPECIES_TO_POKEDEX_MARKER), 1)
        self.assertEqual(pokedex_data.count(self.overlay.POKEDEX_DATA_MARKER), 1)

    def test_pokedex_records_are_inserted_inside_primary_table(self):
        source = (
            "const struct PokedexEntry gPokedexEntries[NATIONAL_DEX_COUNT] =\n"
            "{\n[NATIONAL_DEX_NONE] = {0},\n};\n\n"
            "const int alternate[] =\n{\n0\n};\n"
        )
        patched = self.overlay.patch_pokedex_data(source, self.species)
        marker = patched.index(self.overlay.POKEDEX_DATA_MARKER)
        alternate = patched.index("const int alternate")
        self.assertLess(marker, alternate)
        self.assertEqual(patched.count(self.overlay.POKEDEX_DATA_MARKER), 1)

    def test_custom_national_dex_range_extends_final_entry(self):
        extension = (ROOT / "include" / "release_candidate_species.h").read_text(encoding="utf-8")
        pokedex = (ROOT / "include" / "pokedex.h").read_text(encoding="utf-8")
        self.assertRegex(extension, r"#define\s+NATIONAL_DEX_RC_TARTREK\s+899")
        self.assertRegex(extension, r"#define\s+NATIONAL_DEX_RC_MISTRILLO\s+902")
        self.assertRegex(pokedex, r"#define\s+FINAL_DEX_ENTRY\s+NATIONAL_DEX_RC_MISTRILLO")
        for symbol in (
            "DEX_ENTRY_RC_TARTREK",
            "DEX_ENTRY_RC_FROBYTE",
            "DEX_ENTRY_RC_EMBERFOX",
            "DEX_ENTRY_RC_MISTRILLO",
        ):
            self.assertIn(f"extern const u8 {symbol}[];", pokedex)


if __name__ == "__main__":
    unittest.main()
