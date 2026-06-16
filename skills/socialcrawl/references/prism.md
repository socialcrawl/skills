# Prism — composite recipes

Prism endpoints are **server-side composites**: one call fans out to several of the underlying detail endpoints, runs them in parallel, and folds the legs into a single unified payload behind the standard response envelope. They turn what would be a dozen chained `/v1/{platform}/{resource}` calls into one billable request with one consistent shape.

**30 cross-platform recipes live under `/v1/prism/*`.** A handful of composites keep their platform's own path (and carry a `family: "prism"` flag) — those are documented in their platform's reference file:

- `/v1/{tiktok,instagram,youtube,facebook,twitter,linkedin}/profile/full` — a profile-360 (profile + recent posts + computed analytics), 5 credits. See the per-platform reference files.
- `/v1/reddit/omni-search` — Reddit voice-of-customer sweep. See [reddit.md](reddit.md).
- `/v1/naver/brief` — one query across 6 Naver corpora. See [naver.md](naver.md).
- `/v1/search/forums` — fused forum search. See [search.md](search.md).

All endpoints below are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

## How Prism composites behave

- **`legs[]` transparency.** Every composite response carries a `legs[]` array — one entry per upstream call `{endpoint, status, credits_used, latency_ms, error}` — so you can see exactly what ran.
- **Degrade, don't fail.** Most legs degrade to empty/null when their upstream misses; usually only one "critical" leg (the profile, the search, the first page) can fail the whole call. A critical-leg failure → full refund.
- **Coverage-floor refunds.** Multi-source composites refund automatically when a strict majority of legs fail: `0 < coverage < 0.5` → 50% refund; all legs fail (`ok:false`) → full refund. You never pay full price when most of the fan-out failed.
- **Three cost modes** (see [pricing.md](pricing.md) for the per-endpoint table):
  - **Flat** — a fixed price (e.g. `reputation` 30cr), refunded on failure/low coverage.
  - **Param-derived flat** — the validated request shape sets the price up front, no metering (e.g. `app-reviews` 15cr both stores / 10cr single; `creator-card` 5cr ≤4 platforms +1cr/extra).
  - **Metered ("deduct-ceiling → refund-to-actual")** — cost scales with runtime work; the router deducts a query-derived ceiling and refunds the unused units (e.g. `comments`, `post-stats`, `org-radar`, `creator-vet`, `ai-visibility`).
- **SSE streaming.** `comments`, `video-intel`, `app-reviews`, `post-stats`, and `answers` stream when you send `Accept: text/event-stream` — a `result`/`leg` chunk per unit as it settles, then a terminal `done{credits_used}`. `answers` always streams.
- **Pricing note:** Prism composites are premium-priced (0–50 credits). **Always tell the user the credit cost before executing a Prism call.** After the call, report `credits_used` and `credits_remaining`, and surface `legs[]`/coverage when a refund happened.

---

## Universal helpers

### GET /v1/prism/lookup — 0 credits (resolves to the underlying endpoint's cost)

Universal URL dispatcher: any social/commerce URL → the right detail endpoint's unified response. No surcharge — you pay the resolved endpoint's normal cost.

- `url` (required) — Absolute http(s) URL of the post / profile / product to resolve.
- `include` (optional) — CSV of optional flags forwarded verbatim to the resolved endpoint (e.g. `trim`).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/lookup?url=https://www.youtube.com/watch?v=A9TikdsD5eg"
```

### GET /v1/prism/comments — metered, 1cr/page, min 2 credits

Every comment on a post, replies nested, server-paginated to completion. SSE-capable.

- `url` (required) — Absolute http(s) URL of the post whose comments to harvest.
- `max` (optional, integer) — Stop after roughly this many top-level comments (1–5000, default 1000); whole pages return so the count can slightly exceed this.
- `replies` (optional, boolean) — Expand replies where the platform supports it (default true; TikTok/YouTube/Facebook).
- `cursor` (optional) — Opaque composite cursor from a prior response's `next_cursor` to resume.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/comments?url=https://www.youtube.com/watch?v=A9TikdsD5eg"
```

### POST /v1/prism/post-stats — metered, 1 credit per successful URL

Bulk URL stats refresh for verification loops (e.g. clipper payouts) — up to 100 mixed-platform post URLs → one engagement row per URL. **The only POST endpoint.** Failed/unsupported URLs are refunded; net charge = count of `status:"ok"` rows. SSE-capable; never cached.

