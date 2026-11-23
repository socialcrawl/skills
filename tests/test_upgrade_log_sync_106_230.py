"""The published skill covers the backend UPGRADE-LOG contract rows API-106
to API-230 (12/11/2026 to 23/11/2026).

Same contract as `test_upgrade_log_sync.py`: each test pins one `API-NNN` row
by the fact it introduced (a path, a param, a field, a price, an error
reason), never by a sentence. Rows that change nothing an agent sends, reads
or pays for (a timeout budget, a ranking pass, a retry count) are listed in
`NOT_SKILL_SURFACE` with the reason, so every id in the range is accounted
for by exactly one of the two.
"""

from __future__ import annotations

import json
import re
import unittest

from test_upgrade_log_sync import CANONICAL, SkillCase, heading, read, ref, section


# Rows the skill has nothing to teach: same request, same price, same fields;
# only how long a source is waited on, how often it is retried, or which
# error class an already-documented failure lands in.
NOT_SKILL_SURFACE = {
    "API-107": "replies that came back empty now arrive; same params, price and cursor",
    "API-110": "same `engagement.views` field; a backup source now agrees with the main one",
    "API-135": "a timeout budget restored on TikTok Ad Library search; nothing to send differently",
    "API-136": "a timeout reported as the 504 it is; retry guidance is unchanged",
    "API-137": "a missing account answers the documented free 404; nothing to send differently",
    "API-138": "the 503 keeps its code and refund; only the Retry-After value changed, which errors.md already says to honour",
    "API-139": "an all-timeout answer is a 504 instead of a 502; both are refunded and retried the same way",
    "API-140": "a source's timeout budget, about 5 s longer",
    "API-150": "same params and 5 credits a page; faster pages and case-exact skill matching",
    "API-154": "a later page's timeout budget",
    "API-155": "cursors became portable between sources; an issued cursor still works",
    "API-163": "fewer unrelated rows on a two-word query; no param or price change",
    "API-167": "the wording of one `empty_reason_note`",
    "API-171": "an empty page is checked once; the documented 404 and empty answers are unchanged",
    "API-174": "an internal ranking pass; nothing dropped, price unchanged",
    "API-200": "exact counts where rounded ones were served; same fields",
    "API-202": "`instagram/similar` names fill correctly; the withdrawn Yelp lane leaves the bundle",
    "API-214": "an empty first page answers sooner; same response",
}

FIRST, LAST = 106, 230


def contract_tests() -> set[str]:
    """Every API-NNN that has a test method in this module."""
    ids: set[str] = set()
    for obj in globals().values():
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            for name in dir(obj):
                for m in re.finditer(r"api_((?:\d{3}_?)+)", name):
                    for n in re.findall(r"\d{3}", m.group(1)):
                        ids.add(f"API-{n}")
    return ids


def skill_text(*names: str) -> str:
    return "\n".join(ref(n) for n in names)


class EveryRowIsAccountedFor(unittest.TestCase):
    def test_each_id_is_tested_or_excused(self) -> None:
        tested = contract_tests()
        missing = [
            f"API-{n}" for n in range(FIRST, LAST + 1)
            if f"API-{n}" not in tested and f"API-{n}" not in NOT_SKILL_SURFACE
        ]
        self.assertEqual(missing, [])

    def test_no_id_is_both_tested_and_excused(self) -> None:
        self.assertEqual(sorted(contract_tests() & set(NOT_SKILL_SURFACE)), [])


