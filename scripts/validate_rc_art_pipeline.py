#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "release_candidate" / "starter_art_manifest.json"
EXPECTED_SLOTS = {
    "SPECIES_RC_TURTLE_01": ("Tartrek", "0x050E", 1294),
    "SPECIES_RC_FROG_01": ("Frobyte", "0x050F", 1295),
    "SPECIES_RC_FIREFOX_01": ("Emberfox", "0x0510", 1296),
}
EXPECTED_STAGES = (
    "concept_north_star",
    "silhouette",
    "front_pose",
    "back_pose",
    "reduced_palette",
    "icon",
    "gba_integration",
)
ALLOWED_STATUSES = {"pending", "bootstrap", "approved"}


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(manifest: dict) -> list[str]:
    errors = []
    policy = manifest.get("policy", {})
    if policy.get("required_stage_order") != list(EXPECTED_STAGES):
        errors.append("required stage order does not match the V0.2 production pipeline")
    if policy.get("generated_bootstrap_assets_are_not_final") is not True:
        errors.append("bootstrap assets must be explicitly non-final")

    starters = manifest.get("starters", [])
    by_id = {item.get("species_id"): item for item in starters}
    if set(by_id) != set(EXPECTED_SLOTS):
        errors.append("starter species set does not match the stable RC contract")

    for species_id, (name, slot_hex, slot_decimal) in EXPECTED_SLOTS.items():
        item = by_id.get(species_id)
        if item is None:
            continue
        if (item.get("display_name"), item.get("slot_hex"), item.get("slot_decimal")) != (
            name,
            slot_hex,
            slot_decimal,
        ):
            errors.append(f"{species_id}: display name or stable asset slot changed")
        stages = item.get("stages", {})
        if tuple(stages) != EXPECTED_STAGES:
            errors.append(f"{species_id}: stages are missing or out of order")
        invalid = {status for status in stages.values() if status not in ALLOWED_STATUSES}
        if invalid:
            errors.append(f"{species_id}: invalid stage statuses {sorted(invalid)}")
        if item.get("production_ready"):
            if any(status != "approved" for status in stages.values()):
                errors.append(f"{species_id}: production_ready requires every stage approved")
            if not item.get("review_evidence"):
                errors.append(f"{species_id}: production_ready requires review evidence")
    return errors


def overall_status(manifest: dict) -> str:
    starters = manifest.get("starters", [])
    if starters and all(item.get("production_ready") for item in starters):
        return "APPROVED"
    if any("bootstrap" in item.get("stages", {}).values() for item in starters):
        return "BOOTSTRAP"
    return "IN_PROGRESS"


def run(path: Path = DEFAULT_MANIFEST, *, require_approved: bool = False) -> int:
    manifest = load_manifest(path)
    errors = validate(manifest)
    for error in errors:
        print(f"RC_STARTER_ART_ERROR={error}")
    if errors:
        print("RC_STARTER_ART_STATUS=INVALID")
        return 1

    status = overall_status(manifest)
    print(f"RC_STARTER_ART_STATUS={status}")
    if require_approved and status != "APPROVED":
        print("RC_STARTER_ART_APPROVAL=BLOCKED")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the V0.2 starter art production pipeline.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()
    return run(args.manifest, require_approved=args.require_approved)


if __name__ == "__main__":
    raise SystemExit(main())
