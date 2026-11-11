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
  /** Rows a full page holds for this request; null when unverified. */
  typical_page_size?: number | null;
  /** Credits the next page costs; null when there is no next page. */
  next_page_credits?: number | null;
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
    /** Structured context: `next_step` says what to do next; a missing one-of group is named in `fields`. */
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
  ext?: { social_context?: string | null; account_based_in?: string | null; signup_source?: string | null; username_changes?: number | null; username_last_changed_at?: string | null; location_accurate?: boolean | null; created_country_accurate?: boolean | null; affiliate_username?: string | null; media_count?: number | null; likes_given?: number | null; creator_subscriptions_count?: number | null; verified_blue?: boolean | null; verified_legacy?: boolean | null; identity_verified?: boolean | null; verification_reason?: string | null; instagram_followers?: number | null; instagram_verified?: boolean | null; page_verification?: string | null; page_category?: string | null; entity_type?: string | null; is_political_page?: boolean | null; page_is_restricted?: boolean | null; verified_name?: string | null; verified_country_code?: string | null; advertiser_name?: string | null; registered_location?: string | null; advertiser_sponsor?: string | null; follower_count_text?: string | null; countries_shown?: string[] | null; ad_count?: number | null; gender?: string | null; birthday?: string | null; verified_reason?: string | null; ip_location?: string | null; verified_type?: number | null; hometown?: string | null; employer?: string | null; credit_level?: string | null; activity_summary?: string | null; account_created?: string | null; country?: string | null; country_name?: string | null; collects_received?: number | null; former_usernames?: string[] | null; former_usernames_count?: number | null; verified_at?: string | null; is_memorialized?: boolean | null; public_email?: string | null; contacts?: ({ kind?: "email"; value?: string; role?: "own" | "management" | "agency"; confidence?: number; provenance?: "published" | "gated_reveal"; verification?: { syntax?: boolean; mx?: boolean | null; disposable?: boolean; role_account?: boolean }; sources?: ({ tier?: "bio" | "bio_link" | "caption" | "external_url" | "about" | "instagram_panel" | "video_description" | "link_in_bio" | "website" | "button"; url?: string; snippet?: string; first_seen?: string; last_seen?: string })[] })[] | null; contact_email?: string | null; public_phone?: string | null; similar_source?: string | null; instagram_username?: string | null; similar_via?: string | null; business_category?: string | null; bio_links?: ({ title?: string | null; url?: string | null; link_type?: string | null })[] | null; is_business?: boolean | null; is_professional?: boolean | null; address_latitude?: number | null; address_longitude?: number | null; pronouns?: string[] | null; has_highlights?: boolean | null; threads_username?: string | null; latest_story_at?: string | null; creator_marketplace?: boolean | null; verification_label?: string | null; fbid?: string | null; hd_avatar_url?: string | null; website?: string | null; cover_url?: string | null; page_active?: boolean | null; employee_count?: number | null; employee_count_range?: { start?: number | null; end?: number | null } | null; founded_year?: number | null; company_type?: string | null; tagline?: string | null; specialities?: string[] | null; industries?: string[] | null; headquarters?: { country?: string | null; city?: string | null; geographic_area?: string | null; line1?: string | null; postal_code?: string | null; label?: string | null } | null; locations?: ({ name: string | null; address: { country: string | null; city: string | null; geographic_area: string | null; line1: string | null; line2?: string | null; postal_code: string | null }; lat_long: { latitude: number | null; longitude: number | null }; label?: string | null; is_headquarters?: boolean | null })[] | null; hashtags?: ({ name: string; follower_count: number | null })[] | null; funding?: { last_funding_round: { money_raised: unknown; announced_on: unknown } } | null; founded_on?: { year?: number | null; month?: number | null; day?: number | null } | null; company_type_code?: string | null; page_type?: "company" | "school" | "showcase" | null; domain?: string | null; is_claimable?: boolean | null; is_archived?: boolean | null; is_auto_generated?: boolean | null; verification_updated_at?: string | null; call_to_action_url?: string | null; industry_hierarchy?: string | null; public_phone_extension?: string | null; crunchbase_url?: string | null; open_job_count?: number | null; products?: unknown; address?: string | null; price_range?: string | null; rating?: string | null; rating_count?: number | null; talking_about_count?: number | null; business_hours?: unknown; links?: (string | { id?: string; type?: string; title?: string; url?: string; clicks?: number; order?: number | null })[] | null; ad_library_page_id?: string | null; ad_library_status?: string | null; urn?: string | null; is_top_voice?: boolean | null; is_premium?: boolean | null; is_creator?: boolean | null; is_influencer?: boolean | null; is_open_to_work?: boolean | null; is_hiring?: boolean | null; member_id?: string | null; joined_at_precision?: "month" | null; first_name?: string | null; last_name?: string | null; pronoun?: string | null; primary_locale?: string | null; supported_locales?: string[] | null; about?: string | null; about_localized?: Record<string, unknown> | null; headline_localized?: Record<string, unknown> | null; current_position?: { title?: string | null; company?: string | null; company_id?: string | null; company_username?: string | null; company_url?: string | null } | null; current_school?: { name?: string | null; school_id?: string | null; company_id?: string | null; username?: string | null; url?: string | null } | null; industry?: string | null; industry_id?: string | null; verifications?: ({ type?: string | null; label?: string | null; detail?: string | null })[] | null; geo_id?: string | null; is_open_profile?: boolean | null; last_name_is_initial?: boolean | null; volunteer_causes?: string[] | null; top_skills?: string[] | null; profile_actions?: ({ label?: string | null; url?: string | null })[] | null; section_totals?: Record<string, unknown> | null; company_id?: string | null; reaction_type?: string | null; public_identifier?: string | null; account_type?: string | null; followers_approximate?: boolean | null; counts_source?: "app" | "web" | null; posting_region?: string | null; keywords?: string | null; total_views?: number | null; joined_at_timestamp?: string | null; topicCategories?: string[] | null; bannerExternalUrl?: string | null; madeForKids?: boolean | null; hiddenSubscriberCount?: boolean | null; related_playlists?: { uploads: string; likes: string } | null; topic_ids?: string[] | null; unsubscribed_trailer?: string | null; localizations?: Record<string, unknown> | null; monthly_listeners?: number | null; total_ratings?: number | null; average_rating?: number | null; creator_username?: string | null; join_policy?: string | null; is_nsfw?: boolean | null; rules?: { id: string; rest_id: string; name: string; description: string }[] | null; weekly_active_users?: number | null; weekly_contributions?: number | null; rules_text?: string | null; language?: string | null; post_karma?: number | null; comment_karma?: number | null; awardee_karma?: number | null; trophy_count?: number | null; banner_url?: string | null; profile_title?: string | null; social_links?: { title: string; type: string; url: string }[] | null; bio_link?: string | null; embed_html?: string | null; embed_url?: string | null; group?: { privacy_label?: string; privacy_description?: string; visibility_label?: string; visibility_description?: string; member_count_text?: string; administrator_count?: number; moderator_count?: number; history_summary?: string; categories?: string[]; rules?: unknown[]; administrators?: { id: string; name: string; url: string; profile_picture_url: string }[]; moderators?: { id: string; name: string; url: string; profile_picture_url: string }[]; activity?: { posts_last_day: number; posts_last_month: number; new_members_text: string }; about_info?: { type: string; label: string; description: string }[] } | null; search_hit?: { match?: "group_page" | "post_in_group" | "channel_page" | "post_in_channel" | null; title?: string | null; snippet?: string | null; evidence_url?: string | null; matched_urls?: string[] | null } | null; blog_name?: string | null; blog_no?: string | null; visitors_today?: number | null; visitors_total?: number | null; topic?: string | null; power_blog?: boolean | null; official_blog?: boolean | null } | null;
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
  ext?: { music_id?: string | null; matched_song_id?: string | null; matched_song_title?: string | null; matched_song_artist?: string | null; music_title?: string | null; music_artist?: string | null; music_is_original?: boolean | null; author_id?: string | null; author_url?: string | null; author_followers?: number | null; author_following?: number | null; author_posts_count?: number | null; author_location?: string | null; in_reply_to_id?: string | null; in_reply_to_username?: string | null; conversation_id?: string | null; author_country?: string | null; author_public_email?: string | null; author_public_phone?: string | null; download_count?: number | null; region?: string | null; counts_approximate?: boolean | null; ran_as_ad?: boolean | null; tagged_products?: unknown[] | null; subreddit?: string | null; title?: string | null; selftext?: string | null; link_domain?: string | null; upvote_ratio?: number | null; flair?: string | null; content_language?: string | null; removed?: boolean | null; removed_by?: string | null; type?: string | null; content_type?: "video" | "short" | "live" | "channel" | "playlist" | null; ticker_symbols?: string[] | null; video_view_count?: number | null; ig_play_count?: number | null; repost_count?: number | null; media_type?: "image" | "video" | "carousel" | null; text_truncated?: boolean | null; ip_location?: string | null; carousel_count?: number | null; remix_count?: number | null; audio_cluster_id?: string | null; facebook_likes?: number | null; facebook_comments?: number | null; instagram_views?: number | null; facebook_views?: number | null; published_at_epoch?: number | null; usertags?: string[] | null; coauthors?: ({ id: string; username: string; full_name?: string | null; is_verified?: boolean; profile_pic_url?: string })[] | null; music?: { id?: string; track_title?: string | null; artist?: string | null; is_original?: boolean } | null; use_count?: number | null; use_count_unit?: "videos" | null; shares_source?: "mobile_list" | "post_detail" | null; engagement_source?: "post_detail" | null; sponsor_tags?: string[] | null; sponsored_disclosed?: boolean | null; ai_label?: string | null; story_mentions?: string[] | null; story_links?: string[] | null; story_reshared_posts?: string[] | null; location?: { id: string | null; name: string | null; lat: number | null; lng: number | null } | null; media?: ({ type?: "image" | "video"; url?: string | null; width?: number | null; height?: number | null })[] | null; top_comments?: ({ id?: string | null; text?: string | null; username?: string | null; likes?: number | null; published_at?: string | null })[] | null; hashtags?: string[] | null; mentions?: string[] | null; mentioned_user_ids?: string[] | null; quoted_post?: { id: string; url: string; author: { id: string; username: string; display_name: string; verified?: boolean }; text: string | null; media_urls: string[] | null; thumbnail_url?: string | null; engagement: { views?: number; likes: number; comments: number; shares: number; saves?: number }; published_at: string; quote_count?: number } | null; retweeted_post?: { id: string; url: string; author: { id: string; username: string; display_name: string; verified?: boolean }; text: string | null; media_urls: string[] | null; thumbnail_url?: string | null; engagement: { views?: number; likes: number; comments: number; shares: number; saves?: number }; published_at: string; quote_count?: number } | null; quote_count?: number | null; all_media_urls?: string[] | null; reaction_counts?: ({ type?: string; count: number; emoji?: string | null; emoji_id?: string | null; count_text?: string })[] | null; share_urn?: string | null; post_type?: string | null; activity_id?: string | null; published_at_precision?: string | null; author_urn?: string | null; author_headline?: string | null; author_type?: string | null; is_repost_quote?: boolean | null; article?: { title: string; source: string; url: string; description?: string } | null; reaction_type?: string | null; reacted_at?: string | null; reaction?: string | null; reaction_activity_id?: string | null; mentioned_accounts?: ({ type: string | null; id: string | null; name: string | null; username: string | null; url: string | null })[] | null; text_entities?: ({ start: number | null; length: number | null; type: string | null; id: string | null; url: string | null })[] | null; outbound_links?: string[] | null; is_edited?: boolean | null; comments_disabled?: boolean | null; document?: { title: string | null; page_count: number | null; url: string | null; cover_url: string | null } | null; poll?: { question: string | null; options: ({ text: string | null; votes: number | null })[]; total_votes: number | null; voter_count: number | null; is_closed: boolean | null; remaining: string | null } | null; job?: { id: string | null; title: string | null; company_name: string | null; company_id: string | null; company_url: string | null; company_logo: string | null; location: string | null; url: string | null } | null; celebration?: { headline: string | null; image_url: string | null } | null; newsletter?: { title: string | null; url: string | null } | null; reposted_by?: { type: string | null; id: string | null; name: string | null; username: string | null; url: string | null } | null; reposted_at?: string | null; author_website?: string | null; author_website_label?: string | null; aspect_ratio?: number | null; author_is_premium?: boolean | null; content_credentials?: { is_ai_generated: boolean | null; issuer: string | null; signer: string | null; is_valid: boolean | null } | null; download_media_urls?: { post_id: string; cdn_url: string; type: string; cached: boolean }[] | null; tags?: string[] | null; categoryId?: string | null; categoryTitle?: string | null; topicCategories?: string[] | null; duration?: string | null; license?: string | null; madeForKids?: boolean | null; defaultAudioLanguage?: string | null; hasPaidProductPlacement?: boolean | null; caption?: string | null; playback_availability?: { visibility: string | null; age_restricted: boolean | null; members_only: boolean | null; family_safe: boolean | null; region_restricted: boolean | null; available_countries: string[] | null; live_content: boolean | null; live_now: boolean | null; upcoming: boolean | null; comments_visible: boolean | null; ratings_enabled: boolean | null } | null; position?: number | null; playlistId?: string | null; videoOwnerChannelId?: string | null; videoPublishedAt?: string | null; description?: string | null; default_language?: string | null; localizations?: Record<string, unknown> | null; playlist_item_id?: string | null; playlist_owner_channel_id?: string | null; playlist_owner_title?: string | null; channel_id?: string | null; published_label?: string | null; published_precision?: "minute" | "hour" | "day" | "week" | "month" | "year" | null; title_maybe_translated?: boolean | null; video_count?: number | null; posts_count?: number | null; commerce?: { price?: number | { sku_id?: string; current?: number; original?: number; currency?: string; discount_percent?: number; currency_name?: string; currency_symbol?: string; symbol_position?: number; show_currency_space?: boolean; currency_show_mode?: number; sale_price_decimal?: string; origin_price_decimal?: string; sale_price_format?: string; origin_price_format?: string; discount_format?: string; discount_decimal?: string; single_product_price_format?: string; single_product_price_decimal?: string; sale_price_integer_part_format?: string; sale_price_decimal_part_format?: string; decimal_point_symbol?: string; promotion_deduction_details?: { seller_subtotal_deduction: string; seller_subtotal_deduction_decimal: string } }; currency?: string; price_formatted?: string; strikethrough_price_formatted?: string; description?: string; location_text?: string; latitude?: number; longitude?: number; category_id?: string; mileage?: number | null; attributes?: { attribute_name: string; value: string; label: string }[]; delivery_types?: string[]; availability_text?: string | null; listing_date_text?: string; is_sold?: boolean; is_live?: boolean; is_pending?: boolean; is_hidden?: boolean; is_shipping_offered?: boolean; is_buy_now_enabled?: boolean; messaging_enabled?: boolean; seller_id?: string | null; seller_name?: string | null; rating?: { score: number; review_count: number; average: number; count: number }; sold?: { sold_count: number } } | null; on_screen_texts?: string[] | null; topic_tag?: string | null; reshare_count?: number | null; dsp_ids?: Record<string, unknown> | null; topic_tag_id?: string | null; amazon_shop_lists?: { title: string; itemCount: number; image: string; url: string }[] | null; amazon_shop_trending_picks?: ({ url: string; image: string; price: number; discount: string | null })[] | null; amazon_shop_curations?: { title: string; postCount: number; image: string; url: string }[] | null; amazon_shop_socials?: string[] | null; ad?: { page_id?: string; page_profile_uri?: string; page_like_count?: number; page_categories?: string[]; brand_name?: string; currency?: string; spend?: unknown; spent?: string; reach_estimate?: unknown; estimated_audience?: string; publisher_platforms?: string[]; categories?: string[]; targeted_or_reached_countries?: string[]; country_code?: string | string[]; cta_text?: string; cta_type?: string; link_url?: string; landing_page?: string; landing_page_url?: string | null; profile_web_link?: string; is_active?: boolean; end_date_iso?: string; last_shown_date?: number; display_format?: string; ad_format?: string | null; title?: string; caption?: string; video_hd_url?: string | null; video_sd_url?: string | null; video_url_540p?: string; video_url_360p?: string; video_id?: string; image_urls?: string[]; audit_status?: string; type?: string; source?: string; objectives?: ({ label: string; value: string | null })[]; objective?: string; industry?: string; language?: string | null; ctr?: number; cost_score?: number; rank?: number; like_tier?: string | null; is_spark_ad?: boolean | null; period_days?: number } | null; apple_music?: { kind: string; track_count?: number; release_info?: string; artist_url?: string; artist_id?: string; release_date?: string; genres?: { id: string; name: string }[]; content_advisory?: string | null; track_number?: number; explicit?: boolean } | null; feedback_id?: string | null; question_id?: string | null; answer_no?: number | null; answer_nos?: number[] | null; published_at_est?: string | null; date_basis?: string | null; event?: { description?: string; start_timestamp?: number; end_timestamp?: number | null; time_text?: string; duration_text?: string; location_name?: string; address?: string | null; city?: string | null; latitude?: number | null; longitude?: number | null; hosts?: { id: string; name: string; url: string; profile_picture_url: string; type: string; is_verified: boolean }[]; host_context_text?: string; category?: string; is_online?: boolean; is_canceled?: boolean; is_past?: boolean; privacy?: string; ticket_url?: string | null; attendance_count?: number; interested_count?: number; going_count?: number; id?: string | null; name?: string | null; date_text?: string | null; location?: string | null; url?: string | null; banner_url?: string | null } | null; trend?: { rank: number; country_code: string; chart?: string; chart_title?: string; updated_at?: string; period_days?: number; posts?: number; views?: number; period_views?: number; organic_views?: number; six_second_view_through_rate?: number; engagement_rate?: number; order_by?: string; industry?: string | null; industry_id?: string | null; industry_label?: string | null; boards?: ({ industry: string | null; industry_id: string | null; industry_label: string | null; rank: number })[]; popularity_curve?: { date: string; value: number }[]; top_creators?: { username: string; display_name: string; followers: number; country_code: string; url: string }[]; content_tags?: string[] } | null; updated_at?: string | null; alt_text?: string | null; board_name?: string | null; topic_labels?: string[] | null; story_expires_at?: string | null; numeric_id?: number | null; outbound_url?: string | null; group?: { id: string; url: string; name: string | null; members: number | null } | null } | null;
}

