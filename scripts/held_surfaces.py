"""Registry surfaces that are live but HELD from the published skill.

The skill tree is generated from the backend registry, so a regeneration
publishes everything the registry declares, held work included (trap 1 in the
backend UPGRADE-LOG "API contract changes" section). `build_skill.py` runs the
canonical tree through `strip_tree` before it mirrors and packages it, and
`--check` fails while a held surface is still in the tree. The MCP does the
same in `src/held-surfaces.ts`.

When a hold lifts, delete its entry here and rebuild.

- API-074 `include=contacts` (the contact walk with `roles`, `min_confidence`,
  `max_duration` on 8 profile endpoints): legal gate open, not announced.
  `prism/creators` keeps its own contact options, as in the MCP.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HELD_CONTACT_WALK_ENDPOINTS = frozenset({
    "tiktok/profile",
    "instagram/profile",
    "instagram/profile/about",
    "youtube/channel/about",
    "twitter/profile",
    "facebook/profile",
    "linkbio/page",
    "pillar/page",
})
# Endpoints whose copy describes what a job item asking include=contacts carries.
HELD_COPY_ENDPOINTS = frozenset({"prism/jobs", "prism/jobs/{job_id}"})
HELD_PARAMS = frozenset({"roles", "min_confidence", "max_duration"})
HELD_TOKEN = "contacts"

# A sentence or line that describes the contact walk.
CONTACT_WALK = re.compile(
    r"include=contacts|`contacts`|contact walk|contact lookup|contact_lookup|"
    r"contact_status|contact_items|contact_retry|author\.ext\.contacts|"
    r"\"include\":\s*\"contacts\"|include: \"contacts\""
)
SECTION_HEADING = re.compile(r"^## (GET|POST|PUT|PATCH|DELETE) /v1/(\S+) - ", re.M)
SENTENCE_BREAK = re.compile(r"(?<=\.)\s+(?=[`A-Z])")
PARAM_LINE = re.compile(r"^- `([a-z_.]+)`")
INCLUDE_CONSTRAINT = re.compile(
    r"^- `include`: at most (\d+) comma-separated values; each value one of (.+)\.$"
)


def drop_held_sentences(text: str) -> str:
    """Drop every sentence of `text` that describes the contact walk."""
    if not CONTACT_WALK.search(text):
        return text
    # A field list ("Page-level: `data.contact_lookup`, `data.hydration`.")
    # loses the held field, not the whole list.
    text = re.sub(r"`data\.contact_lookup`, ", "", text)
    text = re.sub(r",? `data\.contact_lookup`(?=\.)", "", text)
    text = re.sub(r" ?Page-level:\.", "", text)
    kept = [s for s in SENTENCE_BREAK.split(text) if not CONTACT_WALK.search(s)]
    return " ".join(kept)


def _strip_held_section(body: str) -> str:
    lines = body.split("\n")
    include_values: list[str] | None = None
    out: list[str] = []
    for line in lines:
        m = INCLUDE_CONSTRAINT.match(line)
        if m:
            values = [v.strip() for v in m.group(2).split("|") if v.strip() != HELD_TOKEN]
            include_values = values
            if values:
                cap = min(int(m.group(1)), len(values))
                out.append(
                    f"- `include`: at most {cap} comma-separated values; each value one of {' | '.join(values)}."
                )
            continue
        p = PARAM_LINE.match(line)
        # Param lines and their constraint lines (`- \`roles\`: at most ...`).
        if p and p.group(1) in HELD_PARAMS:
            continue
        if line.startswith("|") and CONTACT_WALK.search(line):
            continue
        out.append(drop_held_sentences(line))

    result: list[str] = []
    for line in out:
        if line.startswith("- `include` (") and include_values == []:
            continue
        if line.startswith("- `include` (") and line.rstrip().endswith("- Comma list."):
            continue
        result.append(line)
    return "\n".join(result)


# Endpoints that keep their own contact options (not part of API-074).
UNTOUCHED_ENDPOINTS = frozenset({"prism/creators"})
WALK_FIELD_ROW = re.compile(r"^\| `(?:author\.ext\.contacts|data\.contact_lookup)")


def _strip_mentions(text: str) -> str:
    """Outside the held sections: drop rows about the walk's own fields, and
    every sentence (per table cell) that names the walk."""
    out = []
    for line in text.split("\n"):
        if not CONTACT_WALK.search(line):
            out.append(line)
        elif WALK_FIELD_ROW.match(line):
            continue
        elif line.startswith("|"):
            # Split on cell borders only: `string\|null` is one cell.
            cells = re.split(r"(?<!\\)\|", line)
            out.append("|".join(f" {drop_held_sentences(c.strip())} " if c.strip() else c for c in cells))
        else:
            out.append(drop_held_sentences(line))
    return "\n".join(out)


def strip_markdown(text: str) -> str:
    """Strip the contact walk from one markdown file of the tree."""
    matches = list(SECTION_HEADING.finditer(text))
    if not matches:
        return _strip_mentions(text)
    pieces = [_strip_mentions(text[: matches[0].start()])]
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[m.start():end]
        endpoint = m.group(2)
        if endpoint in HELD_CONTACT_WALK_ENDPOINTS:
            section = _strip_held_section(section)
        elif endpoint not in UNTOUCHED_ENDPOINTS:
            section = _strip_mentions(section)
        pieces.append(section)
    return "".join(pieces)


def strip_guide(text: str) -> str:
    """SKILL.md: a line about the walk goes; in a long `; `-joined line only its clauses go."""
    out = []
    for line in text.split("\n"):
        if not CONTACT_WALK.search(line):
            out.append(line)
            continue
        clauses = line.split("; ")
        if len(clauses) < 3 or CONTACT_WALK.search(clauses[0]):
            continue
        out.append("; ".join(c for c in clauses if not CONTACT_WALK.search(c)))
    return "\n".join(out)


def _slug(heading: str) -> str:
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def strip_recipes(text: str) -> tuple[str, set[str]]:
    """Remove every `## ` recipe built on a held surface; return the dropped anchors."""
    parts = re.split(r"(?m)^(?=## )", text)
    kept, dropped = [], set()
    for part in parts:
        if part.startswith("## ") and CONTACT_WALK.search(part):
            dropped.add(_slug(part.split("\n", 1)[0][3:]))
            continue
        kept.append(part)
    return drop_anchor_links("".join(kept), dropped), dropped


def drop_anchor_links(text: str, anchors: set[str]) -> str:
    if not anchors:
        return text
    pattern = re.compile("|".join(re.escape(f"#{a})") for a in sorted(anchors)))
    return "\n".join(l for l in text.split("\n") if not pattern.search(l))


def _strip_entry(e: dict) -> dict:
    """One catalogue endpoint without the held surface (a new dict)."""
    e = json.loads(json.dumps(e))
    if e.get("id") in HELD_COPY_ENDPOINTS:
        rule = e.get("cost", {}).get("rule")
        if rule:
            e["cost"]["rule"] = drop_held_sentences(rule)
        return e
    if e.get("id") not in HELD_CONTACT_WALK_ENDPOINTS:
        return e
    params = []
    for p in e.get("params", []):
        if p["name"] in HELD_PARAMS:
            continue
        enum = p.get("csv", {}).get("enum")
        if p["name"] == "include" and enum and HELD_TOKEN in enum:
            values = [v for v in enum if v != HELD_TOKEN]
            if not values:
                continue
            p = {**p, "csv": {**p["csv"], "enum": values, "max": min(p["csv"].get("max", len(values)), len(values))}}
        params.append(p)
    e["params"] = params
    rule = e.get("cost", {}).get("rule")
    if rule:
        e["cost"]["rule"] = drop_held_sentences(rule)
    return e


ENTRY_LINE = re.compile(r'^(\s*)(\{"id":.*\})(,?)$')


def strip_catalogue(raw: str) -> str:
    """assets/endpoints.json, one compact endpoint per line: only the lines of
    entries that change are rewritten, so the layout and every other byte stay."""
    out = []
    for line in raw.split("\n"):
        m = ENTRY_LINE.match(line)
        if m:
            entry = json.loads(m.group(2))
            stripped = _strip_entry(entry)
            if stripped != entry:
                line = m.group(1) + json.dumps(stripped, ensure_ascii=False, separators=(",", ":")) + m.group(3)
        out.append(line)
    return "\n".join(out)


def strip_tree(root: Path) -> list[str]:
    """Strip every held surface from a skill tree in place; return the files changed."""
    changed: list[str] = []

    def rewrite(path: Path, fn) -> None:
        if not path.is_file():
            return
        before = path.read_text(encoding="utf-8")
        after = fn(before)
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed.append(path.relative_to(root).as_posix())

    refs = root / "references"
    dropped: set[str] = set()

    def recipes(text: str) -> str:
        out, anchors = strip_recipes(text)
        dropped.update(anchors)
        return out

    rewrite(refs / "recipes.md", recipes)
    for path in sorted(refs.rglob("*.md")):
        if path.name == "recipes.md":
            continue
        rewrite(path, lambda t: drop_anchor_links(strip_markdown(t), dropped))
    rewrite(root / "SKILL.md", lambda t: drop_anchor_links(strip_guide(t), dropped))
    rewrite(root / "assets" / "endpoints.json", strip_catalogue)
    return changed
