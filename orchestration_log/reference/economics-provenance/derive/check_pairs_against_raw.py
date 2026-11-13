"""Find each Terminal-Bench cell of pairs.json in the raw Artificial Analysis page, near its variant's slug."""
import json
import re
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
PAIRS = json.loads((BUNDLE / "research/raw/extract-pairs-reach-appetite/pairs.json").read_text())["models"]
RAW = (BUNDLE / "research/raw/research-model-capability-and-effort/aa-claude-fable-5-1").read_text(errors="replace")
SUITE = "Terminal-Bench 4.0 [AA]"


def positions(text):
    return [match.start() for match in re.finditer(re.escape(text), RAW)]


absent = 0
for model, record in PAIRS.items():
    for effort in ("low", "high", "max"):
        pair = record["pairs"][effort]
        slug = re.search(r"slug=([a-z0-9\-]+)", pair["reach"][SUITE]["source"]).group(1)
        slug_positions = positions('"' + slug + '"') or positions(slug)
        found = []
        for name, section in (("score", "reach"), ("tokens", "tokens_generated"), ("dollars", "dollars")):
            value_positions = positions(repr(pair[section][SUITE]["value"]))
            if not value_positions:
                absent += 1
                found.append(name + ": ABSENT")
            else:
                nearest = min(abs(a - b) for a in value_positions for b in slug_positions)
                found.append(f"{name}: {len(value_positions)} occurrence(s), nearest to slug {nearest} characters")
        print(model, effort, slug, "|", "; ".join(found))
print("cells absent from the raw page:", absent)