export interface PostList {
  items: ({ post: Post; computed?: { engagement_rate?: number | null; language?: string | null; content_category?: string | null; estimated_reach?: number | null; save_rate?: number | null; relevance?: { p?: number; sense?: "target" | "other_named_thing" | "generic_word" | "not_present"; depth?: number; spam?: number } | null; labels?: Record<string, unknown> | null; labels_evidence?: Record<string, unknown> | null } })[];
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
  flags?: { pinned?: boolean | null; deleted?: boolean; liked_by_creator?: boolean | null };
  published_at?: string | number | null;
  ext?: { replies_token?: string | null; replies_cursor?: string | null; depth?: number | null; published_at_epoch?: number | null; feedback_id?: string | null; expansion_token?: string | null; author_id?: string | null; ip_location?: string | null; urn?: string | null; reaction_counts?: { type: string; count: number }[] | null; is_edited?: boolean | null; previous_replies_token?: string | null; author_headline?: string | null; author_type?: string | null; author_urn?: string | null; is_contribution?: boolean | null; has_previous_replies?: boolean | null; updated_at?: string | null; author_channel_id?: string | null; author_url?: string | null; viewer_rating?: string | null; text_original?: string | null; preview_replies?: { id: string; channelId: string; videoId: string; textDisplay: string; textOriginal: string; parentId: string; authorDisplayName: string; authorProfileImageUrl: string; authorChannelUrl: string; authorChannelId: { value: string }; canRate: boolean; viewerRating: string; likeCount: number; publishedAt: string; updatedAt: string }[] | null; lookup?: { found_via: string; pages_fetched: number; comments_scanned: number; sort_basis: string; position_hint: string; post_comment_count?: number } | null; post_title?: string | null; post_url?: string | null; subreddit?: string | null; subreddit_subscribers?: number | null; post_score?: number | null; post_comment_count?: number | null; post_author?: string | null; post_published_at?: string | null; post_flair?: string | null; is_submitter?: boolean | null; edited_at?: string | null; removed_by?: string | null; controversiality?: number | null; content_language?: string | null; author_followers?: number | null; author_following?: number | null; author_posts_count?: number | null; author_location?: string | null; quote_count?: number | null; views?: number | null; saves?: number | null } | null;
  replies?: unknown[] | null;
}

