from __future__ import annotations

import subprocess
import sys
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".agents" / "skills" / "socialcrawl"


class SkillPackageTests(unittest.TestCase):
    def test_repository_passes_the_release_check(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_skill.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"release check failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_cost_gate_names_request_shaped_formulas(self) -> None:
        cost_gate = (CANONICAL / "references" / "cost-gate.md").read_text(
            encoding="utf-8"
        )

        required_fragments = (
            "`POST /v1/prism/post-stats`",
            "1 to 5 credits per successful URL",
            "100 Instagram or LinkedIn URLs",
            "500 credits",
            "`GET /v1/prism/ai-visibility`",
            "2 x prompts x runs x engines",
            "2 x 1 x 8 x 2 = 32 credits",
            "`POST /v1/prism/profiles`",
            "`POST /v1/prism/comment-lookup`",
            "`POST /v1/youtube/transcripts`",
            "`POST /v1/web/batch-scrape`",
            "`POST /v1/web/sessions`",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, cost_gate)

    def test_headings_do_not_present_batch_unit_prices_as_totals(self) -> None:
        references = CANONICAL / "references"
        prism = (references / "prism.md").read_text(encoding="utf-8")
        youtube = (references / "youtube.md").read_text(encoding="utf-8")
        web = (references / "web.md").read_text(encoding="utf-8")

        self.assertIn(
            "## POST /v1/prism/post-stats - 1-500 credits (request-shaped)",
            prism,
        )
        self.assertIn(
            "## POST /v1/prism/profiles - 1-250 credits (request-shaped)",
            prism,
        )
        self.assertIn(
            "## POST /v1/prism/comment-lookup - 2-100 credits (request-shaped)",
            prism,
        )
        self.assertIn(
            "## POST /v1/youtube/transcripts - 3-300 credits (request-shaped)",
            youtube,
        )
        self.assertIn(
            "## POST /v1/web/batch-scrape - N credits for N submitted URLs (request-shaped)",
            web,
        )
        self.assertIn(
            "## POST /v1/web/sessions - 5-20 credits (request-shaped)",
            web,
        )

    def test_overviews_do_not_repeat_the_obsolete_fifty_credit_ceiling(self) -> None:
        paths = (
            CANONICAL / "SKILL.md",
            CANONICAL / "references" / "api-overview.md",
            CANONICAL / "references" / "pricing.md",
            CANONICAL / "references" / "prism.md",
            ROOT / "README.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for obsolete in (
                "varies (0-50)",
                "per recipe (0-50",
                "per recipe (0–50",
            ):
                with self.subTest(path=path.name, obsolete=obsolete):
                    self.assertNotIn(obsolete, text)

    def test_skill_never_instructs_agents_to_print_or_inline_the_key(self) -> None:
        skill = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")

        banned = (
            'echo "$SOCIALCRAWL_API_KEY"',
            'echo "sc_xxxxx"',
            "use the resolved key directly in the curl command",
        )
        for fragment in banned:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, skill)

        self.assertIn("Never print, paste, log, or return the key", skill)

    def test_downloadable_skill_carries_the_mit_license(self) -> None:
        root_license = (ROOT / "LICENSE").read_text(encoding="utf-8")
        with zipfile.ZipFile(ROOT / "socialcrawl.skill") as archive:
            packaged_license = archive.read("socialcrawl/LICENSE").decode("utf-8")

        self.assertEqual(packaged_license, root_license)


if __name__ == "__main__":
    unittest.main()
