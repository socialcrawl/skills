"""The published skill covers every API contract change in the backend
UPGRADE-LOG through its sync cursor.

Each test pins one `API-NNN` row of the log's "API contract changes" table
by the registry fact it introduced (a path, a param, a field, a price), not
by a sentence, so a regeneration that rewords a description still passes and
one that drops the fact fails. Rows that change nothing an agent can read in
the skill (OpenAPI document shape, measured recall) are listed in
`NOT_SKILL_SURFACE` with the reason.

Held rows are the opposite contract: API-074 (`include=contacts`) is in the
registry but must not reach the published skill until its hold lifts.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".agents" / "skills" / "socialcrawl"
REFS = CANONICAL / "references"

SYNC_CURSOR = "API-105"

# Rows the skill has nothing to say about, with the reason.
NOT_SKILL_SURFACE = {
    "API-067": "the OpenAPI document's schema shape; the skill does not ship it",
    "API-076": "the OpenAPI document's schema shape; the skill does not ship it",
    "API-086": "measured recall (more rows from the same call); no contract to learn",
}


def read(relative: str) -> str:
    path = CANONICAL / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def ref(name: str) -> str:
    return read(f"references/{name}")


def section(method: str, endpoint: str) -> str:
    """One endpoint's section from its platform reference ('' when missing)."""
    platform = endpoint.split("/", 1)[0]
    text = ref(f"{platform}.md")
    heading = f"## {method} /v1/{endpoint} - "
    start = text.find(heading)
    if start == -1:
        return ""
    rest = text[start + len(heading):]
    nxt = re.search(r"\n## (?:GET|POST|PUT|PATCH|DELETE) /v1/", rest)
    return text[start:] if nxt is None else text[start:start + len(heading) + nxt.start()]


def heading(method: str, endpoint: str) -> str:
    return section(method, endpoint).split("\n", 1)[0]


def whole_skill_text() -> str:
    return "\n".join(
        p.read_text(encoding="utf-8")
        for p in sorted(CANONICAL.rglob("*"))
        if p.is_file() and p.suffix in (".md", ".json", ".ts", ".py")
    )


class SkillCase(unittest.TestCase):
    def assertSection(self, method: str, endpoint: str, *fragments: str) -> None:
        s = section(method, endpoint)
        self.assertTrue(s, f"no section for {method} /v1/{endpoint}")
        for fragment in fragments:
            with self.subTest(endpoint=endpoint, fragment=fragment):
                self.assertIn(fragment, s)


class RowWalksAndPaging(SkillCase):
    def test_api_048_walk_params_on_lists(self) -> None:
        for endpoint in ("reddit/search", "tiktok/profile/videos", "instagram/post/comments"):
            self.assertSection("GET", endpoint, "`max_items`", "`max_credits`", "`max_pages`")
        self.assertIn("`stopped`", ref("api-overview.md"))

    def test_api_049_search_max_pages_ceiling_is_50(self) -> None:
        for endpoint in ("tiktok/search", "youtube/search", "reddit/search", "threads/search"):
            self.assertSection("GET", endpoint, "`max_pages` (1-50)")

    def test_api_050_next_page_credits_and_typical_page_size(self) -> None:
        overview = ref("api-overview.md")
        self.assertIn("next_page_credits", overview)
        self.assertIn("typical_page_size", overview)

    def test_api_051_common_names_and_feed_alias(self) -> None:
        overview = ref("api-overview.md")
        self.assertRegex(overview, r"`sort`, `country`, `limit`, `since` and `until`")
        self.assertRegex(overview, r"profile/posts`?[^\n]*alias|alias[^\n]*profile/posts")


