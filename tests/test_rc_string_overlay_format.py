from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_release_candidate_overlay.py"

spec = importlib.util.spec_from_file_location("rc_overlay", SCRIPT)
rc_overlay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc_overlay)


def test_rendered_name_overlay_uses_only_supported_hash_directives():
    rendered = rc_overlay.render_names(rc_overlay.load_species())
    for line in rendered.splitlines():
        if line.startswith("#"):
            assert line.startswith("#org "), f"unsupported string directive/comment: {line}"
