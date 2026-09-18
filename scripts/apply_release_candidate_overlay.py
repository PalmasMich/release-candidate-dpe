#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "release_candidate" / "preview_species.json"
BASE_STATS = ROOT / "src" / "Base_Stats.c"
LEARNSETS = ROOT / "src" / "Learnsets.c"
NAMES = ROOT / "strings" / "Pokemon_Name_Table.string"
FRONT_TABLE = ROOT / "src" / "Front_Pic_Table.c"
BACK_TABLE = ROOT / "src" / "Back_Pic_Table.c"
ICON_TABLE = ROOT / "src" / "Icon_Table.c"
PALETTE_TABLE = ROOT / "src" / "Palette_Table.c"
SHINY_PALETTE_TABLE = ROOT / "src" / "Shiny_Palette_Table.c"
ICON_PALETTE_TABLE = ROOT / "src" / "Icon_Palette_Table.c"
FRONT_COORDS_TABLE = ROOT / "src" / "Front_Pic_Coords_Table.c"
BACK_COORDS_TABLE = ROOT / "src" / "Back_Pic_Coords_Table.c"
SPRITE_DATA = ROOT / "include" / "sprite_data.h"
BACKUP_DIR = ROOT / "build" / "rc_overlay_backup"

BASE_MARKER = "/* RC_OVERLAY:BASE_STATS */"
LEARNSET_MARKER = "/* RC_OVERLAY:LEARNSETS */"
NAME_MARKER = "#org @NAME_RC_TURTLE_01"
FRONT_TABLE_MARKER = "/* RC_OVERLAY:FRONT_PIC_TABLE */"
BACK_TABLE_MARKER = "/* RC_OVERLAY:BACK_PIC_TABLE */"
ICON_TABLE_MARKER = "/* RC_OVERLAY:ICON_TABLE */"
PALETTE_TABLE_MARKER = "/* RC_OVERLAY:PALETTE_TABLE */"
SHINY_PALETTE_TABLE_MARKER = "/* RC_OVERLAY:SHINY_PALETTE_TABLE */"
ICON_PALETTE_TABLE_MARKER = "/* RC_OVERLAY:ICON_PALETTE_TABLE */"
FRONT_COORDS_MARKER = "/* RC_OVERLAY:FRONT_COORDS */"
BACK_COORDS_MARKER = "/* RC_OVERLAY:BACK_COORDS */"
SPRITE_DATA_MARKER = "/* RC_OVERLAY:SPRITE_DATA */"

TARGETS = (
    BASE_STATS,
    LEARNSETS,
    NAMES,
    FRONT_TABLE,
    BACK_TABLE,
    ICON_TABLE,
    PALETTE_TABLE,
    SHINY_PALETTE_TABLE,
    ICON_PALETTE_TABLE,
    FRONT_COORDS_TABLE,
    BACK_COORDS_TABLE,
    SPRITE_DATA,
)


def load_species():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data["species"]


def camel_name(display_name: str) -> str:
    return "".join(part.capitalize() for part in display_name.replace("-", " ").split())


def sprite_slot(mon) -> int:
    slots = {
        "SPECIES_RC_TURTLE_01": 1294,
        "SPECIES_RC_CAGLIARI_WILD_01": 1297,
    }
    try:
        return slots[mon["id"]]
    except KeyError as exc:
        raise ValueError(f"No sprite slot registered for {mon['id']}") from exc


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
    chunks = []
    for mon in species:
        symbol = mon["id"].replace("SPECIES_", "NAME_")
        chunks.extend([f"#org @{symbol}", mon["display_name"], ""])
    return "\n".join(chunks).rstrip() + "\n"