export interface CommentList {
  items: ({ comment: Comment; computed?: { language?: string | null; labels?: Record<string, unknown> | null; labels_evidence?: Record<string, unknown> | null } })[];
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

}

export interface Transcript {
  transcript?: string | null;
  transcript_format?: "webvtt" | "text";
  transcripts?: { text?: string }[] | null;
}

export interface WebPage {
  page?: { url?: string | null; final_url?: string | null; status_code?: number | null; scrape_id?: string | null; fetched_at?: string | null; published_at?: string | null; content?: { markdown?: string | null; html?: string | null; raw_html?: string | null; summary?: string | null }; media?: { screenshot_url?: string | null; audio_url?: string | null; video_url?: string | null }; title?: string | null; description?: string | null; source_type?: "web" | "news" | "image" | null; extraction?: Record<string, unknown> | null; answer?: unknown; highlights?: unknown; change_tracking?: unknown; page_count?: number | null; total_page_count?: number | null; page_state?: { value?: "content" | "login_or_signup_wall" | "consent_wall" | "challenge" | "error_or_not_found" | "rate_limited" | "paywall_teaser" | "empty_shell" | "other"; confidence?: number; skipped_judge?: boolean }; native?: { endpoint?: string; credits_used?: number; data?: unknown }; extraction_check?: { checked?: number; found_in_text?: number; confirmed?: number; removed?: ({ field?: string; value?: unknown; reason?: "placeholder" | "not_on_page" })[]; unverified?: string[] }; fetch?: { cache_state?: string | null; cached_at?: string | null; proxy_tier?: string | null } };
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
  ext?: { gid?: string | null; data_docid?: string | null; pvf?: string | null; seller_id?: string | null; sold_count?: number | null; bought_past_month?: number | null; bought_past_month_label?: string | null; catalog_id?: string | null; requested_id?: string | null; rating_distribution?: { star_1?: number | null; star_2?: number | null; star_3?: number | null; star_4?: number | null; star_5?: number | null } | null; store_inventory?: ({ store_id?: string | null; store_name?: string | null; state?: string | null; in_stock?: boolean | null; quantity?: number | null; fulfillment?: string | null; service?: string | null; location_type?: string | null; is_selected_store?: boolean | null })[] | null; promotion?: { label?: string | null; amount_off?: number | null; percent_off?: number | null } | null; price_note?: string | null; condition?: string | null; available_quantity?: number | null; watchers?: number | null; sold_at?: string | null; sold_caption?: string | null; buying_format?: string | null; seller_reputation?: { feedback_percentage?: number | null; feedback_count?: number | null; top_rated?: boolean | null; items_sold?: number | null; joined?: string | null; url?: string | null; detailed_ratings?: { accurate_description?: number | null; reasonable_shipping_cost?: number | null; shipping_speed?: number | null; communication?: number | null } | null } | null; g2?: { product_uuid?: string; solution_type?: string; ai_verified?: boolean; g2_reviews_link?: string; categories?: { name: string; link: string }[]; comparisons?: { link: string; name: string; logo: string; rating: number; reviews: number }[]; alternatives?: { name: string; link: string; logo: string; rating: number; reviews: number }[]; pricing_plans?: ({ plan_name: string; plan_price: string; price: number; billing: string | null; plan_description: string; plan_features: string[] })[]; pricing_details?: { free_trial: boolean; overview: string; last_updated: string; faqs: { question: string; answer: string }[]; alternatives_pricing: ({ product: string; plan: string; price: string; billing: string; description: string | null; features: string[] })[] }; features?: { name: string; features: string[] }[]; detailed_features?: ({ name: string; features: ({ name: string; content: string; percentage?: string | null; based_on_number_of_reviews?: number })[] })[]; pros?: string[]; cons?: string[]; pros_details?: { name: string; highlight: string; description: string; mentions: number; reviews_link: string; related_reviews: { reviewer: string; company_size: string; rating: number; title: string; question: string; content: string }[] }[]; cons_details?: { name: string; highlight: string; description: string; mentions: number; reviews_link: string; related_reviews: { reviewer: string; company_size: string; rating: number; title: string; question: string; content: string }[] }[]; integrations?: { count: number; items: { name: string; link: string }[] } } | null; etsy?: { is_handmade?: boolean; favorites?: number; is_bestseller?: boolean; is_top_rated?: boolean; materials?: string[]; taxonomy_path?: string; when_made?: string; user_id?: string } | null; sephora?: { sku?: string; size?: string; ingredients?: string; loves_count?: number } | null; hm?: { color?: string; category_code?: string; sizes?: string[]; new_arrival?: boolean } | null; kohls?: { colors?: string[]; display_color?: string; sku?: string; coupon_eligible?: boolean; ship?: boolean } | null; gumtree?: { user_id?: string; public_user_id?: string; account_id?: string; seller_type?: string; category_id?: string; category?: string; location?: string; location_id?: string } | null; sku_id?: string | null; aliexpress?: { commission_rate?: string; discount?: string; category?: string; subcategory?: string; positive_rate?: string; shop_url?: string } | null; tiktokshop?: { category?: string; category_id?: string; discount_percent?: number; stock?: number; seller_name?: string; seller_location?: string; seller_rating?: number; seller_products_count?: number; seller_followers?: number; seller_sold_count?: number; shop_identity?: string; shop_performance_percentile?: number; positive_feedback_percent?: number; response_rate_24h?: number; free_shipping?: boolean; shipping_fee?: number; delivery_estimate?: string; delivery_days_min?: number; delivery_days_max?: number; shop_id?: string; shop_name?: string; shop_url?: string; shop_rating?: number; shop_region?: string; shop_followers?: number; shop_products_count?: number; shop_reviews_count?: number; shop_sold_count?: number; shop_videos_count?: number; shop_logo_url?: string; trust_label?: string; promotion_labels?: string[] } | null } | null;
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
  ext?: { appdata?: { type?: string; rank_group?: number; rank_absolute?: number; position?: string; id?: string; version?: string | null; rating?: { rating_type: string; value: number; votes_count: number | null; rating_max: number }; timestamp?: string; title?: string | null; review_text?: string; user_profile?: { profile_name: string; profile_image_url: string | null }; entity_id?: string; helpful_count?: number | null; responses?: ({ author: string; title: string | null; text: string; timestamp: string })[] | null } | null; tiktokshop?: { reviewer_id?: string; is_incentivized_review?: boolean; sku_specification?: string } | null; naver?: { visit_count?: number | null; verified_by?: string | null; treatment?: string | null; view_count?: number | null; keywords?: string[] | null; dedupe_key?: string | null } | null; traveler_type?: string | null; stay_check_in?: string | null; stay_check_out?: string | null; stay_nights?: number | null; room_type?: string | null } | null;
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
  ext?: { distance?: number | null; status?: string | null; timezone?: string | null; hours?: ({ date?: string | null; day_name?: string | null; is_open?: boolean | null; opens_at?: string | null; closes_at?: string | null })[] | null; place_id?: string | null; attributes?: { available_attributes?: Record<string, unknown>; unavailable_attributes?: Record<string, unknown> } | null; rating_distribution?: Record<string, unknown> | null; people_also_search?: ({ cid?: string | null; title?: string | null; rating?: { value?: number | null; votes_count?: number | null } | null })[] | null; menu_url?: string | null; domain?: string | null; maps_url?: string | null; rank?: number | null; city?: string | null; postal_code?: string | null; region?: string | null; country_code?: string | null; posts_count?: number | null; website?: string | null; facebook_places_id?: string | null; business_username?: string | null; is_ad?: boolean | null; ad_rank?: number | null; ad_description?: string | null; status_description?: string | null; visitor_reviews_count?: number | null; blog_reviews_count?: number | null; booking_url?: string | null; keywords?: string[] | null; category_ratings?: ({ category?: string | null; label?: string | null; value?: number | null; max?: number | null })[] | null; room_type?: string | null; capacity?: number | null; subtitle?: string | null; listing_badges?: string[] | null; exact_location?: boolean | null; listing_price_note?: string | null; host_profile?: { id?: string | null; name?: string | null; avatar_url?: string | null; superhost?: boolean | null; verified?: boolean | null; years_hosting?: number | null; months_hosting?: number | null; response_rate?: string | null; response_time?: string | null; about?: string | null; highlights?: string[] | null } | null; rooms?: ({ name?: string | null; description?: string | null; size_sqm?: number | null; occupancy?: number | null; bed_configuration?: string | null; image_urls?: string[] | null })[] | null; languages_spoken?: string[] | null } | null;
}