class NewEndpoints(SkillCase):
    def test_api_052_prism_post_comments(self) -> None:
        self.assertSection("POST", "prism/post-comments", "25")

    def test_api_062_prism_creators(self) -> None:
        self.assertSection("GET", "prism/creators", "`similar_to`", "`handles`")
        self.assertTrue(section("POST", "prism/creators"))

    def test_api_068_polymarket_search(self) -> None:
        self.assertTrue(section("GET", "polymarket/search"))

    def test_api_072_notifications_inbox(self) -> None:
        overview = ref("api-overview.md")
        self.assertIn("GET /v1/notifications", overview)
        self.assertIn("next_step", overview)

    def test_api_079_linkedin_endorsers_and_company_bulk(self) -> None:
        self.assertTrue(section("GET", "linkedin/profile/skills/endorsers"))
        self.assertTrue(
            section("POST", "linkedin/company/bulk") or section("GET", "linkedin/company/bulk")
        )

    def test_api_081_linkedin_profile_sections(self) -> None:
        for name in ("languages", "projects", "patents", "organizations", "courses", "test-scores", "featured"):
            with self.subTest(name=name):
                self.assertTrue(section("GET", f"linkedin/profile/{name}"))

    def test_api_092_six_new_platforms(self) -> None:
        expected = {"weibo": 8, "goodreads": 10, "airbnb": 4, "booking": 3, "duckduckgo": 7}
        for platform, count in expected.items():
            with self.subTest(platform=platform):
                text = ref(f"{platform}.md")
                self.assertTrue(text, f"references/{platform}.md is missing")
                self.assertEqual(
                    len(re.findall(r"^## (?:GET|POST) /v1/", text, flags=re.M)), count
                )
        for endpoint in ("bing/search", "bing/rank", "bing/videos", "bing/suggestions"):
            self.assertTrue(section("GET", endpoint), endpoint)
        index = ref("index.md")
        for platform in (*expected, "bing"):
            self.assertIn(f"({platform}.md)", index)

    def test_api_092_review_lanes_take_label(self) -> None:
        for endpoint in ("airbnb/listing/reviews", "goodreads/book/reviews"):
            if section("GET", endpoint):
                self.assertSection("GET", endpoint, "`label`")

    def test_api_093_producthunt_lanes(self) -> None:
        for endpoint in ("leaderboard", "product", "product/comments", "topic"):
            self.assertTrue(section("GET", f"producthunt/{endpoint}"), endpoint)

    def test_api_094_twitter_profile_about(self) -> None:
        self.assertSection("GET", "twitter/profile/about", "account_based_in")
        self.assertIn("2 credit", heading("GET", "twitter/profile/about"))

    def test_api_095_instagram_trending_searches(self) -> None:
        self.assertIn("5 credits", heading("GET", "instagram/trending/searches"))

    def test_api_096_ad_library_advertisers(self) -> None:
        for endpoint in ("facebook/adlibrary/advertiser", "google/adlibrary/advertiser"):
            self.assertIn("5 credits", heading("GET", endpoint), endpoint)


class SearchEverywhere(SkillCase):
    def test_api_053_window_and_limit(self) -> None:
        self.assertSection("GET", "search/everywhere", "`since`", "`until`", "`limit`")

    def test_api_069_urel1_params(self) -> None:
        self.assertSection(
            "GET", "search/everywhere",
            "`platforms`", "`exclude_platforms`", "`keywords`", "`context`",
            "`relevance_threshold`", "`max_per_platform`", "`period`", "`tz`",
            "`undated`", "`comments.per_post`", "`comments.replies`", "`authors.top`",
        )
        self.assertSection("GET", "youtube/search/advanced", "`exact_dates`")

    def test_api_073_post_runs_and_watermark(self) -> None:
        # `deadline_s` and `since_watermark` are GET-only; the POST is lists and watches.
        self.assertSection("GET", "search/everywhere", "`deadline_s`", "`since_watermark`")
        self.assertSection("POST", "search/everywhere", "`queries`", "`schedule`")
        self.assertIn("/v1/search/everywhere/runs", ref("search.md"))

    def test_api_077_lists_watches_more(self) -> None:
        text = ref("search.md")
        self.assertIn("`more`", text)
        self.assertRegex(text, r"[Ww]atch")

    def test_api_084_urel4_params_and_sources(self) -> None:
        self.assertSection(
            "GET", "search/everywhere",
            "`depth`", "`languages`", "`country`", "`unknown_language`", "`unknown_country`",
        )
        s = section("GET", "search/everywhere").lower()
        for source in ("bluesky", "quora"):
            self.assertIn(source, s)

    def test_api_085_sort_rows_newest_and_compact_cap(self) -> None:
        self.assertSection("GET", "facebook/search/posts", "`sort_rows`")
        self.assertIn("32,000", ref("search.md") + ref("api-overview.md"))

    def test_api_088_monitor_payload_has_no_internal_key(self) -> None:
        self.assertNotIn("__search_answer", whole_skill_text())

    def test_api_090_hashtag_sources_only_when_named(self) -> None:
        overview = ref("api-overview.md")
        self.assertRegex(overview, r"hashtag[^\n]*`sources`")

    def test_api_091_changes_url(self) -> None:
        self.assertIn("changes_url", ref("search.md") + ref("api-overview.md"))

    def test_overview_no_longer_says_seventeen_sources(self) -> None:
        self.assertNotIn("up to 17 sources", read("SKILL.md"))