class Pricing(SkillCase):
    def test_api_106_include_joins_cost_one_more(self) -> None:
        for endpoint in ("tiktok/post", "tiktok/profile", "youtube/video"):
            self.assertIn(" - 1-2 credits", heading("GET", endpoint), endpoint)

    def test_api_161_ads_top_include_total(self) -> None:
        self.assertIn("10-400 credits", heading("GET", "tiktok/ads/top"))
        self.assertSection("GET", "tiktok/ads/top", "total")

    def test_api_162_threads_coverage_full(self) -> None:
        self.assertSection("GET", "threads/search", "`coverage`", "full")
        self.assertRegex(section("GET", "threads/search"), r"3 credits? (a|per) post")

    def test_api_187_yelp_reviews_limit_and_page_price(self) -> None:
        self.assertIn(" - 1-", heading("GET", "yelp/business/reviews"))
        self.assertSection("GET", "yelp/business/reviews", "`limit`", "`not_recommended`")

    def test_api_197_203_facebook_profile_details_costs_nothing_extra(self) -> None:
        self.assertIn(" - 1 credit", heading("GET", "facebook/profile"))
        self.assertSection("GET", "facebook/profile", "details")

    def test_api_197_instagram_hashtag_include_engagement(self) -> None:
        self.assertSection("GET", "instagram/search/hashtag", "engagement")
        self.assertIn("1-61 credits", heading("GET", "instagram/search/hashtag"))

    def test_api_213_youtube_include_channel(self) -> None:
        overview = skill_text("youtube.md")
        self.assertIn("include=channel", overview.replace("`include` = `channel`", "include=channel"))


class NewEndpoints(SkillCase):
    def test_api_141_facebook_group_events(self) -> None:
        self.assertSection("GET", "facebook/group/events", "`group_id`", "`cursor`", "details")
        self.assertIn("1-9 credits", heading("GET", "facebook/group/events"))

    def test_api_147_google_business_reviews(self) -> None:
        self.assertSection(
            "GET", "google/business/reviews",
            "`place_id`", "`cid`", "`depth`", "`sort`", "`query`", "`language`", "`since`",
        )

    def test_api_148_google_reviews_history_job(self) -> None:
        self.assertSection("POST", "google/business/reviews/history", "`depth`", "job_id")
        self.assertIn("/v1/google/business/reviews/history/{job_id}", ref("google.md"))

    def test_api_149_settled_history_page_carries_job(self) -> None:
        self.assertIn("data.job", skill_text("google.md", "trustpilot.md", "api-overview.md"))

    def test_api_170_github_search_repos(self) -> None:
        self.assertSection("GET", "github/search/repos", "`sort`")
        self.assertIn(" - 1 credit", heading("GET", "github/search/repos"))

    def test_api_188_yelp_history_and_bulk_reviews(self) -> None:
        self.assertTrue(section("POST", "yelp/business/reviews/history"))
        self.assertSection("POST", "prism/reviews/bulk", "refresh_of")
        prism = ref("prism.md")
        self.assertIn("/v1/prism/reviews/bulk/{job_id}", prism)
        self.assertRegex(prism, r"/v1/prism/reviews/bulk/\{job_id\}/cancel|DELETE /v1/prism/reviews/bulk/\{job_id\}")

    def test_api_191_new_google_endpoints(self) -> None:
        for endpoint in (
            "business/contributor-reviews", "business/popular-times", "business/photos",
            "business/menu", "images", "patents", "ai-overview", "autocomplete",
        ):
            self.assertTrue(section("GET", f"google/{endpoint}"), endpoint)

    def test_api_192_twenty_new_platforms(self) -> None:
        index = ref("index.md")
        for platform in (
            "zillow", "redfin", "realtor", "apartments", "homes", "apple_maps", "yahoo",
            "yandex", "baidu", "ikea", "kroger", "sprouts", "idealo", "bestbuy", "steam",
            "stackoverflow", "wikipedia", "npm", "pypi", "soundcloud",
        ):
            with self.subTest(platform=platform):
                self.assertTrue(ref(f"{platform}.md"), f"references/{platform}.md is missing")
                self.assertIn(f"({platform}.md)", index)

    def test_api_193_job_boards(self) -> None:
        for board in ("greenhouse", "lever", "ashby", "workday", "google", "levels", "indeed"):
            self.assertTrue(section("GET", f"jobs/{board}/search"), board)

    def test_api_194_more_new_endpoints(self) -> None:
        for endpoint in (
            "bing/images", "bing/shopping/search", "bing/shopping/product", "booking/hotel/rooms",
            "amazon/search/suggestions", "hackernews/stories", "pinterest/profile",
            "spotify/playlist", "bluesky/user/followers",
        ):
            self.assertTrue(section("GET", endpoint), endpoint)
        self.assertSection("GET", "bluesky/user/posts", "`filter`", "`cursor`")

    def test_api_195_youtube_channel_lanes(self) -> None:
        for endpoint in ("channel/search", "channel/podcasts", "channel/lives", "channel/playlists"):
            self.assertTrue(section("GET", f"youtube/{endpoint}"), endpoint)
        self.assertSection("GET", "youtube/channel/videos", "oldest")
        self.assertSection("GET", "youtube/search", "`features`")

    def test_api_220_telegram_post_comments(self) -> None:
        self.assertSection("GET", "telegram/post/comments", "`url`", "`cursor`", "comments_disabled")
        self.assertIn(" - 1 credit", heading("GET", "telegram/post/comments"))


