#pragma once

/*
 * Release Candidate custom species live after the upstream DPE species range.
 * Keep these IDs append-only once they appear in a playable build or save.
 *
 * This header intentionally layers on top of upstream include/species.h so we
 * do not renumber or rewrite upstream species definitions.
 */

#define SPECIES_RC_TURTLE_01          (SPECIES_URSHIFU_RAPID_GIGA + 1)
#define SPECIES_RC_FROG_01            (SPECIES_RC_TURTLE_01 + 1)
#define SPECIES_RC_FIREFOX_01         (SPECIES_RC_FROG_01 + 1)
#define SPECIES_RC_CAGLIARI_WILD_01   (SPECIES_RC_FIREFOX_01 + 1)
#define SPECIES_RC_CAGLIARI_WILD_02   (SPECIES_RC_CAGLIARI_WILD_01 + 1)

/* Extend DPE table sizing without altering the upstream species.h file. */
#undef NUM_SPECIES
#define NUM_SPECIES (SPECIES_RC_CAGLIARI_WILD_02 + 1)
