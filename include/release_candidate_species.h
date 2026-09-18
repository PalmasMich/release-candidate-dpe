#pragma once

/*
 * Release Candidate custom species live after the upstream DPE species range.
 * Keep these IDs append-only once they appear in a playable build or save.
 *
 * This header intentionally layers on top of upstream include/species.h so we
 * do not renumber or rewrite upstream species definitions.
 */

/*
 * Reserve IDs after CFRU's complete species range (which ends at 0x50D).
 * DPE's upstream range ends earlier, so using its immediate next ID would
 * collide with CFRU-only species such as G-Max/PLA forms.
 */
#define SPECIES_RC_TURTLE_01          0x50E
#define SPECIES_RC_FROG_01            0x50F
#define SPECIES_RC_FIREFOX_01         0x510
#define SPECIES_RC_CAGLIARI_WILD_01   0x511
#define SPECIES_RC_CAGLIARI_WILD_02   0x512

/* Extend DPE table sizing without altering the upstream species.h file. */
#undef NUM_SPECIES
#define NUM_SPECIES (SPECIES_RC_CAGLIARI_WILD_02 + 1)
