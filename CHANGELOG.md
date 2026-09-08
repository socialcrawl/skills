# Changelog

## 2026-09-08

- Re-synced the whole skill with the backend registry: **48 platforms / 381 endpoints -> 65 platforms / 572 endpoints**. The bundled catalogue had drifted three weeks behind the API, so every platform reference, the pricing reference, and the SKILL.md tables are regenerated.
- **Eighteen new platform references.** Commerce and marketplaces: `klarna` (merchant offers, price history, professional reviews, buying guides), `aliexpress`, `sephora` (incl. per-SKU in-store availability), `gumtree` (UK classifieds), `etsy`, `hm` (incl. supplier and factory disclosure), `kohls`, `wayfair`. Reviews and places: `g2` (software reviews), `yelp`. Data: `us_congress_trades` (STOCK Act disclosures with the full statistics suite), `jobs` (LinkedIn/Indeed/Bing/Xing listings plus salary bands), `finance` (quotes, news, price history, financial statements, options chains), `on_page` (single-URL SEO audit). Social: `douyin`, `quora`, `apple_music`, `telegram`.
- **`cohorts.md`, a new reference for the second stateful family** (`/v1/cohorts/*` + `/v1/cohort-queries/*`): upload a panel of up to 10,000 public identities and ask which of *them* posted your keywords. Covers the eight routes, the ten identity platforms, the `Idempotency-Key` requirement on POST/PUT, the deterministic matching rules, the coverage contract, and the computed credit ceiling. Neither stateful family is counted in the endpoint total.
- **Existing platforms grew.** Tripadvisor 2 -> 16 (hotels, restaurants, attractions and cruises, each with search, detail and reviews); TikTok 21 -> 34 (Ad Library, playlists, collections, liked videos, place feeds, effects, music search); Twitter 8 -> 15 (tweet and user search, replies, media, followers, following, retweeters); Reddit 8 -> 14 (user profiles with post and comment history, comment/media/subreddit search); Amazon 5 -> 8 (Best Sellers, deals, sellers); Home Depot 2 -> 4; Instagram 33 -> 37; LinkedIn 44 -> 45 (the metered full post-history archive walk); Facebook, YouTube, Google Shopping, Snapchat and Universal Search each gained an endpoint.
- `google_finance` is superseded by the broader `finance` platform, which keeps quotes, ticker search and the markets overview and adds instrument news, daily price-history bars, company financial statements, and options chains.
- Corrected the `search/news` band throughout: it is **2-62 credits**, not 2-14, since the bing engine added per-article billing. The figure is now read from the registry rather than retyped, so it cannot rot again.
- SKILL.md now routes the "which of THESE accounts talked about it" question to Cohorts (and away from Prism brand-mentions), and documents `PUT` — the only PUT in the API — alongside the other non-GET routes.
- **Every metered endpoint now explains its own price.** Twenty-nine endpoints published an honest range but no rule, so a reader could see that `linkedin/profile/posts/archive` costs 5-500 credits without learning that `limit` is the lever, or that `prism/share-of-voice` is priced per brand and halves without the social leg. Each one now carries the arithmetic, the default, the ceiling and what gets refunded — in its endpoint section and in the pricing reference's metered table.
- **Every parameter now carries a description.** Fifty-two parameters across the `/v1/web/*` surface and the `{platform}/profile/full` composites were published as a bare name and type: `only_main_content (optional, boolean)` and nothing more. The identity parameters on `profile/full` were the worst of it, since they are the one parameter those endpoints cannot be called without.
- **The unit-price headings on the Prism batches are now generated, not hand-corrected.** `POST /v1/prism/post-stats`, `/v1/prism/profiles` and `/v1/prism/comment-lookup` publish 1-500, 1-250 and 2-100 credits from the registry, so the fix made by hand on 20/08 can no longer be lost by a regeneration.
- **No supplier is named anywhere in the bundle.** Thirty-six mentions of upstream data providers were removed from endpoint descriptions, parameter descriptions, the withdrawn-endpoint lists and the hand-written overview prose. Withdrawn endpoints now say whether they are coming back, which is the part a caller can act on, instead of quoting an internal triage note.

## 2026-08-20

- Licensed the repository under MIT, including permission to reuse and adapt the skill with the licence notice retained.
- Added a mandatory request-level cost gate and a dedicated reference for row, URL, probe, page, chunk, runtime, and recurring billing.
- Corrected misleading unit-price headings for Prism batches, YouTube transcript batches, web batch scraping, and browser sessions.
- Documented the 32-credit default one-prompt `prism/ai-visibility` request and its complete formula.
- Removed the obsolete 50-credit custom/composite ceiling from overview tables.
- Hardened API-key resolution so agents do not print, paste, log, or persist secrets from chat.
- Added bounded, idempotency-aware retry guidance and clearer error classification.
- Added deterministic mirror synchronisation, `.skill` packaging, automated release checks, and stable update/download instructions.
