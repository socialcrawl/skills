"""Unit tests for scripts/held_surfaces.py (API-074 `include=contacts`)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import held_surfaces as hs  # noqa: E402


TIKTOK_SECTION = """## GET /v1/tiktok/profile - 1-3 credits (request-shaped)

Returns a TikTok profile. `include=contacts` runs the contact walk and fills author.ext.contacts. Counts are rounded.

**Pricing** 1 credit per call. `include=account` holds 2 more. `include=contacts` costs no extra credits, whatever the contact lookup answers. A call that fails costs nothing.

**Query params**

- `handle` (required) - The handle
- `include` (optional, string) - Comma list. `contacts` adds author.ext.contacts and data.contact_lookup, and runs the contact walk. `account` adds author.joined_at for 2 extra credits
- `max_duration` (optional, string) - Seconds the contact walk may run before answering, 3 to 20, default 12. Only with include=contacts
- `min_confidence` (optional, string) - 0 to 1, default 0.6
- `roles` (optional, string) - own, management, agency

**Constraints**

- `include`: at most 2 comma-separated values; each value one of contacts | account.
- `roles`: at most 3 comma-separated values; each value one of own | management | agency.
"""

TWITTER_SECTION = """## GET /v1/twitter/profile - 1 credit (standard)

Returns an X profile.

**Query params**

- `handle` (required) - The handle
- `include` (optional, string) - Comma list. `contacts` adds author.ext.contacts and data.contact_lookup, and runs the contact walk
- `min_confidence` (optional, string) - 0 to 1, default 0.6

**Constraints**

- `include`: at most 1 comma-separated values; each value one of contacts.

## GET /v1/twitter/search - 1 credit (standard)

Searches X. Has `include` too.
"""

CREATORS_SECTION = """## GET /v1/prism/creators - pay per search