- `urls` (required) — JSON array of 1–100 absolute http(s) post URLs (mixed platforms allowed).
- `include` (optional) — CSV subset of `views,likes,comments,shares,saves` to trim each row's engagement block.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -X POST "https://www.socialcrawl.dev/v1/prism/post-stats" \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://www.youtube.com/watch?v=A9TikdsD5eg"]}'
```

---

## Profiles, creators & audiences

### GET /v1/prism/creator-card — 5 credits (≤4 platforms; +1cr per extra platform)

One handle → unified author cards across N platforms (`cards{}` + `found_on` + `totals`). A handle missing on a platform returns `null` (that's the answer, not a failure); only an all-platform miss refunds.

- `handle` (required) — Looked up across every requested platform (a single leading `@` is stripped).
- `platforms` (optional) — CSV of `tiktok,instagram,youtube,twitter,threads,bluesky,truthsocial` (default first four).
- `include` (optional) — CSV subset of `cards,totals`.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/creator-card?handle=mrbeast"
```

### GET /v1/prism/creator-vet — metered 50 credits (75 with `cross_platform`)

Vet a creator before partnering — engagement quality, commenter authenticity, posting cadence, and controversy signals. Core profile leg is critical (not found → full refund).

- `handle` (required) — The creator handle to vet.
- `platform` (optional) — Primary platform (`tiktok`/`youtube`/`instagram`).
- `depth` (optional) — Set `deep` to widen the post + commenter sample.
- `include` (optional) — Set `cross_platform` to add the universal presence leg (+25cr, refunded if it fails).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/creator-vet?handle=mkbhd"
```

### GET /v1/prism/voice — 5 credits

One person's public posts across X + Threads + Bluesky + Truth Social, time-merged. Microblogs the handle isn't on return empty + `platform_presence:false`; all-miss → full refund.

- `handle` (required) — Looked up across all four microblogs (a single leading `@` is stripped).
- `platforms` (optional) — CSV subset of `twitter,threads,bluesky,truthsocial`.
- `cursor` (optional) — Opaque per-platform token from `cursors_by_platform`.
- `include` (optional) — CSV subset of `posts_by_platform,merged_timeline,computed`.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/voice?handle=nasa"
```

### GET /v1/prism/audience-overlap — 20 credits

Two TikTok creators → the deterministic overlap of their commenter audiences (Jaccard, shared-fan count, a/b-only counts, a `confidence` label). **TikTok-only in v1.** If either creator can't be fetched → full refund.

- `handle_a` (required) — First TikTok creator handle.
- `handle_b` (required) — Second TikTok creator handle.
- `platform` (optional) — `tiktok` only in v1.
- `videos_per_creator` (optional, integer) — Recent videos sampled per creator (1–10, default 5).
- `depth` (optional) — Set `deep` to widen the shared-fan sample.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/audience-overlap?handle_a=mkbhd&handle_b=mrwhosetheboss"
```

### GET /v1/prism/video-intel — 5 credits (+10cr with `transcript`, refunded when null)

One video URL → detail + stats + top comments + optional transcript + ≤3 commenter profiles, across YouTube / TikTok / Rumble / Instagram. Only the detail leg is critical. SSE when `include=transcript`.

- `url` (required) — Absolute http(s) URL of a YouTube, TikTok, Rumble, or Instagram video.
- `comments` (optional) — How many top comments (0–50, default 20; `0` skips).
- `include` (optional) — CSV of `transcript` (+10cr, refunded when null) and/or `commenter_profiles` (TikTok/Instagram in v1).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/video-intel?url=https://www.youtube.com/watch?v=A9TikdsD5eg&include=transcript"
```

---

## Brand, reputation & market

### GET /v1/prism/brand-mentions — 20 credits

Brand mention volume time-series, sentiment split, top sources, and recent mentions for one keyword. `include=digest` adds an LLM narrative.

- `keyword` (required) — Brand or term (wrap in quotes for exact phrase).
- `date_from` (required) — Window start (YYYY-MM-DD).
- `date_to` (optional) — Window end (defaults to latest crawl).
- `date_group` (optional, enum day|week|month) — Trend bucket (default day).
- `page_type` (optional, enum ecommerce|news|blogs|message-boards|organization) — Surface filter.
- `include` (optional) — Set `digest` for an LLM summary.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/brand-mentions?keyword=socialcrawl&date_from=2026-05-01"
```

### GET /v1/prism/reputation — 30 credits

A brand's cross-source reputation — Trustpilot + app stores + Google Business + web sentiment blended into one weighted score (company vs product axes) with themed pros/cons.

- `brand` (required) — Brand/business/domain to assess.
- `sources` (optional) — CSV subset of `trustpilot,google_play,app_store,google,tripadvisor,web`.
- `country` (optional) — Marketplace/locale (default United States).
- `depth` (optional, integer) — Reviews per source (Trustpilot clamped ≤20).
- `place` (optional) — Enable place-based legs (Google Business + TripAdvisor).
- `axis` (optional, enum company|product|both) — Which axis to headline (default both).
- `app_store_id` / `google_play_id` (optional) — Anchor an app axis directly.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/reputation?brand=Notion"
```

