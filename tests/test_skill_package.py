from __future__ import annotations

import json
import os
import py_compile
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".agents" / "skills" / "socialcrawl"
# The scripts' unit tests live beside their canonical source in the codebase
# repo (a sibling checkout); they are skipped when that checkout is absent.
SCRIPT_TESTS = (
    ROOT.parent
    / "codebase"
    / "packages"
    / "social-api"
    / "src"
    / "docs"
    / "skill-assets"
    / "tests"
)
SCRIPT_NAMES = ("sc.py", "paginate.py", "estimate.py", "batch.py", "to_csv.py")


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
            # Instagram dropped to 2 per URL; LinkedIn is the 5-credit worst case.
            "100 LinkedIn URLs hold 500 credits; 100 Instagram URLs hold 200",
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

    def test_skill_md_stays_cheap_to_load(self) -> None:
        skill = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")

        self.assertLessEqual(len(skill.rstrip("\n").splitlines()), 250)

        frontmatter = skill.split("---", 2)[1]
        lines = frontmatter.splitlines()
        start = next(i for i, l in enumerate(lines) if l.startswith("description:"))
        parts = []
        for line in lines[start + 1 :]:
            if not line.startswith(" "):
                break
            parts.append(line.strip())
        description = " ".join(parts)
        self.assertLessEqual(len(description), 1024)
        # Counts go stale (the old description said "27 platforms and 133 endpoints").
        self.assertNotRegex(description, r"\d[\d,+]*\s+(platforms|endpoints)")

    def test_downloadable_skill_carries_the_mit_license(self) -> None:
        root_license = (ROOT / "LICENSE").read_text(encoding="utf-8")
        with zipfile.ZipFile(ROOT / "socialcrawl.skill") as archive:
            packaged_license = archive.read("socialcrawl/LICENSE").decode("utf-8")

        self.assertEqual(packaged_license, root_license)


class BundledScriptTests(unittest.TestCase):
    """SK-05: the helper scripts and the offline catalogue ship in the skill."""

    def test_script_unit_tests_pass_when_present(self) -> None:
        if not SCRIPT_TESTS.is_dir():
            self.skipTest("codebase script tests are not checked out next to this repo")
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(SCRIPT_TESTS)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"script tests failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_bundled_scripts_compile_and_show_help_when_present(self) -> None:
        scripts = CANONICAL / "scripts"
        if not scripts.is_dir():
            self.skipTest("the skill tree has no scripts/ yet")
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1"}
        for name in SCRIPT_NAMES:
            with self.subTest(script=name):
                path = scripts / name
                self.assertTrue(path.is_file(), msg=f"{name} is missing")
                with tempfile.TemporaryDirectory() as tmp:
                    py_compile.compile(str(path), cfile=str(Path(tmp) / "x.pyc"), doraise=True)
                result = subprocess.run(
                    [sys.executable, str(path), "--help"],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_endpoint_catalogue_and_types_are_well_formed_when_present(self) -> None:
        assets = CANONICAL / "assets"
        if not assets.is_dir():
            self.skipTest("the skill tree has no assets/ yet")
        catalogue = json.loads((assets / "endpoints.json").read_text(encoding="utf-8"))
        self.assertEqual(catalogue["unit"], "credits")
        self.assertGreater(len(catalogue["endpoints"]), 100)
        for endpoint in catalogue["endpoints"][:50]:
            for key in ("id", "method", "params", "cost", "paging"):
                self.assertIn(key, endpoint)
            self.assertIn(endpoint["cost"]["model"], ("flat", "metered"))
        self.assertIn("export interface ApiResponse", (assets / "socialcrawl-types.ts").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            py_compile.compile(
                str(assets / "socialcrawl_types.py"), cfile=str(Path(tmp) / "t.pyc"), doraise=True
            )

    def test_scripts_never_print_the_key(self) -> None:
        scripts = CANONICAL / "scripts"
        if not scripts.is_dir():
            self.skipTest("the skill tree has no scripts/ yet")
        for name in SCRIPT_NAMES + ("sclib.py",):
            text = (scripts / name).read_text(encoding="utf-8")
            with self.subTest(script=name):
                self.assertNotIn("print(key", text)
                self.assertNotIn("echo $SOCIALCRAWL_API_KEY", text)


if __name__ == "__main__":
    unittest.main()
