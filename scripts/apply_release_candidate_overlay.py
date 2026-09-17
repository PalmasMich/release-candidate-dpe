#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "release_candidate" / "preview_species.json"
BASE_STATS = ROOT / "src" / "Base_Stats.c"
LEARNSETS = ROOT / "src" / "Learnsets.c"
NAMES = ROOT / "strings" / "Pokemon_Name_Table.string"

BASE_MARKER = "/* RC_OVERLAY:BASE_STATS */"
LEARNSET_MARKER = "/* RC_OVERLAY:LEARNSETS */"
NAME_MARKER = "# RC_OVERLAY:SPECIES_NAMES"


def load_species():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data["species"]


def camel_name(display_name: str) -> str:
    return "".join(part.capitalize() for part in display_name.replace("-", " ").split())


def render_base_stats(species):
    blocks = [BASE_MARKER]
    for mon in species:
        stats = mon["base_stats"]
        t1, t2 = mon["types"]
        egg1, egg2 = mon["egg_groups"]
        ability1, ability2 = mon["abilities"]
        blocks.append(
            f"\t[{mon['id']}] =\n"
            "\t{\n"
            f"\t\t.baseHP = {stats['hp']},\n"
            f"\t\t.baseAttack = {stats['attack']},\n"
            f"\t\t.baseDefense = {stats['defense']},\n"
            f"\t\t.baseSpAttack = {stats['sp_attack']},\n"
            f"\t\t.baseSpDefense = {stats['sp_defense']},\n"
            f"\t\t.baseSpeed = {stats['speed']},\n"
            f"\t\t.type1 = {t1},\n"
            f"\t\t.type2 = {t2},\n"
            f"\t\t.catchRate = {mon['catch_rate']},\n"
            f"\t\t.expYield = {mon['exp_yield']},\n"
            "\t\t.evYield_HP = 0,\n"
            "\t\t.evYield_Attack = 0,\n"
            "\t\t.evYield_Defense = 1,\n"
            "\t\t.evYield_SpAttack = 0,\n"
            "\t\t.evYield_SpDefense = 0,\n"
            "\t\t.evYield_Speed = 0,\n"
            "\t\t.item1 = ITEM_NONE,\n"
            "\t\t.item2 = ITEM_NONE,\n"
            f"\t\t.genderRatio = PERCENT_FEMALE({mon['gender_ratio_female_percent']}),\n"
            f"\t\t.eggCycles = {mon['egg_cycles']},\n"
            f"\t\t.friendship = {mon['friendship']},\n"
            f"\t\t.growthRate = {mon['growth_rate']},\n"
            f"\t\t.eggGroup1 = {egg1},\n"
            f"\t\t.eggGroup2 = {egg2},\n"
            f"\t\t.ability1 = {ability1},\n"
            f"\t\t.ability2 = {ability2},\n"
            "\t\t.safariZoneFleeRate = 0,\n"
            f"\t\t.hiddenAbility = {mon['hidden_ability']},\n"
            "\t\t.noFlip = TRUE,\n"
            "\t},"
        )
    return "\n".join(blocks) + "\n"


def render_learnset_defs(species):
    blocks = [LEARNSET_MARKER]
    for mon in species:
        cname = camel_name(mon["display_name"])
        lines = [f"static const struct LevelUpMove s{cname}LevelUpLearnset[] = {{"]
        for level, move in mon["learnset"]:
            lines.append(f"\tLEVEL_UP_MOVE({level:2d}, {move}),")
        lines.extend(["\tLEVEL_UP_END", "};"])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n\n"


def render_learnset_table_entries(species):
    lines = []
    for mon in species:
        cname = camel_name(mon["display_name"])
        lines.append(f"\t[{mon['id']}] = s{cname}LevelUpLearnset,")
    return "\n".join(lines) + "\n"


def render_names(species):
    chunks = [NAME_MARKER]
    for mon in species:
        symbol = mon["id"].replace("SPECIES_", "NAME_")
        chunks.extend([f"#org @{symbol}", mon["display_name"], ""])
    return "\n".join(chunks).rstrip() + "\n"


def patch_base_stats(text: str, species) -> str:
    if BASE_MARKER in text:
        return text
    pos = text.rfind("\n};")
    if pos < 0:
        raise ValueError("Could not find final gBaseStats terminator")
    return text[:pos] + "\n" + render_base_stats(species) + text[pos:]


def patch_learnsets(text: str, species) -> str:
    if LEARNSET_MARKER in text:
        return text
    table_marker = "const struct LevelUpMove* const gLevelUpLearnsets[NUM_SPECIES] ="
    table_pos = text.find(table_marker)
    if table_pos < 0:
        raise ValueError("Could not find gLevelUpLearnsets table")
    text = text[:table_pos] + render_learnset_defs(species) + text[table_pos:]

    table_pos = text.find(table_marker)
    open_brace = text.find("{", table_pos)
    close_brace = text.find("\n};", open_brace)
    if open_brace < 0 or close_brace < 0:
        raise ValueError("Could not find gLevelUpLearnsets table boundaries")
    return text[:close_brace] + "\n" + render_learnset_table_entries(species) + text[close_brace:]


def patch_names(text: str, species) -> str:
    if NAME_MARKER in text:
        return text
    return text.rstrip() + "\n\n" + render_names(species)


def apply_overlay():
    species = load_species()
    BASE_STATS.write_text(patch_base_stats(BASE_STATS.read_text(encoding="utf-8"), species), encoding="utf-8")
    LEARNSETS.write_text(patch_learnsets(LEARNSETS.read_text(encoding="utf-8"), species), encoding="utf-8")
    NAMES.write_text(patch_names(NAMES.read_text(encoding="utf-8"), species), encoding="utf-8")
    print(f"Applied Release Candidate overlay for {len(species)} species.")


def main():
    parser = argparse.ArgumentParser(description="Apply source-controlled Release Candidate data to upstream DPE tables.")
    parser.parse_args()
    apply_overlay()


if __name__ == "__main__":
    main()