### GET /v1/prism/review-integrity — 30 credits

A deterministic (no-LLM) cross-source review-integrity verdict: rating divergence, distribution bimodality, forum-tone contrast, spam-domain clustering → an A–F grade with per-signal evidence.

- One of `query` / `asin` / `gid` is required (`gid` = `product.ext.gid`, NOT the catalog id).
- `sources` (optional) — CSV subset of `amazon,google_shopping,trustpilot,web,forums`.
- `country` (optional) — Marketplace country (default United States).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/review-integrity?query=sony wh-1000xm5"
```

### GET /v1/prism/product-reviews — 30 credits

A product's reviews across Amazon + Google Shopping + Trustpilot → a cross-marketplace rating + themed pros/cons report with per-topic rating impact. Commerce legs are slow (20–60s).

- One of `query` / `asin` / `gid` is required (`gid` = `product.ext.gid`, NOT the catalog id).
- `sources` (optional) — CSV subset of `amazon,google_shopping,trustpilot`.
- `country` (optional) — Marketplace country.
- `depth` (optional, integer) — Reviews per source (Trustpilot ≤20).
- `competitors` (optional) — Optional competitor products.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/product-reviews?query=airpods pro 2"
```

### GET /v1/prism/earned-media — 20 credits

A brand's earned-media footprint — news + tech-press + fresh-web clips, deduped and ranked, with an outlet-coverage rollup and optional competitor gap. `include=digest` adds an LLM narrative.

- `brand` (required) — Brand/company to map.
- `competitor` (optional) — For a share-of-coverage gap.
- `date_from` / `date_to` (optional) — Window (YYYY-MM-DD).
- `min_domain_rank` (optional, integer) — Drop clips below this domain authority.
- `include` (optional) — Set `digest` for an LLM narrative.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/earned-media?brand=Vercel"
```

### GET /v1/prism/share-of-voice — metered 40 credits (20 web-only)

Engagement-weighted Share of Voice across 2–5 brands — web + social split, emotion overlay, true-share-of-category, and ESOV. Drop `social` for the cheaper web-only variant.

- `brands` (required) — 2–5 competitor brand names (CSV).
- `category_code` (optional) — Numeric DFS taxonomy code for true-share-of-category.
- `market_shares` (optional) — JSON map of real market share per brand for ESOV.
- `include` (optional) — CSV toggles (default `emotions,social`).
- `page_type` (optional, enum) — Surface filter.
- `date_from` / `date_to` (optional) — Window (defaults: 90 days ago → today).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/share-of-voice?brands=notion,coda,airtable"
```

### GET /v1/prism/demand-signals — 30 credits

A consumer-demand nowcast fusing app-review velocity + web-mention slope + Reddit velocity + Amazon review level into a published, deterministic demand index (every weight/anchor/window disclosed). Honest one-shot v1 — true deltas need a monitor.

- `keyword` (required) — Brand/product to nowcast.
- `google_play_id` / `app_store_id` (optional) — Enable the app-review axis.
- `signals` (optional) — CSV subset of `app_reviews,mentions,reddit,commerce`.
- `amazon_query` / `country` / `date_from` / `date_to` / `depth` (optional).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/demand-signals?keyword=spotify"
```

### GET /v1/prism/campaign — 35 credits

A hashtag/phrase campaign tracker: pre/during/post volume lift + cross-platform engagement rollup + ranked top amplifiers.

- One of `hashtag` / `phrase` is required.
- `window_start` (required) — Launch date (YYYY-MM-DD) — the pre/during boundary.
- `window_end` (optional) — End date (default today).
- `pre_days` (optional, integer, default 14) / `post_days` (optional, integer, default 14).
- `include` (optional) — Set `amplifier_dates` to date YouTube amplifiers.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/campaign?hashtag=shotoniphone&window_start=2026-05-01"
```

---

## Crisis monitoring

