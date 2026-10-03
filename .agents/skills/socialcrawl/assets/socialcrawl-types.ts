/**
 * SocialCrawl response types. Generated from the canonical schemas
 * (packages/social-api/src/schemas/canonical.ts); do not edit.
 *
 * Every response is `ApiResponse<Data>` or, on failure, `ApiErrorBody`. A canonical
 * object (`Comment`, `Post`, `Author`, ...) is the same shape on every platform; a list
 * is `{ items: [{ <row key>: Object }], next_cursor?, total? }` with `pagination` at the
 * envelope root. Response types are named after the endpoint id, for the endpoints the
 * recipes use; any other endpoint returns the canonical type of its archetype
 * (`GET /v1/utility/endpoints` or assets/endpoints.json names it).
 */

export interface Pagination {
  next_cursor: string | null;
  has_more: boolean;
  page_size: number;
  stopped_at?: "since" | "known_id" | "end" | null;
}

export interface ApiResponse<T> {
  success: true;
  platform: string;
  endpoint: string;
  data: T;
  credits_used: number;
  /** null means unknown, never zero. */
  credits_remaining: number | null;
  request_id: string;
  cached: boolean;
  /** On every list response. */
  pagination?: Pagination;
  idempotent_replay?: true;
}

export interface ApiErrorBody {
  success: false;
  error: {
    /** The error code, e.g. INSUFFICIENT_CREDITS, RATE_LIMITED. */
    type: string;
    message: string;
    status: number;
    doc_url: string;
    retryable?: boolean;
    details?: Record<string, unknown>;
  };
  credits_used: number;
  credits_remaining: number | null;
  request_id: string;
}


export interface Author {
  id?: string;
  username?: string | null;
  display_name?: string | null;
  avatar_url?: string | null;
  bio?: string | null;
  verified?: boolean | null;
  followers?: number | null;
  following?: number | null;
  posts_count?: number | null;
  likes_count?: number | null;
  url?: string | null;
  location?: string | null;
  external_url?: string | null;
  private?: boolean | null;
  joined_at?: string | null;
  last_post_at?: string | null;
  ext?: { social_context?: string | null; account_created?: string | null; country?: string | null; collects_received?: number | null; former_usernames?: string[] | null; public_email?: string | null; contact_email?: string | null; public_phone?: string | null; similar_source?: string | null; instagram_username?: string | null; business_category?: string | null; hd_avatar_url?: string | null; website?: string | null; cover_url?: string | null; page_active?: boolean | null; employee_count?: number | null; employee_count_range?: { start?: number | null; end?: number | null } | null; founded_year?: number | null; specialities?: string[] | null; industries?: string[] | null; headquarters?: string | null; locations?: string[] | null; hashtags?: string[] | null; funding?: string | null; address?: string | null; price_range?: string | null; rating?: string | null; rating_count?: number | null; talking_about_count?: number | null; business_hours?: string[] | null; links?: string[] | null; ad_library_page_id?: string | null; ad_library_status?: string | null; urn?: string | null; is_top_voice?: boolean | null; is_premium?: boolean | null; is_creator?: boolean | null; is_influencer?: boolean | null; is_open_to_work?: boolean | null; is_hiring?: boolean | null; member_id?: string | null; company_id?: string | null; reaction_type?: string | null; followers_approximate?: boolean | null; keywords?: string | null; total_views?: number | null; joined_at_timestamp?: string | null; topicCategories?: string[] | null; bannerExternalUrl?: string | null; madeForKids?: boolean | null; hiddenSubscriberCount?: boolean | null; related_playlists?: string | null; topic_ids?: string[] | null; unsubscribed_trailer?: string | null; localizations?: string | null; monthly_listeners?: number | null; total_ratings?: number | null; average_rating?: number | null; creator_username?: string | null; join_policy?: string | null; is_nsfw?: boolean | null; rules?: string[] | null; weekly_active_users?: number | null; weekly_contributions?: number | null; rules_text?: string | null; language?: string | null; post_karma?: number | null; comment_karma?: number | null; awardee_karma?: number | null; trophy_count?: number | null; banner_url?: string | null; profile_title?: string | null; social_links?: string[] | null; bio_link?: string | null; group?: string | null; search_hit?: { match?: string | null; title?: string | null; snippet?: string | null; evidence_url?: string | null } | null } | null;
}