class NewParams(SkillCase):
    def test_api_159_yelp_reviews_sort(self) -> None:
        self.assertSection(
            "GET", "yelp/business/reviews", "`sort`", "newest", "oldest", "highest_rated", "lowest_rated",
        )

    def test_api_160_219_yelp_takes_slug(self) -> None:
        for endpoint in ("yelp/business/reviews", "yelp/business/info"):
            # Yelp calls the name slug the business "alias".
            self.assertRegex(section("GET", endpoint), r"\balias\b[^\n]*(URL|prince-street)", endpoint)

    def test_api_173_search_everywhere_lookback_days(self) -> None:
        self.assertSection("GET", "search/everywhere", "`lookback_days`")

    def test_api_177_trustpilot_reviews_url(self) -> None:
        self.assertSection("GET", "trustpilot/reviews", "`url`", "`domain`")

    def test_api_185_creators_brief(self) -> None:
        self.assertSection("GET", "prism/creators", "`brief`")

    def test_api_189_yelp_info_fields_and_search_bbox(self) -> None:
        self.assertSection("GET", "yelp/search", "`bbox`")

    def test_api_190_tripadvisor_depth_500(self) -> None:
        for lane in ("reviews", "restaurant/reviews", "attraction/reviews", "cruise/reviews"):
            self.assertSection("GET", f"tripadvisor/{lane}", "`depth`")
        self.assertIn("500", section("GET", "tripadvisor/reviews"))

    def test_api_196_finance_history_intervals(self) -> None:
        self.assertSection("GET", "finance/history", "`interval`", "1wk", "1mo")

    def test_api_204_relevant_to_on_naver_kin_and_reddit_comments(self) -> None:
        for endpoint in ("naver/kin/search", "reddit/search/comments"):
            self.assertSection("GET", endpoint, "`relevant_to`")

    def test_api_206_g2_depth_and_product_index_query(self) -> None:
        self.assertSection("GET", "g2/reviews", "`depth`")
        self.assertSection("GET", "g2/product-index", "`query`")

    def test_api_208_web_scrape_accept_language(self) -> None:
        self.assertSection("GET", "web/scrape", "`accept_language`")

    def test_api_210_client_tag(self) -> None:
        text = skill_text("api-overview.md") + read("SKILL.md")
        self.assertIn("x-client-tag", text)
        self.assertIn("group_by=tag", text)
        self.assertIn("X-Client-Tag-Ignored", text)

    def test_api_212_redfin_include_details(self) -> None:
        redfin = ref("redfin.md")
        self.assertIn("details", redfin)
        self.assertRegex(redfin, r"`include`")

    def test_api_215_tweet_replies_newest_first(self) -> None:
        self.assertSection("GET", "twitter/tweet/replies", "latest", "`since_id`")

    def test_api_217_tavily_domains_json_list(self) -> None:
        self.assertRegex(section("GET", "tavily/search"), r"JSON (list|array)")