### GET /v1/prism/crisis-radar — 10 credits baseline (+30cr on a confirmed breach)

A stateless crisis breach check: a 7-day rolling z-score on mention volume + negative-share → an `alert_level` (`calm`/`watch`/`alert`/`crisis`). With `confirm=true`, a breach triggers escalation legs and a severity grade — the +30cr is charged ONLY when a breach actually fires.

- `brand` (required) — The brand to watch.
- `sensitivity` (optional, default 2.0) — Z-score breach threshold (0.5–6).
- `confirm` (optional, boolean) — Run escalation on breach (+30cr only when it fires).
- `baseline_days` (optional, default 7) / `date_to` (optional).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/crisis-radar?brand=Acme&confirm=true"
```

### GET /v1/prism/crisis-postmortem — 35 credits

A who-said-what-first crisis timeline across web + Reddit + Hacker News + social, with an origin (from natively-dated events only), peak day, propagation sequence, and a grounded LLM narrative.

- `brand` (required) — The entity the crisis is about.
- `window_start` (required) — Crisis window start (YYYY-MM-DD).
- `window_end` (optional) — Default today.
- `crisis_terms` (optional) — CSV of ≤5 scoping terms.
- `include` (optional) — `narrative` is on by default; pass empty for the raw timeline only.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/crisis-postmortem?brand=Acme&window_start=2026-05-01"
```

---

## Developer & launch intelligence

### GET /v1/prism/devtool-pulse — 15 credits

Developer-brand health: a devtool's GitHub repo dossier + Hacker News reaction + Reddit chatter + dev-blog echo, folded into a health block (release recency, open issues, top feature request/complaint, attention, a `pulse` label).

- `query` (required) — The devtool name (e.g. Bun, Drizzle ORM, tRPC).
- `repo` (optional) — `owner/repo` or a github URL (recommended for a precise dossier).
- `subreddit` (optional) — Scope the Reddit leg.
- `include` (optional) — CSV subset of `dossier,hn,reddit,blogs`.
- `date_from` / `date_to` (optional).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/devtool-pulse?query=Bun"
```

### GET /v1/prism/launch-echo — 10 credits

How a launch landed — the Hacker News reaction (top threads + comments) + dev-blog echo + an optional GitHub repo dossier.

- `query` (required) — The launch/product name.
- `repo` (optional) — `owner/repo` or github URL to anchor the dossier.
- `threads` (optional, integer) — Top HN threads to dig comments for.
- `date_from` / `date_to` / `include` (optional).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/launch-echo?query=Bun 1.2"
```

### GET /v1/prism/org-radar — metered, 1 credit + 5 credits per repo

A GitHub org → its top repos each expanded into a full dossier (releases, issue load, top request/complaint), rolled up to an org level. Ceiling = 1 + 5×`repos`; unused per-repo credits refund.

- `org` (required) — GitHub org login or `github.com/{org}` URL.
- `repos` (optional, integer) — Top repos to dossier (1–10, default 5) — drives the metered price.
- `sort` (optional, enum stars|updated|pushed) — Repo ranking (default stars).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/org-radar?org=vercel"
```

---

## Research & answers

### GET /v1/prism/answers — 15 credits (always SSE)

Multi-engine AI consensus: one question → Perplexity + Grok + Tavily answers kept verbatim, citations merged + deduped, plus an LLM-judged agreement matrix and disputed claims. Always streams; never cached. Coverage-floor partial refund.

- `query` (required) — The question, forwarded verbatim to every engine.
- `engines` (optional) — CSV subset of `perplexity,grok,tavily`.
- `include` (optional) — `polymarket` adds market grounding.

```bash
curl -N -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Accept: text/event-stream" \
  "https://www.socialcrawl.dev/v1/prism/answers?query=will the fed cut rates in september"
```

### GET /v1/prism/ai-visibility — metered, 2 credits per probe (prompt × run × engine)

AI Share-of-Voice / GEO monitoring — a prompts × runs × engines matrix across grounded-answer engines → per-brand **appearance-%** per engine (never volatile rank) + a cited-domain ranking. Unran/unparsed probes are refunded.

- `brand` (required) — Whose appearance-% is measured.
- One of `prompts` / `topic` is required (`prompts` = JSON array or pipe-delimited list, 1–20).
- `competitors` (optional) — CSV of up to 5.
- `engines` (optional) — CSV subset of `perplexity,grok`.
- `runs` (optional, integer 1–20, default 8) / `preset` (quick|standard|deep) / `include=web_baseline` / `brand_domains`.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/ai-visibility?brand=Notion&topic=best note taking app"
```