- `include` (optional, string) - posts, contacts (the contact values). Either implies include=contacts.
"""


class SectionStripping(unittest.TestCase):
    def test_mixed_include_keeps_the_other_value(self) -> None:
        out = hs.strip_markdown(TIKTOK_SECTION)
        self.assertIn("- `include` (optional, string) - Comma list. `account` adds author.joined_at", out)
        self.assertIn("- `include`: at most 1 comma-separated values; each value one of account.", out)
        self.assertIn("`include=account` holds 2 more.", out)
        self.assertIn("A call that fails costs nothing.", out)
        self.assertIn("Counts are rounded.", out)
        for gone in ("max_duration", "min_confidence", "`roles`", "contact walk", "contact lookup", "include=contacts"):
            self.assertNotIn(gone, out)

    def test_contacts_only_include_is_removed_and_next_section_kept(self) -> None:
        out = hs.strip_markdown(TWITTER_SECTION)
        self.assertNotIn("`include`", out.split("## GET /v1/twitter/search")[0])
        self.assertNotIn("min_confidence", out)
        self.assertIn("## GET /v1/twitter/search - 1 credit (standard)\n\nSearches X. Has `include` too.", out)

    def test_endpoints_outside_the_hold_are_untouched(self) -> None:
        self.assertEqual(hs.strip_markdown(CREATORS_SECTION), CREATORS_SECTION)

    def test_cross_references_elsewhere_lose_only_the_walk_sentence(self) -> None:
        text = (
            "## GET /v1/youtube/channel - 1 credit (standard)\n\n"
            "- `contact_email` (optional, enum: 1) - Returns author.ext.contact_email. "
            "It is decided by the same role rules as include=contacts, so it is always an address include=contacts serves. "
            "No extra credits.\n"
        )
        out = hs.strip_markdown(text)
        self.assertIn("- `contact_email` (optional, enum: 1) - Returns author.ext.contact_email. No extra credits.", out)

    def test_schema_pages_lose_walk_rows_and_sentences(self) -> None:
        schema = (
            "| `author.ext.contact_email` | string | Opt-in. Same rules as `include=contacts`. Verbatim. |\n"
            "| `author.ext.contacts` | array | Filled by include=contacts. |\n"
            "| `author.ext.country` | string | Country. |\n"
        )
        out = hs.strip_markdown(schema)
        self.assertEqual(
            out,
            "| `author.ext.contact_email` | string | Opt-in. Verbatim. |\n| `author.ext.country` | string | Country. |\n",
        )

    def test_escaped_pipes_in_a_cell_survive(self) -> None:
        row = "| `author.ext.contact_email` | string\\|null | Opt-in. Same rules as `include=contacts`. Verbatim. |"
        self.assertEqual(
            hs.strip_markdown(row),
            "| `author.ext.contact_email` | string\\|null | Opt-in. Verbatim. |",
        )

    def test_page_level_list_loses_only_the_held_field(self) -> None:
        text = (
            "## GET /v1/tiktok/profile - 1-3 credits (request-shaped)\n\n"
            "+18 more (types in the full schema): `author` {url}. Page-level: `data.contact_lookup`, `data.hydration`.\n\n"
            "## GET /v1/twitter/profile - 1 credit (standard)\n\n"
            "+15 more (types in the full schema): `author` {url}. Page-level: `data.contact_lookup`.\n"
        )
        out = hs.strip_markdown(text)
        self.assertIn("`author` {url}. Page-level: `data.hydration`.\n", out)
        self.assertIn("+15 more (types in the full schema): `author` {url}.\n", out)

    def test_stripping_is_idempotent(self) -> None:
        once = hs.strip_markdown(TIKTOK_SECTION)
        self.assertEqual(hs.strip_markdown(once), once)


class GuideAndRecipes(unittest.TestCase):
    def test_guide_lines_about_the_walk_go(self) -> None:
        guide = "keep\n| A creator's contact email | `GET /v1/youtube/channel/about?include=contacts` |\nalso keep\n"
        self.assertEqual(hs.strip_guide(guide), "keep\nalso keep\n")

    def test_recipe_using_the_walk_is_removed_with_its_links(self) -> None:
        recipes = (
            "# Recipes\n\n- [Find a creator's email](#find-a-creators-email)\n- [Other](#other)\n\n"
            "## Find a creator's email\n\n1. `GET /v1/youtube/channel/about?include=contacts`\n\n"
            "## Other\n\nbody\n"
        )
        out, anchors = hs.strip_recipes(recipes)
        self.assertEqual(anchors, {"find-a-creators-email"})
        self.assertNotIn("creator's email", out)
        self.assertIn("## Other\n\nbody\n", out)
        self.assertIn("- [Other](#other)", out)
        index = "| Find a creator's email | [recipe](recipes.md#find-a-creators-email) |\n| x | y |\n"
        self.assertEqual(hs.drop_anchor_links(index, anchors), "| x | y |\n")


class Catalogue(unittest.TestCase):
    def test_catalogue_entry_loses_the_walk(self) -> None:
        catalogue = {
            "endpoints": [
                {
                    "id": "tiktok/profile", "method": "GET",
                    "params": [
                        {"name": "include", "csv": {"max": 2, "enum": ["contacts", "account"]}},
                        {"name": "max_duration"}, {"name": "min_confidence"}, {"name": "roles"},
                    ],
                    "cost": {"model": "metered", "rule": "1 credit. `include=contacts` costs no extra credits, whatever the contact lookup answers. Failures are free."},
                },
                {"id": "linkbio/page", "method": "GET", "params": [{"name": "include", "csv": {"max": 1, "enum": ["contacts"]}}], "cost": {"model": "flat"}},
                {"id": "prism/creators", "method": "GET", "params": [{"name": "include"}], "cost": {"model": "per_unit", "rule": "include=contacts is fine here."}},
            ]
        }
        # The generator's layout: one compact endpoint per line.
        rows = ",\n".join("    " + json.dumps(e, separators=(",", ":")) for e in catalogue["endpoints"])
        out = json.loads(hs.strip_catalogue('{\n  "endpoints": [\n' + rows + "\n  ]\n}\n"))
        tiktok, linkbio, creators = out["endpoints"]
        self.assertEqual(tiktok["params"], [{"name": "include", "csv": {"max": 1, "enum": ["account"]}}])
        self.assertEqual(tiktok["cost"]["rule"], "1 credit. Failures are free.")
        self.assertEqual(linkbio["params"], [])
        self.assertEqual(creators, catalogue["endpoints"][2])


class CatalogueLayout(unittest.TestCase):
    def test_one_endpoint_per_line_layout_is_kept(self) -> None:
        raw = (
            '{\n  "version": 1,\n  "endpoints": [\n'
            '    {"id":"a/b","method":"GET","params":[],"cost":{"model":"flat","min":1,"max":1}},\n'
            '    {"id":"twitter/profile","method":"GET","params":[{"name":"include","csv":{"max":1,"enum":["contacts"]}},{"name":"min_confidence"}],"cost":{"model":"flat","min":1,"max":1}}\n'
            "  ]\n}\n"
        )
        out = hs.strip_catalogue(raw)
        self.assertEqual(
            out,
            '{\n  "version": 1,\n  "endpoints": [\n'
            '    {"id":"a/b","method":"GET","params":[],"cost":{"model":"flat","min":1,"max":1}},\n'
            '    {"id":"twitter/profile","method":"GET","params":[],"cost":{"model":"flat","min":1,"max":1}}\n'
            "  ]\n}\n",
        )
        json.loads(out)


class ReleaseCheck(unittest.TestCase):
    def test_check_reports_a_tree_that_still_carries_a_held_surface(self) -> None:
        import tempfile

        import build_skill

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "references").mkdir()
            (root / "references" / "twitter.md").write_text(TWITTER_SECTION, encoding="utf-8")
            issues = build_skill.held_surface_issues(root)
            self.assertEqual(issues, ["references/twitter.md carries a held surface (scripts/held_surfaces.py)"])
            hs.strip_tree(root)
            self.assertEqual(build_skill.held_surface_issues(root), [])


if __name__ == "__main__":
    unittest.main()
