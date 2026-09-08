#!/usr/bin/env python3
"""Synchronise, package, and validate the public SocialCrawl skill."""

from __future__ import annotations

import argparse
import io
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".agents" / "skills" / "socialcrawl"
MIRRORS = (ROOT / "skills" / "socialcrawl", ROOT / "socialcrawl")
PACKAGE = ROOT / "socialcrawl.skill"
FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)

REQUIRED_FILES = (
    "LICENSE",
    "SKILL.md",
    "references/api-overview.md",
    "references/cost-gate.md",
    "references/pricing.md",
    "references/prism.md",
    # The two stateful families. Neither is a registry endpoint, so neither is
    # reachable from the generated platform tables - a reader who does not get
    # a reference file for them never learns they exist. `cohorts.md` was
    # missing from the bundle entirely until 08/09/2026.
    "references/monitors.md",
    "references/cohorts.md",
)

# The endpoints that can hold the most credits in one request, pinned by the
# RULE rather than by a heading spelling.
#
# The previous version of this table pinned heading strings like
# "## POST /v1/prism/post-stats - 1-500 credits (request-shaped)". Those were
# hand-written into a tree that is now generated from the endpoint registry, so
# the guard was asserting a wording no generator produces and would have failed
# on the first sync. What actually has to survive is the SUBSTANCE: that a
# reader meets the worst-case hold, not the per-row unit, before they call.
#
# post-stats / profiles / comment-lookup now carry a real span in the heading
# (a display-only PRICING descriptor was added upstream on 08/09/2026 for
# exactly this reason). batch-scrape and sessions cannot carry one - each
# shares its registry key with a free GET sibling - so for those two the rule
# rides the `**Pricing**` line directly under the heading instead.
# A batch endpoint's heading must state the shape of the charge, not a unit
# price that reads as the total. "(request-shaped)" is the wording the test
# suite pins; "(metered)" is the billing-engine word and means nothing to a
# reader pricing a call.
PRICING_INVARIANTS = {
    "references/prism.md": (
        "## POST /v1/prism/post-stats - 1-500 credits (request-shaped)",
        "## POST /v1/prism/profiles - 1-250 credits (request-shaped)",
        "## POST /v1/prism/comment-lookup - 2-100 credits (request-shaped)",
        "5 on Instagram and LinkedIn",
    ),
    "references/youtube.md": (
        "## POST /v1/youtube/transcripts - 3-300 credits (request-shaped)",
        "a full batch holds 300",
    ),
    "references/web.md": (
        "## POST /v1/web/batch-scrape - N credits for N submitted URLs (request-shaped)",
        "## POST /v1/web/sessions - 5-20 credits (request-shaped)",
        "**Pricing** 1 credit per URL submitted, held up front and refunded",
        "**Pricing** 20 credits per browser-hour, minimum 5.",
    ),
    "references/cost-gate.md": (
        "2 x 1 x 8 x 2 = 32 credits",
        "2 x 20 x 20 x 2 + 5 = 1,605",
    ),
    "references/pricing.md": (
        "`POST /v1/prism/post-stats` | 1-500 credits",
        "`POST /v1/prism/profiles` | 1-250 credits",
        "`POST /v1/prism/comment-lookup` | 2-100 credits",
        "`POST /v1/youtube/transcripts` | 3-300 credits",
        "1 credit per URL submitted",
        "20 credits per browser-hour, minimum 5",
    ),
}

BANNED_KEY_GUIDANCE = (
    'echo "$SOCIALCRAWL_API_KEY"',
    'echo "sc_xxxxx"',
    "use the resolved key directly in the curl command",
)


def tree_files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def package_bytes() -> bytes:
    payload = io.BytesIO()
    with zipfile.ZipFile(
        payload,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for relative, content in tree_files(CANONICAL).items():
            info = zipfile.ZipInfo(f"socialcrawl/{relative}", FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED)
    return payload.getvalue()


def safe_sync_destination(destination: Path) -> None:
    resolved_root = ROOT.resolve()
    resolved_destination = destination.resolve()
    if resolved_destination == CANONICAL.resolve():
        return
    if resolved_destination == resolved_root or resolved_root not in resolved_destination.parents:
        raise RuntimeError(f"Refusing to replace unsafe mirror path: {destination}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(CANONICAL, destination)


def build() -> None:
    for mirror in MIRRORS:
        safe_sync_destination(mirror)
    PACKAGE.write_bytes(package_bytes())


def validate_frontmatter(issues: list[str]) -> None:
    skill_path = CANONICAL / "SKILL.md"
    if not skill_path.is_file():
        issues.append("canonical SKILL.md is missing")
        return
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        issues.append("SKILL.md does not have valid YAML frontmatter fences")
        return
    frontmatter = text.split("---", 2)[1]
    if "name: socialcrawl" not in frontmatter:
        issues.append("SKILL.md frontmatter must preserve name: socialcrawl")
    if "description:" not in frontmatter:
        issues.append("SKILL.md frontmatter is missing a description")


def validate() -> list[str]:
    issues: list[str] = []
    root_license = ROOT / "LICENSE"
    if not root_license.is_file():
        issues.append("LICENSE is missing")

    for relative in REQUIRED_FILES:
        if not (CANONICAL / relative).is_file():
            issues.append(f"canonical skill is missing {relative}")

    validate_frontmatter(issues)
    packaged_license = CANONICAL / "LICENSE"
    if (
        root_license.is_file()
        and packaged_license.is_file()
        and packaged_license.read_bytes() != root_license.read_bytes()
    ):
        issues.append("packaged LICENSE differs from the repository LICENSE")
    canonical_files = tree_files(CANONICAL)
    for mirror in MIRRORS:
        if not mirror.is_dir():
            issues.append(f"mirror is missing: {mirror.relative_to(ROOT)}")
            continue
        mirror_files = tree_files(mirror)
        if mirror_files != canonical_files:
            issues.append(f"mirror differs from canonical: {mirror.relative_to(ROOT)}")

    expected_package = package_bytes()
    if not PACKAGE.is_file():
        issues.append("socialcrawl.skill is missing")
    elif PACKAGE.read_bytes() != expected_package:
        issues.append("socialcrawl.skill is stale; run python scripts/build_skill.py")

    for relative, fragments in PRICING_INVARIANTS.items():
        path = CANONICAL / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                issues.append(f"{relative} is missing pricing invariant: {fragment}")

    skill_text = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
    for fragment in BANNED_KEY_GUIDANCE:
        if fragment in skill_text:
            issues.append(f"SKILL.md contains secret-revealing guidance: {fragment}")
    if "Never print, paste, log, or return the key" not in skill_text:
        issues.append("SKILL.md is missing the API-key non-disclosure rule")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "npx skills update socialcrawl --yes" not in readme:
        issues.append("README is missing the documented update command")
    if "raw/main/socialcrawl.skill" not in readme:
        issues.append("README is missing the stable latest-package download link")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate without changing mirrors or the packaged artifact",
    )
    args = parser.parse_args()

    if not args.check:
        build()

    issues = validate()
    if issues:
        print("SocialCrawl skill validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print(
        "PASS: licence, frontmatter, pricing safeguards, mirrors, and package are current."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