### GET /v1/prism/audience-questions — 30 credits

The real questions a topic's audience asks — harvested from Reddit + YouTube threads and LLM-clustered by intent (who/what/why/how/vs) with verbatim quotes + per-question source counts.

- `topic` (required) — The topic/keyword.
- `platforms` (optional) — CSV subset of `reddit,youtube,web`.
- `max_questions` / `threads_per_source` / `timeframe` (optional).
- `include` (optional) — Set `web` to add the universal-search leg.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/audience-questions?topic=kubernetes operators"
```

### GET /v1/prism/leads — 20 credits

A ranked, deduped feed of public conversations seeking alternatives to (or switching from) a competitor. **Conversation-level intent only — no author PII.** Deterministic, no LLM.

- `competitor` (required) — The competitor/product to mine (≤80 chars).
- `product_category` (optional) — Disambiguator to cut cross-domain noise.
- `freshness` (optional, default 30d) — `Nd`/`Nw`/`Nm` or an ISO date.
- `limit` (optional, integer 1–100, default 50).
- `include` (optional) — Set `comments` to attach top-thread Reddit comments.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/leads?competitor=notion&product_category=project management"
```

---

## App stores

### GET /v1/prism/apps-lookup — 30 credits

One app across Google Play + the App Store — resolved, title-matched (so same-named apps aren't conflated), and compared into a cross-store rating + listing report. Neither store resolves → 404 + refund.

- One of `title` / `google_play_id` / `app_store_id` is required.
- `stores` (optional) — CSV subset of `google_play,app_store`.
- `country` / `language` (optional).
- `match_threshold` (optional, default 0.6) — Title-similarity guard (0–1).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/apps-lookup?title=Notion"
```

### GET /v1/prism/app-reviews — 15 credits both stores / 10 credits single store

Cross-store app review intelligence (Google Play + App Store) — per-store rating summary, LLM topic clusters + feature requests, a sentiment timeline, dev-response rate, plus every raw review. SSE-capable.

- One of `google_play_id` / `app_store_id` / `query` is required.
- `country` / `language` (optional).
- `depth` (optional, integer) — Reviews per store (default 150 Google / 50 Apple, max 600).
- `stores` (optional) — CSV subset of `google_play,app_store`.
- `include` (optional) — CSV of `topics,sentiment_timeline,feature_requests,responses`.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/app-reviews?query=Spotify"
```

---

## Regional & specialized

### GET /v1/prism/korea-gap — metered 40 credits (15 web-only)

The gap between the global/English conversation and the Korean (Naver) conversation for a brand/topic — a per-surface presence index + a Korean channel map + translated quote samples. Drop `social` for the 15cr web-only variant.

- `query` (required) — The brand/topic to compare.
- `include` (optional) — `social` (the everywhere leg) + `digest`.
- `date_from` / `date_to` / `display` (optional).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/korea-gap?query=Stanley cup"
```

### GET /v1/prism/truthsocial-pulse — 8 credits

A Truth Social handle's pulse — profile + recent posts + per-post detail drill + a news echo, folded into a deterministic activity/sentiment pulse. Profile leg critical (404 → full refund). Handle-scoped (no Truth Social search exists upstream).

- `handle` (required) — The Truth Social handle (no @).
- `drill` (optional, integer) — Top posts to drill for full detail (0 to skip).
- `posts` (optional, integer) — Recent posts to pull.
- `news_query` / `include` / `cursor` (optional).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/truthsocial-pulse?handle=realDonaldTrump"
```

### GET /v1/prism/employer-brand — 30 credits

A company's employer brand — what people say about working there across Reddit + web + YouTube + Naver + the company's own LinkedIn voice, with a posting-tone-vs-reality gap.

- `company` (required) — The employer/company name.
- `linkedin_url` (optional) — Enables the LinkedIn voice axis + the posting-vs-reality gap.
- `surfaces` / `phrases` / `timeframe` / `date_from` / `date_to` (optional).

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/prism/employer-brand?company=Stripe"
```

---

## Monitors — scheduled Prism

Any Prism recipe (or raw endpoint) can be wrapped in a **stateful schedule** that re-runs it on a cadence, delivers each result to a signed webhook, and accumulates a time-series. *"Prism answers once; monitors watch it for you."* Monitors live at `/v1/monitors/*` (POST/GET/PATCH/DELETE) and are documented separately — see **[monitors.md](monitors.md)**.