export interface AuthorList {
  items: { author: Author }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Post {
  id?: string;
  url?: string | null;
  content?: { text?: string | null; media_urls?: string | string[] | null; thumbnail_url?: string | null; duration_seconds?: number | null };
  author?: { username?: string | null; display_name?: string | null; avatar_url?: string | null; verified?: boolean | null };
  engagement?: { views?: number | null; likes?: number | null; comments?: number | null; shares?: number | null; saves?: number | null };
  flags?: { nsfw?: boolean | null; spoiler?: boolean | null; pinned?: boolean | null; deleted?: boolean; likes_hidden?: boolean | null; comments_hidden?: boolean | null; shares_hidden?: boolean | null; views_hidden?: boolean | null; saves_hidden?: boolean | null };
  published_at?: string | number | null;
  ext?: { music_id?: string | null; author_id?: string | null; author_followers?: number | null; author_following?: number | null; author_posts_count?: number | null; author_country?: string | null; author_public_email?: string | null; author_public_phone?: string | null; download_count?: number | null; region?: string | null; subreddit?: string | null; title?: string | null; selftext?: string | null; upvote_ratio?: number | null; flair?: string | null; content_language?: string | null; type?: string | null; content_type?: string | null; ticker_symbols?: string[] | null; video_view_count?: number | null; ig_play_count?: number | null; repost_count?: number | null; media_type?: string | null; text_truncated?: boolean | null; ip_location?: string | null; carousel_count?: number | null; remix_count?: number | null; audio_cluster_id?: string | null; facebook_likes?: number | null; facebook_comments?: number | null; published_at_epoch?: number | null; usertags?: string[] | null; coauthors?: string[] | null; music?: string | null; sponsor_tags?: string[] | null; location?: string | null; quoted_post?: string | null; retweeted_post?: string | null; quote_count?: number | null; all_media_urls?: string[] | null; reaction_counts?: string[] | null; share_urn?: string | null; post_type?: string | null; activity_id?: string | null; published_at_precision?: string | null; author_urn?: string | null; author_headline?: string | null; author_type?: string | null; is_repost_quote?: boolean | null; article?: string | null; reaction_type?: string | null; download_media_urls?: string[] | null; tags?: string[] | null; categoryId?: string | null; categoryTitle?: string | null; topicCategories?: string[] | null; duration?: string | null; license?: string | null; madeForKids?: boolean | null; defaultAudioLanguage?: string | null; hasPaidProductPlacement?: boolean | null; caption?: string | null; position?: number | null; playlistId?: string | null; videoOwnerChannelId?: string | null; videoPublishedAt?: string | null; description?: string | null; default_language?: string | null; localizations?: string | null; playlist_item_id?: string | null; playlist_owner_channel_id?: string | null; playlist_owner_title?: string | null; channel_id?: string | null; published_label?: string | null; published_precision?: string | null; video_count?: number | null; commerce?: string | null; on_screen_texts?: string[] | null; topic_tag?: string | null; reshare_count?: number | null; dsp_ids?: string | null; topic_tag_id?: string | null; amazon_shop_lists?: string[] | null; amazon_shop_trending_picks?: string[] | null; amazon_shop_curations?: string[] | null; amazon_shop_socials?: string[] | null; ad?: string | null; apple_music?: string | null; feedback_id?: string | null; event?: string | null; trend?: string | null; updated_at?: string | null } | null;
}

export interface PostList {
  items: ({ post: Post; computed?: { engagement_rate?: number | null; language?: string | null; content_category?: string | null; estimated_reach?: number | null; relevance?: { p?: number; sense?: string; depth?: number; spam?: number } | null; labels?: string | null; labels_evidence?: string | null } })[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Comment {
  id?: string;
  url?: string | null;
  parent_id?: string | null;
  post_id?: string | null;
  text?: string | null;
  author?: { username?: string | null; display_name?: string | null; avatar_url?: string | null; verified?: boolean | null };
  engagement?: { likes?: number | null; replies?: number | null };
  flags?: { pinned?: boolean | null; deleted?: boolean };
  published_at?: string | number | null;
  ext?: { replies_token?: string | null; replies_cursor?: string | null; depth?: number | null; published_at_epoch?: number | null; feedback_id?: string | null; expansion_token?: string | null; author_id?: string | null; ip_location?: string | null; urn?: string | null; reaction_counts?: string[] | null; is_edited?: boolean | null; previous_replies_token?: string | null; author_headline?: string | null; updated_at?: string | null; author_channel_id?: string | null; author_url?: string | null; viewer_rating?: string | null; text_original?: string | null; preview_replies?: string[] | null; lookup?: string | null; post_title?: string | null; post_url?: string | null; subreddit?: string | null; subreddit_subscribers?: number | null; post_score?: number | null; post_comment_count?: number | null; post_author?: string | null; post_published_at?: string | null; post_flair?: string | null; is_submitter?: boolean | null; edited_at?: string | null; controversiality?: number | null; content_language?: string | null; author_followers?: number | null; author_following?: number | null; author_posts_count?: number | null; quote_count?: number | null; views?: number | null; saves?: number | null } | null;
  replies?: Record<string, unknown>[] | null;
}

export interface CommentList {
  items: { comment: Comment }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Audience {
  audienceLocations?: { country?: string; countryCode?: string; count?: number; percentage?: string }[] | null;
  audienceAges?: { key?: string; percentage?: number }[] | null;
  audienceGenders?: { key?: string; percentage?: number }[] | null;
  audienceStates?: { state?: string; count?: number }[] | null;
}

export interface SearchResult {
  items?: Record<string, unknown>[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Analytics {
  metrics?: { total_views?: number; total_likes?: number; total_comments?: number; engagement_rate?: number };
  period?: string | null;
  breakdown?: Record<string, unknown>[] | null;
}

export interface Transcript {
  transcript?: string | null;
  transcripts?: { text?: string }[] | null;
}

export interface WebPage {
  page?: { url?: string | null; final_url?: string | null; status_code?: number | null; scrape_id?: string | null; fetched_at?: string | null; content?: { markdown?: string | null; html?: string | null; raw_html?: string | null; summary?: string | null }; media?: { screenshot_url?: string | null; audio_url?: string | null; video_url?: string | null }; extraction?: Record<string, unknown> | null; fetch?: { cache_state?: string | null; cached_at?: string | null; proxy_tier?: string | null } };
}

export interface WebPageList {
  items: WebPage[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Product {
  id?: string;
  url?: string | null;
  title?: string | null;
  description?: string | null;
  seller?: string | null;
  brand?: string | null;
  price?: { current?: number | null; original?: number | null; currency?: string | null };
  rating?: { average?: number | null; count?: number | null };
  image_urls?: string | string[] | null;
  availability?: string | null;
  reviews_count?: number | null;
  features?: string[] | null;
  specifications?: ({ group?: string | null; name?: string | null; value?: string | null })[] | null;
  variations?: ({ id?: string | null; title?: string | null; url?: string | null; category?: string | null })[] | null;
  ext?: { gid?: string | null; data_docid?: string | null; pvf?: string | null; seller_id?: string | null; sold_count?: number | null; bought_past_month?: number | null; bought_past_month_label?: string | null; catalog_id?: string | null; requested_id?: string | null; rating_distribution?: { star_1?: number | null; star_2?: number | null; star_3?: number | null; star_4?: number | null; star_5?: number | null } | null; store_inventory?: ({ store_id?: string | null; store_name?: string | null; state?: string | null; in_stock?: boolean | null; quantity?: number | null; fulfillment?: string | null; service?: string | null; location_type?: string | null; is_selected_store?: boolean | null })[] | null; promotion?: { label?: string | null; amount_off?: number | null; percent_off?: number | null } | null; price_note?: string | null; condition?: string | null; available_quantity?: number | null; watchers?: number | null; sold_at?: string | null; sold_caption?: string | null; buying_format?: string | null; seller_reputation?: { feedback_percentage?: number | null; feedback_count?: number | null; top_rated?: boolean | null; items_sold?: number | null; joined?: string | null; url?: string | null; detailed_ratings?: { accurate_description?: number | null; reasonable_shipping_cost?: number | null; shipping_speed?: number | null; communication?: number | null } | null } | null; g2?: string | null; etsy?: string | null; sephora?: string | null; hm?: string | null; kohls?: string | null; gumtree?: string | null; sku_id?: string | null; aliexpress?: string | null; tiktokshop?: string | null } | null;
}

export interface ProductList {
  items: { product: Product }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Review {
  id?: string;
  entity_id?: string | null;
  url?: string | null;
  title?: string | null;
  text?: string | null;
  rating?: { value?: number | null; max?: number | null };
  author?: { name?: string | null; avatar_url?: string | null; url?: string | null; location?: string | null; reviews_count?: number | null };
  helpful_votes?: number | null;
  verified?: boolean | null;
  source?: string | null;
  language?: string | null;
  original_language?: string | null;
  translated?: boolean | null;
  images?: string[] | null;
  responses?: ({ id?: string | null; author?: string | null; text?: string | null; published_at?: string | number | null })[] | null;
  published_at?: string | number | null;
  ext?: { appdata?: string | null; tiktokshop?: string | null } | null;
}

export interface ReviewList {
  items: { review: Review }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Seller {
  id?: string | null;
  name?: string | null;
  domain?: string | null;
  url?: string | null;
  price?: { base?: number | null; tax?: number | null; shipping?: number | null; total?: number | null; currency?: string | null };
  rating?: { average?: number | null; count?: number | null };
  condition?: string | null;
  availability?: string | null;
  annotation?: string | null;
}

export interface SellerList {
  items: { seller: Seller }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Place {
  id?: string;
  name?: string | null;
  url?: string | null;
  category?: string | null;
  rating?: { value?: number | null; max?: number | null };
  reviews_count?: number | null;
  price_level?: string | null;
  address?: string | null;
  phone?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  verified?: boolean | null;
  description?: string | null;
  image_urls?: string | string[] | null;
  categories?: string[] | null;
  hotel?: { stars?: number | null; stars_description?: string | null; check_in_time?: string | null; check_out_time?: string | null; amenities?: ({ category?: string | null; name?: string | null; available?: boolean | null; hint?: string | null })[] | null; review_topics?: ({ title?: string | null; positive_score?: number | null; positive_count?: number | null; negative_count?: number | null; total_count?: number | null })[] | null; prices?: ({ title?: string | null; price?: number | null; currency?: string | null; url?: string | null; official_site?: boolean | null })[] | null } | null;
  ext?: { distance?: number | null; status?: string | null; timezone?: string | null; hours?: ({ date?: string | null; day_name?: string | null; is_open?: boolean | null; opens_at?: string | null; closes_at?: string | null })[] | null; place_id?: string | null; attributes?: string | null; rating_distribution?: string | null; people_also_search?: ({ cid?: string | null; title?: string | null; rating?: { value?: number | null; votes_count?: number | null } | null })[] | null; menu_url?: string | null } | null;
}

export interface PlaceList {
  items: { place: Place }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface App {
  id?: string;
  store?: string;
  url?: string | null;
  title?: string | null;
  subtitle?: string | null;
  icon?: string | null;
  description?: string | null;
  developer?: { id?: string | null; name?: string | null; url?: string | null; email?: string | null; address?: string | null; website?: string | null };
  rating?: { value?: number | null; max?: number | null; count?: number | null };
  price?: { current?: number | null; original?: number | null; currency?: string | null; is_free?: boolean | null; displayed?: string | null };
  reviews_count?: number | null;
  category?: string | null;
  categories?: string[] | null;
  installs?: { display?: string | null; count?: number | null } | null;
  version?: string | null;
  minimum_os_version?: string | null;
  size?: string | null;
  released_at?: string | number | null;
  updated_at?: string | number | null;
  update_notes?: string | null;
  image_urls?: string[] | null;
  video_urls?: string[] | null;
  languages?: string[] | null;
  advisories?: string[] | null;
  genres?: string[] | null;
  tags?: string[] | null;
  similar_apps?: ({ id?: string | null; title?: string | null; url?: string | null })[] | null;
  more_by_developer?: ({ id?: string | null; title?: string | null; url?: string | null })[] | null;
  ext?: { appdata?: string | null } | null;
}

export interface AppList {
  items: { app: App }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface NewsArticleList {
  items: ({ article: { id?: string; title?: string | null; url?: string | null; source?: string | null; domain?: string | null; snippet?: string | null; image_url?: string | null; published_at?: string | number | null; rank?: number | null; placement?: string | null } })[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Quote {
  id?: string;
  ticker?: string | null;
  exchange?: string | null;
  name?: string | null;
  type?: string;
  url?: string | null;
  currency?: string | null;
  pair?: { base_symbol?: string | null; quote_symbol?: string | null; base_display_name?: string | null; quote_display_name?: string | null } | null;
  price?: { current?: number | null; previous_close?: number | null; delta?: number | null; percentage_delta?: number | null; trend?: string | null; day_low?: number | null; day_high?: number | null; year_low?: number | null; year_high?: number | null; timestamp?: string | null };
  metrics?: { market_cap?: number | null; volume?: number | null; avg_volume?: number | null; pe_ratio?: number | null; dividend_yield?: number | null; ytd_return?: number | null; expense_ratio?: number | null; net_assets?: number | null; yield?: number | null; open_interest?: number | null; category?: string | null; metrics_currency?: string | null } | null;
  about?: { description?: string | null; description_source_url?: string | null; ceo?: string | null; founded?: string | null; headquarters?: string | null; website?: string | null; employees?: number | null } | null;
  graph?: ({ timestamp?: string; value?: number; volume?: number | null })[] | null;
  financials?: { quarterly?: string[] | null; annual?: string[] | null } | null;
  peers?: ({ id?: string; ticker?: string | null; exchange?: string | null; name?: string | null; type?: string; url?: string | null; currency?: string | null; pair?: { base_symbol?: string | null; quote_symbol?: string | null; base_display_name?: string | null; quote_display_name?: string | null } | null; price?: { current?: number | null; previous_close?: number | null; delta?: number | null; percentage_delta?: number | null; trend?: string | null; day_low?: number | null; day_high?: number | null; year_low?: number | null; year_high?: number | null; timestamp?: string | null }; metrics?: { market_cap?: number | null; volume?: number | null; avg_volume?: number | null; pe_ratio?: number | null; dividend_yield?: number | null; ytd_return?: number | null; expense_ratio?: number | null; net_assets?: number | null; yield?: number | null; open_interest?: number | null; category?: string | null; metrics_currency?: string | null } | null })[] | null;
  ext?: string | null;
}

export interface QuoteList {
  items: { quote: Quote }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface BarList {
  items: ({ bar: { id?: string; symbol?: string | null; date?: string | number | null; open?: number | null; high?: number | null; low?: number | null; close?: number | null; adj_close?: number | null; volume?: number | null; dividend?: number | null; split_ratio?: string | null; currency?: string | null; interval?: string | null } })[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface FinancialStatementList {
  items: ({ financial_statement: { id?: string; symbol?: string | null; statement?: string | null; period_type?: string | null; period_end?: string | number | null; currency?: string | null; revenue?: number | null; revenue_delta?: number | null; operating_expense?: number | null; operating_expense_delta?: number | null; net_income?: number | null; net_income_delta?: number | null; net_profit_margin?: number | null; net_profit_margin_delta?: number | null; earnings_per_share?: number | null; earnings_per_share_delta?: number | null; ebitda?: number | null; ebitda_delta?: number | null; effective_tax_rate?: number | null; cash_and_short_term_investments?: number | null; cash_and_short_term_investments_delta?: number | null; total_assets?: number | null; total_assets_delta?: number | null; total_liabilities?: number | null; total_liabilities_delta?: number | null; total_equity?: number | null; shares_outstanding?: number | null; price_to_book?: number | null; return_on_assets?: number | null; return_on_capital?: number | null; cash_from_operations?: number | null; cash_from_operations_delta?: number | null; cash_from_investing?: number | null; cash_from_investing_delta?: number | null; cash_from_financing?: number | null; cash_from_financing_delta?: number | null; net_change_in_cash?: number | null; net_change_in_cash_delta?: number | null; free_cash_flow?: number | null; free_cash_flow_delta?: number | null } })[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface OptionContractList {
  items: ({ option_contract: { id?: string; symbol?: string | null; contract_symbol?: string | null; type?: string | null; strike?: number | null; expiry?: string | number | null; last_price?: number | null; bid?: number | null; ask?: number | null; change?: number | null; percent_change?: number | null; volume?: number | null; open_interest?: number | null; implied_volatility?: number | null; in_the_money?: boolean | null; contract_size?: string | null; currency?: string | null; last_trade_date?: string | number | null } })[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface Job {
  id?: string;
  title?: string | null;
  url?: string | null;
  company?: { id?: string | null; name?: string | null; url?: string | null; verified?: boolean | null };
  location?: string | null;
  listed_at?: string | number | null;
  easy_apply?: boolean | null;
  remote?: string | null;
  employment_type?: string | null;
  experience_level?: string | null;
  description?: string | null;
  apply_url?: string | null;
  ext?: { is_promote?: boolean | null; applicant_count?: number | null; skills?: string[] | null; job_provider?: string | null; salary_min?: number | null; salary_max?: number | null; salary_currency?: string | null; country_code?: string | null; linkedin_company_name?: string | null; industries?: string | null; job_function?: string | null; accepting_applications?: boolean | null; board?: string | null } | null;
}

export interface JobList {
  items: { job: Job }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface MediaList {
  items: { url: string }[];
  next_cursor?: string | null;
  total?: number | null;
}

/** Response types for the endpoints the recipes use. */
export type PrismBrandMentionsResponse = ApiResponse<Analytics>;
export type SearchMultiResponse = ApiResponse<Analytics>;
export type PrismMentionsResponse = ApiResponse<Analytics>;
export type PrismShareOfVoiceResponse = ApiResponse<Analytics>;
export type TwitterSearchTweetsResponse = ApiResponse<PostList>;
export type RedditSearchResponse = ApiResponse<PostList>;
export type SearchForumsResponse = ApiResponse<Analytics>;
export type GoogleNewsSearchResponse = ApiResponse<NewsArticleList>;
export type SearchCreatorsResponse = ApiResponse<Analytics>;
export type InstagramSearchReelsResponse = ApiResponse<PostList>;
export type PrismCreatorVetResponse = ApiResponse<Analytics>;
export type PrismCreatorCardResponse = ApiResponse<Analytics>;
export type TiktokProfileResponse = ApiResponse<Author>;
export type TiktokProfileVideosResponse = ApiResponse<PostList>;
export type TiktokPostCommentsResponse = ApiResponse<CommentList>;
export type PrismFindAccountsResponse = ApiResponse<Analytics>;
export type LinkedinProfileResponse = ApiResponse<Author>;
export type LinkedinProfilePostsResponse = ApiResponse<PostList>;
export type LinkedinSearchPeopleResponse = ApiResponse<AuthorList>;
export type LinkedinProfileCompleteResponse = ApiResponse<Analytics>;
export type PrismProfilesPostResponse = ApiResponse<Analytics>;
export type PrismCommentsResponse = ApiResponse<Analytics>;
export type YoutubeVideoTranscriptResponse = ApiResponse<Transcript>;
export type AmazonProductSearchResponse = ApiResponse<ProductList>;
export type AmazonReviewsResponse = ApiResponse<ReviewList>;
export type WalmartSearchResponse = ApiResponse<ProductList>;
export type WalmartReviewsResponse = ApiResponse<ReviewList>;
export type HomeDepotSearchResponse = ApiResponse<ProductList>;
export type HomeDepotReviewsResponse = ApiResponse<ReviewList>;
export type PrismProductReviewsResponse = ApiResponse<Analytics>;
export type AppStoreAppSearchResponse = ApiResponse<AppList>;
export type AppStoreAppReviewsResponse = ApiResponse<ReviewList>;
export type YelpSearchResponse = ApiResponse<PlaceList>;
export type YelpBusinessReviewsResponse = ApiResponse<ReviewList>;
export type FacebookAdlibraryCompanyAdsResponse = ApiResponse<PostList>;
export type InstagramProfilePostsResponse = ApiResponse<PostList>;
export type YoutubeChannelVideosResponse = ApiResponse<PostList>;
export type WebMonitorsPostResponse = ApiResponse<Analytics>;
export type WebMonitorsMonitorIdChecksResponse = ApiResponse<WebPageList>;
export type PrismPostStatsPostResponse = ApiResponse<Analytics>;
export type JobsSalaryResponse = ApiResponse<Analytics>;
export type JobsLinkedinSearchResponse = ApiResponse<JobList>;
export type FinanceTickerSearchResponse = ApiResponse<QuoteList>;
export type FinanceQuoteResponse = ApiResponse<Quote>;
export type FinanceNewsResponse = ApiResponse<NewsArticleList>;
export type WebCrawlPostResponse = ApiResponse<Analytics>;
export type WebJobsJobIdResponse = ApiResponse<Analytics>;
export type WebExtractResponse = ApiResponse<WebPage>;
export type NaverBriefResponse = ApiResponse<Analytics>;
export type NaverSearchTrendResponse = ApiResponse<Analytics>;
