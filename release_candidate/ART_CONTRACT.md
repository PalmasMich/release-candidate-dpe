# Release Candidate Preview Art Contract

This document defines the battle-art contract for original Preview species before the binary ROM build is available.

## First starter: Tartrek

Species ID: `SPECIES_RC_TURTLE_01`

Required source assets:

- `graphics/frontspr/gFrontSprite1268RCTartrek.png`
- `graphics/backspr/gBackShinySprite1268RCTartrek.png`
- `graphics/pokeicon/gIconSprite1268RCTartrek.png`

`1268` is the decimal value of the first Release Candidate species slot (`0x4F4`) immediately after upstream `SPECIES_URSHIFU_RAPID_GIGA` (`0x4F3`). The numeric prefix is part of the DPE asset-ordering convention and must remain aligned with the stable species ID.

Expected generated symbols:

- `gFrontSprite1268RCTartrekTiles`
- `gBackShinySprite1268RCTartrekTiles`
- `gIconSprite1268RCTartrekTiles`

The sprite-table overlay must register those symbols at `SPECIES_RC_TURTLE_01` in:

- `src/Front_Pic_Table.c`
- `src/Back_Pic_Table.c`
- `src/Icon_Table.c`
- required coordinate and palette tables
- `include/sprite_data.h` declarations

## Visual constraints

- Front/back battle art: authored for the existing DPE 64×64 battle-sprite pipeline.
- Icon: authored for the existing DPE party/icon pipeline.
- Indexed palette and transparency must match DPE/Grit expectations.
- Design identity: turtle/wanderer, Grass/Ground, sturdy rather than fast.
- Do not copy Pokémon, Unbound, or third-party fan-project artwork.
- `Tartrek` is the current working display name; changing the displayed name before Preview 0.1 does not change the stable species ID or asset slot.

## Next slots

The contiguous Preview slots are:

- `0x4F4` / 1268 — `SPECIES_RC_TURTLE_01`
- `0x4F5` / 1269 — `SPECIES_RC_FROG_01`
- `0x4F6` / 1270 — `SPECIES_RC_FIREFOX_01`
- `0x4F7` / 1271 — `SPECIES_RC_CAGLIARI_WILD_01`
- `0x4F8` / 1272 — `SPECIES_RC_CAGLIARI_WILD_02`

Once a species appears in a distributed playable build/save, its numeric slot is append-only and must not be recycled.
