# Release Candidate — Starter Art Contract v0.2

This contract separates technically valid bootstrap graphics from reviewed production art. The generated sprites keep private builds reproducible, but they are not approved final assets.

## Stable asset slots

| Species | Stable ID | Decimal asset prefix | Required generated symbols |
| --- | ---: | ---: | --- |
| Tartrek / `SPECIES_RC_TURTLE_01` | `0x050E` | 1294 | `gFrontSprite1294RCTartrekTiles`, `gBackShinySprite1294RCTartrekTiles`, `gIconSprite1294RCTartrekTiles` |
| Frobyte / `SPECIES_RC_FROG_01` | `0x050F` | 1295 | `gFrontSprite1295RCFrobyteTiles`, `gBackShinySprite1295RCFrobyteTiles`, `gIconSprite1295RCFrobyteTiles` |
| Emberfox / `SPECIES_RC_FIREFOX_01` | `0x0510` | 1296 | `gFrontSprite1296RCEmberfoxTiles`, `gBackShinySprite1296RCEmberfoxTiles`, `gIconSprite1296RCEmberfoxTiles` |
| Mistrillo / `SPECIES_RC_CAGLIARI_WILD_01` | `0x0511` | 1297 | `gFrontSprite1297RCMistrilloTiles`, `gBackShinySprite1297RCMistrilloTiles`, `gIconSprite1297RCMistrilloTiles` |

These IDs are save-facing and append-only. Art replacement must not renumber them.

## Required files per species

- `graphics/frontspr/gFrontSprite<slot><name>.png` — 64×64 indexed battle front;
- `graphics/backspr/gBackShinySprite<slot><name>.png` — 64×64 indexed back sheet used by the current DPE pipeline;
- `graphics/pokeicon/gIconSprite<slot><name>.png` — 32×64 two-frame indexed icon;
- normal, shiny, and icon palette registrations;
- front and back coordinate registrations.

PNG inputs must use 4-bit indexed colour, palette index 0 as transparency, and no more than 16 palette entries.

## Mandatory production sequence

1. approved concept as a north star;
2. silhouette review at native size;
3. authored front pose;
4. authored back pose;
5. reduced-palette review;
6. icon review;
7. GBA integration and runtime smoke.

Do not raster-convert a rich concept and call the result final. Front, back, and icon must be deliberately redrawn for their native dimensions.

The machine-readable state lives in `release_candidate/starter_art_manifest.json`. Validate it with:

```bash
python scripts/validate_rc_art_pipeline.py
```

That command currently reports `RC_STARTER_ART_STATUS=BOOTSTRAP`. The release approval gate is deliberately stricter:

```bash
python scripts/validate_rc_art_pipeline.py --require-approved
```

It must remain blocked until all seven stages for all three starters are `approved` and contain review evidence.

## Current generator status

`scripts/generate_rc_sprite_assets.py` produces original, deterministic placeholder graphics for private technical builds. Those files prove dimensions, indexing, symbols, table integration, and palette transport only. They do not satisfy silhouette, pose, palette, or final-art approval.

No Nintendo, Pokémon, Unbound, or third-party fan-project artwork may be copied or traced.