class PrismDiscoverAndCreators(SkillCase):
    def test_api_064_066_discover_country(self) -> None:
        self.assertSection("GET", "prism/discover", "`country`")

    def test_api_065_exclude_lists(self) -> None:
        self.assertSection("GET", "prism/discover", "`exclude_list_id`")
        self.assertSection("POST", "prism/discover/inputs", "`exclude`")

    def test_api_082_creators_fill_to_limit(self) -> None:
        self.assertSection("GET", "prism/creators", "`limit`", "max_credits")

    def test_api_083_author_identity_and_key_hash(self) -> None:
        self.assertSection("GET", "prism/creators", "`author_identity`")
        self.assertIn("account_key_hash", ref("prism.md"))

    def test_api_087_prism_comments_takes_x_threads_linkedin(self) -> None:
        s = section("GET", "prism/comments")
        for platform in ("X", "Threads", "LinkedIn"):
            self.assertIn(platform, s)

    def test_api_089_recent_runs_export_newest_first(self) -> None:
        self.assertRegex(ref("prism.md") + ref("api-overview.md"), r"sort=recent[^\n]*newest first")

    def test_creators_and_discover_headings_are_not_a_ten_million_band(self) -> None:
        for method, endpoint in (
            ("GET", "prism/creators"), ("POST", "prism/creators"),
            ("GET", "prism/discover"), ("POST", "prism/discover"),
        ):
            h = heading(method, endpoint)
            self.assertTrue(h, endpoint)
            self.assertNotRegex(h, r"10,?000,?000")
            self.assertIn("max_credits", h)


class PlatformParamsAndFields(SkillCase):
    def test_api_054_reddit_search_limit_1000(self) -> None:
        self.assertSection("GET", "reddit/search", "1,000", "1 credit per 25 posts")

    def test_api_055_threads_low_balance(self) -> None:
        self.assertSection("GET", "threads/search", "expand=false")

    def test_api_056_event_links_are_full_urls(self) -> None:
        self.assertRegex(ref("api-overview.md"), r"`links`[^\n]*(full|absolute) URL")

    def test_api_057_instagram_hashtag_one_credit_page(self) -> None:
        h = heading("GET", "instagram/search/hashtag")
        self.assertRegex(h, r" - 1(-\d+)? credit")
        self.assertSection("GET", "instagram/search/hashtag", "`max_items`")

    def test_api_058_tiktok_search_expand(self) -> None:
        self.assertSection("GET", "tiktok/search", "`expand`")

    def test_api_059_tiktok_ads_top_retention(self) -> None:
        self.assertSection("GET", "tiktok/ads/top", "retention")

    def test_api_060_linkedin_company_include_about(self) -> None:
        self.assertSection("GET", "linkedin/company", "`include`", "about")
        self.assertIn("request-shaped", heading("GET", "linkedin/company"))

    def test_api_061_reels_region_ae_sa(self) -> None:
        self.assertSection("GET", "instagram/search/reels", "AE", "SA")

    def test_api_070_facebook_post_include_group(self) -> None:
        self.assertSection("GET", "facebook/post", "`include`", "group")

    def test_api_071_twitter_ai_search_async(self) -> None:
        self.assertSection("GET", "twitter/ai-search", "async", "prism/jobs")

    def test_api_075_linktree_links(self) -> None:
        self.assertSection("GET", "linktree/page", "links")

    def test_api_078_linkedin_mention_filters(self) -> None:
        self.assertSection("GET", "linkedin/search/posts", "`mentions_company`", "`mentions_member`")

    def test_api_080_tripadvisor_city_country(self) -> None:
        self.assertTrue(section("GET", "tripadvisor/search"))
        self.assertRegex(ref("tripadvisor.md"), r"`location`[^\n]*Paris, ?France")

    def test_api_097_facebook_ad_filters(self) -> None:
        self.assertSection(
            "GET", "facebook/adlibrary/company/ads",
            "`publisher_platforms`", "`ad_category`", "total_active_time",
        )

    def test_api_098_tiktok_ad_targeting(self) -> None:
        self.assertSection("GET", "tiktok/adlibrary/search", "`ages`", "`reach`", "`gender`")

    def test_api_099_linkedin_ad_payer(self) -> None:
        self.assertSection("GET", "linkedin/ad", "payer")

    def test_api_100_tiktok_exact_counts(self) -> None:
        for endpoint in ("tiktok/post", "tiktok/profile/videos", "tiktok/search"):
            self.assertSection("GET", endpoint, "exact_counts")

    def test_api_101_tiktok_profile_account(self) -> None:
        self.assertSection("GET", "tiktok/profile", "posting_region")
        self.assertIn("1-3 credits", heading("GET", "tiktok/profile"))

    def test_api_102_youtube_video_availability(self) -> None:
        self.assertSection("GET", "youtube/video", "playback_availability")

    def test_api_103_long_x_video_captions(self) -> None:
        self.assertRegex(section("GET", "twitter/tweet/transcript"), r"600")

    def test_api_104_raw_format_drops_source_billing_fields(self) -> None:
        raw = ref("api-overview.md").split("## Raw Format", 1)[-1].split("\n## ", 1)[0]
        self.assertIn("credits_charged", raw)

    def test_api_105_single_source_bad_input_is_free_400(self) -> None:
        self.assertRegex(ref("errors.md"), r"single-source[^\n]*400|400[^\n]*single-source")