def render_sprite_registration(species):
    front = []
    back = []
    icons = []
    palettes = []
    shiny_palettes = []
    icon_palettes = []
    front_coords = []
    back_coords = []
    declarations = []

    for mon in species:
        slot = sprite_slot(mon)
        cname = camel_name(mon["display_name"])
        species_id = mon["id"]
        front_symbol = f"gFrontSprite{slot}RC{cname}"
        back_symbol = f"gBackShinySprite{slot}RC{cname}"
        icon_symbol = f"gIconSprite{slot}RC{cname}"

        front.append(
            f"\t[{species_id}] = {{{front_symbol}Tiles, (64 * 64) / 2, {species_id}}},"
        )
        back.append(
            f"\t[{species_id}] = {{{back_symbol}Tiles, (64 * 64) / 2, {species_id}}},"
        )
        icons.append(f"\t[{species_id}] = {icon_symbol}Tiles,")
        palettes.append(
            f"\t[{species_id}] = {{{front_symbol}Pal, {species_id}, 0x0}},"
        )
        shiny_palettes.append(
            f"\t[{species_id}] = {{{back_symbol}Pal, {species_id} + NUM_SPECIES, 0x0}},"
        )
        icon_palettes.append(f"\t[{species_id}] = 0x0,")
        front_coords.append(
            f"\t[{species_id}] =\n\t{{\n\t\t.size = 0x66,\n\t\t.y_offset = 0x6,\n\t}},"
        )
        back_coords.append(
            f"\t[{species_id}] =\n\t{{\n\t\t.size = 0x66,\n\t\t.y_offset = 0x5,\n\t}},"
        )
        declarations.extend(
            [
                f"extern const u8 {front_symbol}Tiles[];",
                f"extern const u8 {front_symbol}Pal[];",
                f"extern const u8 {back_symbol}Tiles[];",
                f"extern const u8 {back_symbol}Pal[];",
                f"extern const u8 {icon_symbol}Tiles[];",
            ]
        )

    return {
        "front_table": "\n".join(front) + "\n",
        "back_table": "\n".join(back) + "\n",
        "icon_table": "\n".join(icons) + "\n",
        "palette_table": "\n".join(palettes) + "\n",
        "shiny_palette_table": "\n".join(shiny_palettes) + "\n",
        "icon_palette_table": "\n".join(icon_palettes) + "\n",
        "front_coords": "\n".join(front_coords) + "\n",
        "back_coords": "\n".join(back_coords) + "\n",
        "sprite_data": "\n".join(declarations) + "\n",
    }


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


def patch_before_final_terminator(text: str, entry: str, marker: str) -> str:
    if marker in text:
        return text
    pos = text.rfind("\n};")
    if pos < 0:
        raise ValueError(f"Could not find final table terminator for {marker}")
    block = f"\n{marker}\n{entry.rstrip()}\n"
    return text[:pos] + block + text[pos:]


def patch_sprite_data(text: str, entry: str) -> str:
    if SPRITE_DATA_MARKER in text:
        return text
    return text.rstrip() + f"\n\n{SPRITE_DATA_MARKER}\n{entry.rstrip()}\n"


def patch_sprite_tables(species):
    registration = render_sprite_registration(species)
    patches = (
        (FRONT_TABLE, registration["front_table"], FRONT_TABLE_MARKER),
        (BACK_TABLE, registration["back_table"], BACK_TABLE_MARKER),
        (ICON_TABLE, registration["icon_table"], ICON_TABLE_MARKER),
        (PALETTE_TABLE, registration["palette_table"], PALETTE_TABLE_MARKER),
        (SHINY_PALETTE_TABLE, registration["shiny_palette_table"], SHINY_PALETTE_TABLE_MARKER),
        (ICON_PALETTE_TABLE, registration["icon_palette_table"], ICON_PALETTE_TABLE_MARKER),
        (FRONT_COORDS_TABLE, registration["front_coords"], FRONT_COORDS_MARKER),
        (BACK_COORDS_TABLE, registration["back_coords"], BACK_COORDS_MARKER),
    )
    for target, entry, marker in patches:
        target.write_text(
            patch_before_final_terminator(target.read_text(encoding="utf-8"), entry, marker),
            encoding="utf-8",
        )
    SPRITE_DATA.write_text(
        patch_sprite_data(SPRITE_DATA.read_text(encoding="utf-8"), registration["sprite_data"]),
        encoding="utf-8",
    )


def backup_targets():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for target in TARGETS:
        backup = BACKUP_DIR / target.relative_to(ROOT)
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(target, backup)


def restore_overlay():
    if not BACKUP_DIR.exists():
        return
    for target in TARGETS:
        backup = BACKUP_DIR / target.relative_to(ROOT)
        if backup.exists():
            shutil.copy2(backup, target)
    shutil.rmtree(BACKUP_DIR)
    print("Restored upstream DPE source files after Release Candidate overlay.")


def apply_overlay():
    species = load_species()
    backup_targets()
    try:
        BASE_STATS.write_text(
            patch_base_stats(BASE_STATS.read_text(encoding="utf-8"), species),
            encoding="utf-8",
        )
        LEARNSETS.write_text(
            patch_learnsets(LEARNSETS.read_text(encoding="utf-8"), species),
            encoding="utf-8",
        )
        NAMES.write_text(
            patch_names(NAMES.read_text(encoding="utf-8"), species),
            encoding="utf-8",
        )
        patch_sprite_tables(species)
    except Exception:
        restore_overlay()
        raise
    print(f"Applied Release Candidate overlay for {len(species)} species.")


def main():
    parser = argparse.ArgumentParser(
        description="Apply or restore source-controlled Release Candidate data overlays for DPE."
    )
    parser.add_argument("command", choices=("apply", "restore"), nargs="?", default="apply")
    args = parser.parse_args()
    if args.command == "restore":
        restore_overlay()
    else:
        apply_overlay()


if __name__ == "__main__":
    main()