class ResponseFields(SkillCase):
    def test_api_108_instagram_post_media_urls(self) -> None:
        self.assertIn("media_urls", ref("instagram.md"))

    def test_api_109_crosspost_counts(self) -> None:
        self.assertIn("facebook_likes", ref("instagram.md"))

    def test_api_115_inline_comment_geo(self) -> None:
        self.assertIn("post_country", ref("prism.md"))

    def test_api_116_comment_country(self) -> None:
        text = skill_text("api-overview.md") + read("references/schemas/Comment.md")
        self.assertIn("computed.country", text)

    def test_api_119_monitor_status_fields(self) -> None:
        monitors = ref("monitors.md")
        for field in ("paused_because", "consecutive_skips", "webhook_failing", "legs_billed_separately", "runs_until_cap"):
            self.assertIn(field, monitors)

    def test_api_142_event_location(self) -> None:
        self.assertIn("location_type", ref("facebook.md"))
        self.assertIn("location_id", ref("facebook.md"))

    def test_api_164_165_x_article_rows(self) -> None:
        self.assertIn("article_url", ref("twitter.md"))
        self.assertIn("reposts_excluded", ref("twitter.md"))

    def test_api_166_reddit_thread_post(self) -> None:
        self.assertSection("GET", "reddit/post/comments", "data.post")

    def test_api_168_github_issue_state(self) -> None:
        github = ref("github.md")
        for field in ("state_reason", "merged_at", "closed_at"):
            self.assertIn(field, github)

    def test_api_169_github_repo_stats(self) -> None:
        github = ref("github.md")
        for field in ("stars", "forks", "open_issues", "pushed_at", "programming_language"):
            self.assertIn(field, github)

    def test_api_175_ad_search_rows_canonical(self) -> None:
        self.assertSection("GET", "facebook/adlibrary/search/ads", "post.ext.ad")

    def test_api_180_181_youtube_comments_disabled(self) -> None:
        self.assertSection("GET", "youtube/video/comments", "comments_disabled")
        self.assertSection("GET", "youtube/video", "comments_disabled")

    def test_api_184_creators_estimate_capped(self) -> None:
        self.assertIn("capped_by_max_credits", ref("prism.md"))

    def test_api_198_review_responses(self) -> None:
        self.assertIn("responses", section("GET", "google_play/app-reviews"))

    def test_api_199_review_ext_yelp(self) -> None:
        self.assertIn("review.ext.yelp", ref("yelp.md"))

    def test_api_201_marketplace_currency(self) -> None:
        self.assertIn("currency", section("GET", "facebook/marketplace/search"))

    def test_api_205_estimate_hold_semantics(self) -> None:
        text = skill_text("utility.md", "cost-gate.md")
        self.assertIn("upfront_hold", text)
        self.assertIn("quote_basis", text)
        self.assertIn("credits_ceiling", text)

    def test_api_207_store_status(self) -> None:
        self.assertIn("store_status", skill_text("prism.md", "app_store.md", "google_play.md"))

    def test_api_208_page_state(self) -> None:
        self.assertIn("page_state", ref("web.md"))

    def test_api_212_highlight_owner(self) -> None:
        self.assertTrue(section("GET", "instagram/highlight/detail"))
        self.assertIn("walmart", ref("index.md"))

    def test_api_218_finance_bars_and_bing_sponsored(self) -> None:
        self.assertIn("exchange", section("GET", "finance/history"))
        self.assertIn("sponsored_results", section("GET", "bing/search"))

    def test_api_222_facebook_comment_media(self) -> None:
        facebook = ref("facebook.md")
        self.assertIn("author_profile_token", facebook)
        self.assertIn("comment.ext.media", facebook)

    def test_api_223_commenter_display_name(self) -> None:
        self.assertIn("commenters", section("GET", "prism/discover"))

    def test_api_228_discover_run_normalized(self) -> None:
        self.assertIn("normalized", ref("prism.md") + ref("api-overview.md"))