class ListeningPublished(SkillCase):
    """API-063: the owner chose to publish Listening on 11/11/2026."""

    def test_listening_reference_and_routing(self) -> None:
        self.assertIn("/v1/listening/streams", ref("listening.md"))
        self.assertIn("references/listening.md", read("SKILL.md"))


class HeldSurfacesStayOut(SkillCase):
    """API-074 `include=contacts`: legal gate open, not announced."""

    HELD = (
        "include=contacts",
        "author.ext.contacts",
        "contact_lookup",
        "contact walk",
        "`min_confidence`",
        "`max_duration`",
        "\"contacts\"",
    )

    def test_no_contact_walk_anywhere_in_the_tree(self) -> None:
        for path in sorted(CANONICAL.rglob("*")):
            if not path.is_file() or path.suffix not in (".md", ".json", ".ts", ".py"):
                continue
            text = path.read_text(encoding="utf-8")
            if path.name == "prism.md":
                # prism/creators keeps its own contact options (not API-074).
                for method in ("GET", "POST"):
                    text = text.replace(section(method, "prism/creators"), "")
            if path.name == "endpoints.json":
                catalogue = json.loads(text)
                catalogue["endpoints"] = [e for e in catalogue["endpoints"] if e["id"] != "prism/creators"]
                text = json.dumps(catalogue)
            for fragment in self.HELD:
                with self.subTest(path=str(path.relative_to(CANONICAL)), fragment=fragment):
                    self.assertNotIn(fragment, text)

    def test_include_lists_no_longer_offer_contacts(self) -> None:
        for path in sorted(REFS.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"each value one of [^\n]*\bcontacts\b", path.name)

    def test_catalogue_has_no_contact_params(self) -> None:
        catalogue = json.loads(read("assets/endpoints.json"))
        for e in catalogue["endpoints"]:
            names = {p["name"] for p in e["params"]}
            with self.subTest(endpoint=e["id"]):
                self.assertFalse(names & {"min_confidence", "max_duration", "roles"} and e["id"] in {
                    "tiktok/profile", "instagram/profile", "instagram/profile/about",
                    "youtube/channel/about", "twitter/profile", "facebook/profile",
                    "linkbio/page", "pillar/page",
                })

    def test_unrelated_contact_features_survive(self) -> None:
        # Not part of the hold: the bio email picker and G2's website crawl.
        self.assertIn("contact_email", section("GET", "youtube/channel/about") or ref("youtube.md"))
        self.assertIn("website_contacts_crawl_mode", ref("g2.md"))
        self.assertTrue(section("GET", "tiktok/profile"))