export interface PlaceList {
  items: { place: Place }[];
  next_cursor?: string | null;
  total?: number | null;
}

export interface App {
  id?: string;
  store?: "google_play" | "app_store";
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
  rank?: number | null;
  ext?: { appdata?: { type?: string; rank_group?: number; rank_absolute?: number; position?: string; app_id?: string; title?: string; subtitle?: string; url?: string; icon?: string; description?: string; reviews_count?: number | null; rating?: { rating_type: string; value: number; votes_count: number | null; rating_max: number }; price?: { current: number; regular?: number | null; max_value?: number | null; currency?: string; is_price_range?: boolean; displayed_price?: string | null }; is_free?: boolean; main_category?: string | null; categories?: string[] | null; languages?: string[]; advisories?: string[]; developer?: string; developer_id?: string; developer_url?: string | null; developer_website?: string; developer_email?: string; developer_address?: string; version?: string | null; minimum_os_version?: string | null; size?: string | null; released_date?: string | null; last_update_date?: string; time_update?: string; update_notes?: string | null; images?: string[]; videos?: string[] | null; similar_apps?: { app_id: string; title: string; url: string }[]; more_apps_by_developer?: { app_id: string; title: string; url: string }[] | null; installs?: string; installs_count?: number; genres?: string[]; tags?: string[]; category_drift_probe?: boolean } | null } | null;
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
  type?: "stock" | "etf" | "index" | "crypto" | "forex" | "futures" | "fund" | "unknown";
  url?: string | null;
  currency?: string | null;
  pair?: { base_symbol?: string | null; quote_symbol?: string | null; base_display_name?: string | null; quote_display_name?: string | null } | null;
  price?: { current?: number | null; previous_close?: number | null; delta?: number | null; percentage_delta?: number | null; trend?: "up" | "down" | "stable" | null; day_low?: number | null; day_high?: number | null; year_low?: number | null; year_high?: number | null; timestamp?: string | null };
  metrics?: { market_cap?: number | null; volume?: number | null; avg_volume?: number | null; pe_ratio?: number | null; dividend_yield?: number | null; ytd_return?: number | null; expense_ratio?: number | null; net_assets?: number | null; yield?: number | null; open_interest?: number | null; category?: string | null; metrics_currency?: string | null } | null;
  about?: { description?: string | null; description_source_url?: string | null; ceo?: string | null; founded?: string | null; headquarters?: string | null; website?: string | null; employees?: number | null } | null;
  graph?: ({ timestamp?: string; value?: number; volume?: number | null })[] | null;
  financials?: { quarterly?: ({ type?: string; timestamp: string; revenue?: number | null; revenue_delta?: number | null; operating_expense?: number | null; operating_expense_delta?: number | null; net_income?: number | null; net_income_delta?: number | null; net_profit_margin?: number | null; net_profit_margin_delta?: number | null; earnings_per_share?: number | null; earnings_per_share_delta?: number | null; ebitda?: number | null; ebitda_delta?: number | null; cash_and_short_term_investments?: number | null; cash_and_short_term_investments_delta?: number | null; total_assets?: number | null; total_assets_delta?: number | null; total_liabilities?: number | null; total_liabilities_delta?: number | null; cash_from_operations?: number | null; cash_from_operations_delta?: number | null; cash_from_investing?: number | null; cash_from_investing_delta?: number | null; cash_from_financing?: number | null; cash_from_financing_delta?: number | null; net_change_in_cash?: number | null; net_change_in_cash_delta?: number | null; free_cash_flow?: number | null; free_cash_flow_delta?: number | null; effective_tax_rate?: number | null; total_equity?: number | null; shares_outstanding?: number | null; price_to_book?: number | null; return_on_assets?: number | null; return_on_capital?: number | null })[] | null; annual?: ({ type?: string; timestamp: string; revenue?: number | null; revenue_delta?: number | null; operating_expense?: number | null; operating_expense_delta?: number | null; net_income?: number | null; net_income_delta?: number | null; net_profit_margin?: number | null; net_profit_margin_delta?: number | null; earnings_per_share?: number | null; earnings_per_share_delta?: number | null; ebitda?: number | null; ebitda_delta?: number | null; cash_and_short_term_investments?: number | null; cash_and_short_term_investments_delta?: number | null; total_assets?: number | null; total_assets_delta?: number | null; total_liabilities?: number | null; total_liabilities_delta?: number | null; cash_from_operations?: number | null; cash_from_operations_delta?: number | null; cash_from_investing?: number | null; cash_from_investing_delta?: number | null; cash_from_financing?: number | null; cash_from_financing_delta?: number | null; net_change_in_cash?: number | null; net_change_in_cash_delta?: number | null; free_cash_flow?: number | null; free_cash_flow_delta?: number | null; effective_tax_rate?: number | null; total_equity?: number | null; shares_outstanding?: number | null; price_to_book?: number | null; return_on_assets?: number | null; return_on_capital?: number | null })[] | null } | null;
  peers?: ({ id?: string; ticker?: string | null; exchange?: string | null; name?: string | null; type?: "stock" | "etf" | "index" | "crypto" | "forex" | "futures" | "fund" | "unknown"; url?: string | null; currency?: string | null; pair?: { base_symbol?: string | null; quote_symbol?: string | null; base_display_name?: string | null; quote_display_name?: string | null } | null; price?: { current?: number | null; previous_close?: number | null; delta?: number | null; percentage_delta?: number | null; trend?: "up" | "down" | "stable" | null; day_low?: number | null; day_high?: number | null; year_low?: number | null; year_high?: number | null; timestamp?: string | null }; metrics?: { market_cap?: number | null; volume?: number | null; avg_volume?: number | null; pe_ratio?: number | null; dividend_yield?: number | null; ytd_return?: number | null; expense_ratio?: number | null; net_assets?: number | null; yield?: number | null; open_interest?: number | null; category?: string | null; metrics_currency?: string | null } | null })[] | null;
  ext?: { section?: string } | null;
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
export type PrismDiscoverResponse = ApiResponse<Analytics>;
export type PrismCreatorsResponse = ApiResponse<Analytics>;
export type InstagramSearchReelsResponse = ApiResponse<PostList>;
export type InstagramProfileAboutResponse = ApiResponse<Author>;
export type PrismCreatorVetResponse = ApiResponse<Analytics>;
export type YoutubeChannelAboutResponse = ApiResponse<Author>;
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