class Behaviour(SkillCase):
    def test_api_111_reddit_comments_take_t3_ids(self) -> None:
        self.assertIn("t3_", section("GET", "reddit/post/comments"))

    def test_api_112_113_discover_input_routes(self) -> None:
        text = ref("prism.md") + ref("api-overview.md")
        self.assertIn("/v1/prism/discover/inputs/{id}/entries", text)
        self.assertIn("exclude_list_full", text)
        self.assertIn("input_not_found", text)
        self.assertIn("input_limit", text)
        self.assertRegex(text, r"DELETE /v1/prism/discover/inputs/\{id\}")
        self.assertRegex(text, r"GET /v1/prism/discover/inputs\b")

    def test_api_114_117_google_news_windows(self) -> None:
        self.assertSection("GET", "google_news/search", "`from`", "`to`", "`language_code`")

    def test_api_118_monthly_cap(self) -> None:
        monitors = ref("monitors.md")
        self.assertIn("max_credits_per_month", monitors)
        self.assertIn("monthly_cap", monitors)

    def test_api_120_email_digest(self) -> None:
        self.assertIn("email_digest", ref("monitors.md"))

    def test_api_121_export_shape_rows(self) -> None:
        self.assertIn("shape=rows", ref("monitors.md"))

    def test_api_122_hourly_minute(self) -> None:
        self.assertRegex(ref("monitors.md"), r"[Hh]ourly[^\n]*minute|minute[^\n]*hourly")

    def test_api_123_run_retention_30_days(self) -> None:
        text = ref("search.md") + ref("prism.md")
        self.assertIn("retention_days", text)
        self.assertRegex(text, r"30 days")

    def test_api_124_monitor_quote_sources_on_top(self) -> None:
        self.assertRegex(ref("monitors.md"), r"billed (on top|separately)")

    def test_api_125_133_age_restricted(self) -> None:
        for endpoint in ("facebook/group/posts", "threads/user/posts"):
            self.assertRegex(section("GET", endpoint), r"age[- ]restricted|age limit", endpoint)

    def test_api_126_channel_popular_sort(self) -> None:
        self.assertIn("sort=latest", section("GET", "youtube/channel/videos"))

    def test_api_127_ad_cursor_expired(self) -> None:
        self.assertRegex(section("GET", "facebook/adlibrary/company/ads"), r"cursor[^\n]*expire")

    def test_api_128_157_web_not_found_reasons(self) -> None:
        web = ref("web.md") + ref("errors.md")
        self.assertIn("site_not_supported", web)
        self.assertIn("url_unreachable", web)

    def test_api_129_session_execute_errors(self) -> None:
        self.assertSection("POST", "web/sessions/{session_id}/execute", "`code`")
        self.assertRegex(section("POST", "web/sessions/{session_id}/execute"), r"no longer active|expired")

    def test_api_130_131_152_search_end_of_walk(self) -> None:
        self.assertRegex(section("GET", "facebook/search/posts") + ref("errors.md"), r"facebook/search/posts[^\n]*10 minutes")
        self.assertIn("not_found_unconfirmed", section("GET", "tiktok/search") + ref("errors.md"))

    def test_api_132_usage_read_timeout(self) -> None:
        self.assertRegex(ref("api-overview.md"), r"credits/usage[\s\S]{0,1500}(shorter range|api_key_id)")

    def test_api_134_live_profile_timeout(self) -> None:
        self.assertIn("profile_lookup_timeout", section("GET", "tiktok/user/live") + ref("errors.md"))

    def test_api_143_hashtag_recent_is_relevance(self) -> None:
        self.assertRegex(section("GET", "instagram/search/hashtag"), r"[Rr]ecent")

    def test_api_144_most_viewed_reels(self) -> None:
        self.assertSection("GET", "instagram/profile/reels", "most_viewed")

    def test_api_145_breaker_open(self) -> None:
        self.assertIn("breaker_open", ref("errors.md") + ref("api-overview.md"))

    def test_api_146_reels_search_later_pages(self) -> None:
        self.assertSection("GET", "instagram/search/reels", "`cursor`")

    def test_api_151_job_items_resume(self) -> None:
        self.assertIn("resumes", ref("prism.md"))

    def test_api_153_comment_lookup_retry(self) -> None:
        self.assertRegex(section("GET", "instagram/comment"), r"Retry-After|503")

    def test_api_156_ai_search_handle_filters(self) -> None:
        self.assertSection("GET", "twitter/ai-search", "`from_handles`", "`exclude_handles`")

    def test_api_158_google_redirect_links(self) -> None:
        self.assertRegex(ref("web.md"), r"google\.<tld>/url|[Gg]oogle redirect")

    def test_api_172_everywhere_partial(self) -> None:
        self.assertIn("partial", section("GET", "search/everywhere"))

    def test_api_176_resolve_ad_library_and_maps(self) -> None:
        utility = ref("utility.md")
        self.assertRegex(utility, r"Ad Library")
        self.assertRegex(utility, r"Google Maps")

    def test_api_178_estimate_dashed_ids(self) -> None:
        self.assertRegex(ref("utility.md"), r"dash")

    def test_api_179_tiktok_comment_total_counts_replies(self) -> None:
        self.assertIn("tiktok/video/comment/replies", ref("tiktok.md"))

    def test_api_182_instagram_post_stats_pointer(self) -> None:
        self.assertIn("instagram/post/stats", section("GET", "instagram/post"))

    def test_api_183_monitor_dry_run_refusal(self) -> None:
        monitors = ref("monitors.md")
        self.assertIn("would_be_refused", monitors)
        self.assertIn("MONITOR_LIMIT_REACHED", monitors + ref("errors.md"))

    def test_api_186_plan_account_watch(self) -> None:
        self.assertIn("account_watch", ref("utility.md") + read("SKILL.md"))

    def test_api_209_errors_and_aliases(self) -> None:
        self.assertIn("no_matches", section("GET", "google/search"))
        self.assertSection("GET", "naver/brief", "`relevant_to`")
        self.assertRegex(ref("errors.md") + ref("api-overview.md"), r"429[^\n]*error\.details")

    def test_api_211_job_walk_ceiling(self) -> None:
        self.assertIn("credits_max", ref("prism.md"))

    def test_api_216_youtube_video_wrong_link(self) -> None:
        self.assertRegex(section("GET", "youtube/video"), r"11")

    def test_api_221_telegram_comment_lane(self) -> None:
        self.assertRegex(section("POST", "prism/profiles") + section("GET", "prism/profiles"), r"[Tt]elegram")

    def test_api_203_504_retry_after(self) -> None:
        self.assertRegex(ref("errors.md"), r"504[^\n]*Retry-After")

    def test_api_224_targets_country(self) -> None:
        self.assertIn("targets_country", ref("prism.md"))

    def test_api_225_region_defaults(self) -> None:
        self.assertIn("region_defaults", ref("prism.md"))

    def test_api_226_discover_per_platform_limit(self) -> None:
        self.assertRegex(section("GET", "prism/discover"), r"min\(25")

    def test_api_227_linkedin_accounts_search(self) -> None:
        self.assertIn("search_in", section("GET", "prism/discover") + section("POST", "prism/discover"))

    def test_api_229_new_accounts_schedule(self) -> None:
        self.assertIn("new_accounts", ref("prism.md") + ref("api-overview.md"))

    def test_api_230_did_you_mean_on_unknown_routes(self) -> None:
        self.assertIn("did_you_mean", ref("errors.md") + ref("api-overview.md"))


class CatalogueCarriesNewEndpoints(SkillCase):
    def test_catalogue_grew_to_the_current_registry(self) -> None:
        catalogue = json.loads(read("assets/endpoints.json"))["endpoints"]
        ids = {e["id"] for e in catalogue}
        for endpoint in ("telegram/post/comments", "github/search/repos", "prism/reviews/bulk", "zillow/search"):
            self.assertIn(endpoint, ids)


if __name__ == "__main__":
    unittest.main()