class EveryEndpointIsCoveredAndPriced(SkillCase):
    def setUp(self) -> None:
        self.catalogue = json.loads(read("assets/endpoints.json"))["endpoints"]

    def test_index_totals_match_the_catalogue(self) -> None:
        m = re.search(r"\*\*(\d+) platforms, (\d+) endpoints\*\*", ref("index.md"))
        self.assertIsNotNone(m)
        platforms = {e["id"].split("/", 1)[0] for e in self.catalogue}
        self.assertEqual(int(m.group(2)), len(self.catalogue))
        self.assertEqual(int(m.group(1)), len(platforms))
        self.assertGreaterEqual(len(self.catalogue), 733)
        self.assertGreaterEqual(len(platforms), 75)

    def test_every_endpoint_has_a_section(self) -> None:
        missing = [
            f"{e['method']} {e['id']}" for e in self.catalogue
            if not section(e["method"], e["id"])
        ]
        self.assertEqual(missing, [])

    def test_every_endpoint_has_a_pricing_row(self) -> None:
        pricing = ref("pricing.md")
        missing = [
            f"{e['method']} {e['id']}" for e in self.catalogue
            if f"| `/v1/{e['id']}` | {e['method']} |" not in pricing
        ]
        self.assertEqual(missing, [])

    def test_every_catalogue_entry_carries_a_price(self) -> None:
        for e in self.catalogue:
            with self.subTest(endpoint=e["id"]):
                cost = e["cost"]
                self.assertIn(cost["model"], ("flat", "metered", "per_unit"))
                self.assertIsInstance(cost["min"], int)
                if cost["model"] == "per_unit":
                    # A per-unit price must name its unit and the rule.
                    self.assertTrue(cost.get("unit"))
                    self.assertTrue(cost.get("rule"))


class UpdatesReachTheUser(SkillCase):
    def test_stale_copy_offers_to_update_itself(self) -> None:
        skill = read("SKILL.md")
        freshness = skill.split("## Freshness Check", 1)[1].split("\n## ", 1)[0]
        self.assertIn("npx skills update socialcrawl --yes", freshness)
        # An agent with a shell offers to run it, and only on a yes.
        self.assertRegex(freshness, r"offer[^\n]*run[^\n]*yes")
        # A copy uploaded to claude.ai cannot be updated by a command.
        self.assertIn("raw/main/socialcrawl.skill", freshness)


class SyncCursorRecorded(SkillCase):
    def test_changelog_records_cursor_and_fingerprint(self) -> None:
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        newest = changelog.split("\n## ", 2)[1]
        self.assertIn(f"Upgrade-log cursor: {SYNC_CURSOR}", newest)
        fingerprint = re.search(r"registry_fingerprint: ([0-9a-f]{64})", read("SKILL.md"))
        self.assertIsNotNone(fingerprint)
        self.assertIn(fingerprint.group(1), newest)

    def test_readme_counts_match_the_index(self) -> None:
        m = re.search(r"\*\*(\d+) platforms, (\d+) endpoints\*\*", ref("index.md"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"Platforms-{m.group(1)}-", readme)
        self.assertIn(f"Endpoints-{m.group(2)}-", readme)
        self.assertIn(f"**Total: {m.group(2)} endpoints across {m.group(1)} platforms**", readme)

    def test_readme_platform_table_matches_the_index(self) -> None:
        index = {
            name.split(" (")[0]: int(count)
            for name, count in re.findall(r"^\| ([^|\[]+?) \| (\d+) \| [A-Z/]+ \| \[", ref("index.md"), flags=re.M)
        }
        readme = {
            name: int(count)
            for name, count in re.findall(
                r"^\| \*\*(.+?)\*\* \| (\d+) \|", (ROOT / "README.md").read_text(encoding="utf-8"), flags=re.M
            )
        }
        self.assertGreaterEqual(len(index), 75)
        self.assertEqual(readme, index)

    def test_readme_tier_counts_match_the_pricing_reference(self) -> None:
        pricing = ref("pricing.md")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for tier, label in (("standard", "Standard"), ("advanced", "Advanced"), ("premium", "Premium")):
            count = re.search(rf"^\| {tier} \| [^|]+ \| (\d+) \|", pricing, flags=re.M).group(1)
            with self.subTest(tier=tier):
                self.assertRegex(readme, rf"\| \*\*{label}\*\* \| [^|]+ \| {count} \|")
        self.assertNotIn("walks up to 5 pages", readme)
        self.assertNotIn("17 sources across 14 platforms", readme)


if __name__ == "__main__":
    unittest.main()
