"""SocialCrawl response types. Generated from the canonical schemas
(packages/social-api/src/schemas/canonical.ts); do not edit.

Every response is a `<Archetype>Response` (success) or `ApiErrorBody`. A canonical object
(Comment, Post, Author, ...) is the same shape on every platform; a list is
`{"items": [{"<row key>": Object}], "next_cursor"?, "total"?}` with `pagination` at the
envelope root. Response types are named after the endpoint id, for the endpoints the recipes
use. All keys are optional (total=False): check before you index. Python 3.8+.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union


class Pagination(TypedDict, total=False):
    next_cursor: Optional[str]
    has_more: bool
    page_size: int
    stopped_at: Optional[Literal["since", "known_id", "end"]]
    typical_page_size: Optional[int]
    next_page_credits: Optional[int]


class ApiErrorDetail(TypedDict, total=False):
    type: str
    message: str
    status: int
    doc_url: str
    retryable: bool
    # Structured context: next_step says what to do next; a missing one-of group is named in fields.
    details: Dict[str, Any]


class ApiErrorBody(TypedDict, total=False):
    success: bool
    error: ApiErrorDetail
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str


class AuthorExtContactsItemVerification(TypedDict, total=False):
    syntax: bool
    mx: Optional[bool]
    disposable: bool
    role_account: bool

class AuthorExtContactsItemSourcesItem(TypedDict, total=False):
    tier: Literal["bio", "bio_link", "caption", "external_url", "about", "instagram_panel", "video_description", "link_in_bio", "website", "button"]
    url: str
    snippet: str
    first_seen: str
    last_seen: str

class AuthorExtContactsItem(TypedDict, total=False):
    kind: Literal["email"]
    value: str
    role: Literal["own", "management", "agency"]
    confidence: float
    provenance: Literal["published", "gated_reveal"]
    verification: AuthorExtContactsItemVerification
    sources: List[AuthorExtContactsItemSourcesItem]

class AuthorExtBioLinksItem(TypedDict, total=False):
    title: Optional[str]
    url: Optional[str]
    link_type: Optional[str]

class AuthorExtEmployeeCountRange(TypedDict, total=False):
    start: Optional[float]
    end: Optional[float]

class AuthorExtHeadquarters(TypedDict, total=False):
    country: Optional[str]
    city: Optional[str]
    geographic_area: Optional[str]
    line1: Optional[str]
    postal_code: Optional[str]
    label: Optional[str]

class AuthorExtLocationsItemAddress(TypedDict, total=False):
    country: Optional[str]
    city: Optional[str]
    geographic_area: Optional[str]
    line1: Optional[str]
    line2: Optional[str]
    postal_code: Optional[str]

class AuthorExtLocationsItemLatLong(TypedDict, total=False):
    latitude: Optional[float]
    longitude: Optional[float]

class AuthorExtLocationsItem(TypedDict, total=False):
    name: Optional[str]
    address: AuthorExtLocationsItemAddress
    lat_long: AuthorExtLocationsItemLatLong
    label: Optional[str]
    is_headquarters: Optional[bool]

class AuthorExtHashtagsItem(TypedDict, total=False):
    name: str
    follower_count: Optional[float]

class AuthorExtFundingLastFundingRound(TypedDict, total=False):
    money_raised: Any
    announced_on: Any

class AuthorExtFunding(TypedDict, total=False):
    last_funding_round: AuthorExtFundingLastFundingRound

class AuthorExtFoundedOn(TypedDict, total=False):
    year: Optional[float]
    month: Optional[float]
    day: Optional[float]

class AuthorExtLinksItem(TypedDict, total=False):
    id: str
    type: str
    title: str
    url: str
    clicks: float
    order: Optional[float]

class AuthorExtCurrentPosition(TypedDict, total=False):
    title: Optional[str]
    company: Optional[str]
    company_id: Optional[str]
    company_username: Optional[str]
    company_url: Optional[str]

class AuthorExtCurrentSchool(TypedDict, total=False):
    name: Optional[str]
    school_id: Optional[str]
    company_id: Optional[str]
    username: Optional[str]
    url: Optional[str]

class AuthorExtVerificationsItem(TypedDict, total=False):
    type: Optional[str]
    label: Optional[str]
    detail: Optional[str]

class AuthorExtProfileActionsItem(TypedDict, total=False):
    label: Optional[str]
    url: Optional[str]

class AuthorExtRelatedPlaylists(TypedDict, total=False):
    uploads: str
    likes: str

class AuthorExtRulesItem(TypedDict, total=False):
    id: str
    rest_id: str
    name: str
    description: str

class AuthorExtSocialLinksItem(TypedDict, total=False):
    title: str
    type: str
    url: str

class AuthorExtGroupAdministratorsItem(TypedDict, total=False):
    id: str
    name: str
    url: str
    profile_picture_url: str

class AuthorExtGroupModeratorsItem(TypedDict, total=False):
    id: str
    name: str
    url: str
    profile_picture_url: str

class AuthorExtGroupActivity(TypedDict, total=False):
    posts_last_day: float
    posts_last_month: float
    new_members_text: str

class AuthorExtGroupAboutInfoItem(TypedDict, total=False):
    type: str
    label: str
    description: str

class AuthorExtGroup(TypedDict, total=False):
    privacy_label: str
    privacy_description: str
    visibility_label: str
    visibility_description: str
    member_count_text: str
    administrator_count: float
    moderator_count: float
    history_summary: str
    categories: List[str]
    rules: List[Any]
    administrators: List[AuthorExtGroupAdministratorsItem]
    moderators: List[AuthorExtGroupModeratorsItem]
    activity: AuthorExtGroupActivity
    about_info: List[AuthorExtGroupAboutInfoItem]

class AuthorExtSearchHit(TypedDict, total=False):
    match: Optional[str]
    title: Optional[str]
    snippet: Optional[str]
    evidence_url: Optional[str]
    matched_urls: Optional[List[str]]

class AuthorExt(TypedDict, total=False):
    social_context: Optional[str]
    account_based_in: Optional[str]
    signup_source: Optional[str]
    username_changes: Optional[float]
    username_last_changed_at: Optional[str]
    location_accurate: Optional[bool]
    created_country_accurate: Optional[bool]
    affiliate_username: Optional[str]
    media_count: Optional[float]
    likes_given: Optional[float]
    creator_subscriptions_count: Optional[float]
    verified_blue: Optional[bool]
    verified_legacy: Optional[bool]
    identity_verified: Optional[bool]
    verification_reason: Optional[str]
    instagram_followers: Optional[float]
    instagram_verified: Optional[bool]
    page_verification: Optional[str]
    page_category: Optional[str]
    entity_type: Optional[str]
    is_political_page: Optional[bool]
    page_is_restricted: Optional[bool]
    verified_name: Optional[str]
    verified_country_code: Optional[str]
    advertiser_name: Optional[str]
    registered_location: Optional[str]
    advertiser_sponsor: Optional[str]
    follower_count_text: Optional[str]
    countries_shown: Optional[List[str]]
    ad_count: Optional[float]
    gender: Optional[str]
    birthday: Optional[str]
    verified_reason: Optional[str]
    ip_location: Optional[str]
    verified_type: Optional[float]
    hometown: Optional[str]
    employer: Optional[str]
    credit_level: Optional[str]
    activity_summary: Optional[str]
    account_created: Optional[str]
    country: Optional[str]
    country_name: Optional[str]
    collects_received: Optional[float]
    former_usernames: Optional[List[str]]
    former_usernames_count: Optional[int]
    verified_at: Optional[str]
    is_memorialized: Optional[bool]
    public_email: Optional[str]
    contacts: Optional[List[AuthorExtContactsItem]]
    contact_email: Optional[str]
    public_phone: Optional[str]
    similar_source: Optional[str]
    instagram_username: Optional[str]
    similar_via: Optional[str]
    business_category: Optional[str]
    bio_links: Optional[List[AuthorExtBioLinksItem]]
    is_business: Optional[bool]
    is_professional: Optional[bool]
    address_latitude: Optional[float]
    address_longitude: Optional[float]
    pronouns: Optional[List[str]]
    has_highlights: Optional[bool]
    threads_username: Optional[str]
    latest_story_at: Optional[str]
    creator_marketplace: Optional[bool]
    verification_label: Optional[str]
    fbid: Optional[str]
    hd_avatar_url: Optional[str]
    website: Optional[str]
    cover_url: Optional[str]
    page_active: Optional[bool]
    employee_count: Optional[float]
    employee_count_range: Optional[AuthorExtEmployeeCountRange]
    founded_year: Optional[float]
    company_type: Optional[str]
    tagline: Optional[str]
    specialities: Optional[List[str]]
    industries: Optional[List[str]]
    headquarters: Optional[AuthorExtHeadquarters]
    locations: Optional[List[AuthorExtLocationsItem]]
    hashtags: Optional[List[AuthorExtHashtagsItem]]
    funding: Optional[AuthorExtFunding]
    founded_on: Optional[AuthorExtFoundedOn]
    company_type_code: Optional[str]
    page_type: Optional[str]
    domain: Optional[str]
    is_claimable: Optional[bool]
    is_archived: Optional[bool]
    is_auto_generated: Optional[bool]
    verification_updated_at: Optional[str]
    call_to_action_url: Optional[str]
    industry_hierarchy: Optional[str]
    public_phone_extension: Optional[str]
    crunchbase_url: Optional[str]
    open_job_count: Optional[float]
    products: Any
    address: Optional[str]
    price_range: Optional[str]
    rating: Optional[str]
    rating_count: Optional[float]
    talking_about_count: Optional[float]
    business_hours: Any
    links: Optional[List[Union[str, AuthorExtLinksItem]]]
    ad_library_page_id: Optional[str]
    ad_library_status: Optional[str]
    urn: Optional[str]
    is_top_voice: Optional[bool]
    is_premium: Optional[bool]
    is_creator: Optional[bool]
    is_influencer: Optional[bool]
    is_open_to_work: Optional[bool]
    is_hiring: Optional[bool]
    member_id: Optional[str]
    joined_at_precision: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    pronoun: Optional[str]
    primary_locale: Optional[str]
    supported_locales: Optional[List[str]]
    about: Optional[str]
    about_localized: Optional[Dict[str, Any]]
    headline_localized: Optional[Dict[str, Any]]
    current_position: Optional[AuthorExtCurrentPosition]
    current_school: Optional[AuthorExtCurrentSchool]
    industry: Optional[str]
    industry_id: Optional[str]
    verifications: Optional[List[AuthorExtVerificationsItem]]
    geo_id: Optional[str]
    is_open_profile: Optional[bool]
    last_name_is_initial: Optional[bool]
    volunteer_causes: Optional[List[str]]
    top_skills: Optional[List[str]]
    profile_actions: Optional[List[AuthorExtProfileActionsItem]]
    section_totals: Optional[Dict[str, Any]]
    company_id: Optional[str]
    reaction_type: Optional[str]
    public_identifier: Optional[str]
    account_type: Optional[str]
    followers_approximate: Optional[bool]
    counts_source: Optional[str]
    posting_region: Optional[str]
    keywords: Optional[str]
    total_views: Optional[float]
    joined_at_timestamp: Optional[str]
    topicCategories: Optional[List[str]]
    bannerExternalUrl: Optional[str]
    madeForKids: Optional[bool]
    hiddenSubscriberCount: Optional[bool]
    related_playlists: Optional[AuthorExtRelatedPlaylists]
    topic_ids: Optional[List[str]]
    unsubscribed_trailer: Optional[str]
    localizations: Optional[Dict[str, Any]]
    monthly_listeners: Optional[float]
    total_ratings: Optional[float]
    average_rating: Optional[float]
    creator_username: Optional[str]
    join_policy: Optional[str]
    is_nsfw: Optional[bool]
    rules: Optional[List[AuthorExtRulesItem]]
    weekly_active_users: Optional[float]
    weekly_contributions: Optional[float]
    rules_text: Optional[str]
    language: Optional[str]
    post_karma: Optional[float]
    comment_karma: Optional[float]
    awardee_karma: Optional[float]
    trophy_count: Optional[float]
    banner_url: Optional[str]
    profile_title: Optional[str]
    social_links: Optional[List[AuthorExtSocialLinksItem]]
    bio_link: Optional[str]
    embed_html: Optional[str]
    embed_url: Optional[str]
    group: Optional[AuthorExtGroup]
    search_hit: Optional[AuthorExtSearchHit]
    blog_name: Optional[str]
    blog_no: Optional[str]
    visitors_today: Optional[float]
    visitors_total: Optional[float]
    topic: Optional[str]
    power_blog: Optional[bool]
    official_blog: Optional[bool]

class Author(TypedDict, total=False):
    id: str
    username: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    verified: Optional[bool]
    followers: Optional[float]
    following: Optional[float]
    posts_count: Optional[float]
    likes_count: Optional[float]
    url: Optional[str]
    location: Optional[str]
    external_url: Optional[str]
    private: Optional[bool]
    joined_at: Optional[str]
    last_post_at: Optional[str]
    ext: Optional[AuthorExt]

class AuthorListItemsItem(TypedDict, total=False):
    author: Author

class AuthorList(TypedDict, total=False):
    items: List[AuthorListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class PostContent(TypedDict, total=False):
    text: Optional[str]
    media_urls: Optional[Union[str, List[str]]]
    thumbnail_url: Optional[str]
    duration_seconds: Optional[float]

class PostAuthor(TypedDict, total=False):
    username: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    verified: Optional[bool]

class PostEngagement(TypedDict, total=False):
    views: Optional[float]
    likes: Optional[float]
    comments: Optional[float]
    shares: Optional[float]
    saves: Optional[float]

class PostFlags(TypedDict, total=False):
    nsfw: Optional[bool]
    spoiler: Optional[bool]
    pinned: Optional[bool]
    deleted: bool
    likes_hidden: Optional[bool]
    comments_hidden: Optional[bool]
    shares_hidden: Optional[bool]
    views_hidden: Optional[bool]
    saves_hidden: Optional[bool]

class PostExtCoauthorsItem(TypedDict, total=False):
    id: str
    username: str
    full_name: Optional[str]
    is_verified: bool
    profile_pic_url: str

class PostExtMusic(TypedDict, total=False):
    id: str
    track_title: Optional[str]
    artist: Optional[str]
    is_original: bool

class PostExtLocation(TypedDict, total=False):
    id: Optional[str]
    name: Optional[str]
    lat: Optional[float]
    lng: Optional[float]

class PostExtMediaItem(TypedDict, total=False):
    type: Literal["image", "video"]
    url: Optional[str]
    width: Optional[float]
    height: Optional[float]

class PostExtTopCommentsItem(TypedDict, total=False):
    id: Optional[str]
    text: Optional[str]
    username: Optional[str]
    likes: Optional[float]
    published_at: Optional[str]

class PostExtQuotedPostAuthor(TypedDict, total=False):
    id: str
    username: str
    display_name: str
    verified: bool

class PostExtQuotedPostEngagement(TypedDict, total=False):
    views: float
    likes: float
    comments: float
    shares: float
    saves: float

class PostExtQuotedPost(TypedDict, total=False):
    id: str
    url: str
    author: PostExtQuotedPostAuthor
    text: Optional[str]
    media_urls: Optional[List[str]]
    thumbnail_url: Optional[str]
    engagement: PostExtQuotedPostEngagement
    published_at: str
    quote_count: float

class PostExtRetweetedPostAuthor(TypedDict, total=False):
    id: str
    username: str
    display_name: str
    verified: bool

class PostExtRetweetedPostEngagement(TypedDict, total=False):
    views: float
    likes: float
    comments: float
    shares: float
    saves: float

class PostExtRetweetedPost(TypedDict, total=False):
    id: str
    url: str
    author: PostExtRetweetedPostAuthor
    text: Optional[str]
    media_urls: Optional[List[str]]
    thumbnail_url: Optional[str]
    engagement: PostExtRetweetedPostEngagement
    published_at: str
    quote_count: float

class PostExtReactionCountsItem(TypedDict, total=False):
    type: str
    count: float
    emoji: Optional[str]
    emoji_id: Optional[str]
    count_text: str

class PostExtArticle(TypedDict, total=False):
    title: str
    source: str
    url: str
    description: str

class PostExtMentionedAccountsItem(TypedDict, total=False):
    type: Optional[str]
    id: Optional[str]
    name: Optional[str]
    username: Optional[str]
    url: Optional[str]

class PostExtTextEntitiesItem(TypedDict, total=False):
    start: Optional[float]
    length: Optional[float]
    type: Optional[str]
    id: Optional[str]
    url: Optional[str]

class PostExtDocument(TypedDict, total=False):
    title: Optional[str]
    page_count: Optional[float]
    url: Optional[str]
    cover_url: Optional[str]

class PostExtPollOptionsItem(TypedDict, total=False):
    text: Optional[str]
    votes: Optional[float]

class PostExtPoll(TypedDict, total=False):
    question: Optional[str]
    options: List[PostExtPollOptionsItem]
    total_votes: Optional[float]
    voter_count: Optional[float]
    is_closed: Optional[bool]
    remaining: Optional[str]

class PostExtJob(TypedDict, total=False):
    id: Optional[str]
    title: Optional[str]
    company_name: Optional[str]
    company_id: Optional[str]
    company_url: Optional[str]
    company_logo: Optional[str]
    location: Optional[str]
    url: Optional[str]

class PostExtCelebration(TypedDict, total=False):
    headline: Optional[str]
    image_url: Optional[str]

class PostExtNewsletter(TypedDict, total=False):
    title: Optional[str]
    url: Optional[str]

class PostExtRepostedBy(TypedDict, total=False):
    type: Optional[str]
    id: Optional[str]
    name: Optional[str]
    username: Optional[str]
    url: Optional[str]

class PostExtContentCredentials(TypedDict, total=False):
    is_ai_generated: Optional[bool]
    issuer: Optional[str]
    signer: Optional[str]
    is_valid: Optional[bool]

class PostExtDownloadMediaUrlsItem(TypedDict, total=False):
    post_id: str
    cdn_url: str
    type: str
    cached: bool

class PostExtPlaybackAvailability(TypedDict, total=False):
    visibility: Optional[str]
    age_restricted: Optional[bool]
    members_only: Optional[bool]
    family_safe: Optional[bool]
    region_restricted: Optional[bool]
    available_countries: Optional[List[str]]
    live_content: Optional[bool]
    live_now: Optional[bool]
    upcoming: Optional[bool]
    comments_visible: Optional[bool]
    ratings_enabled: Optional[bool]

class PostExtCommercePricePromotionDeductionDetails(TypedDict, total=False):
    seller_subtotal_deduction: str
    seller_subtotal_deduction_decimal: str

class PostExtCommercePrice(TypedDict, total=False):
    sku_id: str
    current: float
    original: float
    currency: str
    discount_percent: float
    currency_name: str
    currency_symbol: str
    symbol_position: float
    show_currency_space: bool
    currency_show_mode: float
    sale_price_decimal: str
    origin_price_decimal: str
    sale_price_format: str
    origin_price_format: str
    discount_format: str
    discount_decimal: str
    single_product_price_format: str
    single_product_price_decimal: str
    sale_price_integer_part_format: str
    sale_price_decimal_part_format: str
    decimal_point_symbol: str
    promotion_deduction_details: PostExtCommercePricePromotionDeductionDetails

class PostExtCommerceAttributesItem(TypedDict, total=False):
    attribute_name: str
    value: str
    label: str

class PostExtCommerceRating(TypedDict, total=False):
    score: float
    review_count: float
    average: float
    count: float

class PostExtCommerceSold(TypedDict, total=False):
    sold_count: float

class PostExtCommerce(TypedDict, total=False):
    price: Union[float, PostExtCommercePrice]
    currency: str
    price_formatted: str
    strikethrough_price_formatted: str
    description: str
    location_text: str
    latitude: float
    longitude: float
    category_id: str
    mileage: Optional[float]
    attributes: List[PostExtCommerceAttributesItem]
    delivery_types: List[str]
    availability_text: Optional[str]
    listing_date_text: str
    is_sold: bool
    is_live: bool
    is_pending: bool
    is_hidden: bool
    is_shipping_offered: bool
    is_buy_now_enabled: bool
    messaging_enabled: bool
    seller_id: Optional[str]
    seller_name: Optional[str]
    rating: PostExtCommerceRating
    sold: PostExtCommerceSold

class PostExtAmazonShopListsItem(TypedDict, total=False):
    title: str
    itemCount: float
    image: str
    url: str

class PostExtAmazonShopTrendingPicksItem(TypedDict, total=False):
    url: str
    image: str
    price: float
    discount: Optional[str]

class PostExtAmazonShopCurationsItem(TypedDict, total=False):
    title: str
    postCount: float
    image: str
    url: str

class PostExtAdObjectivesItem(TypedDict, total=False):
    label: str
    value: Optional[str]

class PostExtAd(TypedDict, total=False):
    page_id: str
    page_profile_uri: str
    page_like_count: float
    page_categories: List[str]
    brand_name: str
    currency: str
    spend: Any
    spent: str
    reach_estimate: Any
    estimated_audience: str
    publisher_platforms: List[str]
    categories: List[str]
    targeted_or_reached_countries: List[str]
    country_code: Union[str, List[str]]
    cta_text: str
    cta_type: str
    link_url: str
    landing_page: str
    landing_page_url: Optional[str]
    profile_web_link: str
    is_active: bool
    end_date_iso: str
    last_shown_date: float
    display_format: str
    ad_format: Optional[str]
    title: str
    caption: str
    video_hd_url: Optional[str]
    video_sd_url: Optional[str]
    video_url_540p: str
    video_url_360p: str
    video_id: str
    image_urls: List[str]
    audit_status: str
    type: str
    source: str
    objectives: List[PostExtAdObjectivesItem]
    objective: str
    industry: str
    language: Optional[str]
    ctr: float
    cost_score: float
    rank: float
    like_tier: Optional[str]
    is_spark_ad: Optional[bool]
    period_days: float

class PostExtAppleMusicGenresItem(TypedDict, total=False):
    id: str
    name: str

class PostExtAppleMusic(TypedDict, total=False):
    kind: str
    track_count: float
    release_info: str
    artist_url: str
    artist_id: str
    release_date: str
    genres: List[PostExtAppleMusicGenresItem]
    content_advisory: Optional[str]
    track_number: float
    explicit: bool

class PostExtEventHostsItem(TypedDict, total=False):
    id: str
    name: str
    url: str
    profile_picture_url: str
    type: str
    is_verified: bool

class PostExtEvent(TypedDict, total=False):
    description: str
    start_timestamp: float
    end_timestamp: Optional[float]
    time_text: str
    duration_text: str
    location_name: str
    address: Optional[str]
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    hosts: List[PostExtEventHostsItem]
    host_context_text: str
    category: str
    is_online: bool
    is_canceled: bool
    is_past: bool
    privacy: str
    ticket_url: Optional[str]
    attendance_count: float
    interested_count: float
    going_count: float
    id: Optional[str]
    name: Optional[str]
    date_text: Optional[str]
    location: Optional[str]
    url: Optional[str]
    banner_url: Optional[str]

class PostExtTrendBoardsItem(TypedDict, total=False):
    industry: Optional[str]
    industry_id: Optional[str]
    industry_label: Optional[str]
    rank: float

class PostExtTrendPopularityCurveItem(TypedDict, total=False):
    date: str
    value: float

class PostExtTrendTopCreatorsItem(TypedDict, total=False):
    username: str
    display_name: str
    followers: float
    country_code: str
    url: str

class PostExtTrend(TypedDict, total=False):
    rank: float
    country_code: str
    chart: str
    chart_title: str
    updated_at: str
    period_days: float
    posts: float
    views: float
    period_views: float
    organic_views: float
    six_second_view_through_rate: float
    engagement_rate: float
    order_by: str
    industry: Optional[str]
    industry_id: Optional[str]
    industry_label: Optional[str]
    boards: List[PostExtTrendBoardsItem]
    popularity_curve: List[PostExtTrendPopularityCurveItem]
    top_creators: List[PostExtTrendTopCreatorsItem]
    content_tags: List[str]

class PostExtGroup(TypedDict, total=False):
    id: str
    url: str
    name: Optional[str]
    members: Optional[float]

class PostExt(TypedDict, total=False):
    music_id: Optional[str]
    matched_song_id: Optional[str]
    matched_song_title: Optional[str]
    matched_song_artist: Optional[str]
    music_title: Optional[str]
    music_artist: Optional[str]
    music_is_original: Optional[bool]
    author_id: Optional[str]
    author_url: Optional[str]
    author_followers: Optional[float]
    author_following: Optional[float]
    author_posts_count: Optional[float]
    author_location: Optional[str]
    in_reply_to_id: Optional[str]
    in_reply_to_username: Optional[str]
    conversation_id: Optional[str]
    author_country: Optional[str]
    author_public_email: Optional[str]
    author_public_phone: Optional[str]
    download_count: Optional[float]
    region: Optional[str]
    counts_approximate: Optional[bool]
    ran_as_ad: Optional[bool]
    tagged_products: Optional[List[Any]]
    subreddit: Optional[str]
    title: Optional[str]
    selftext: Optional[str]
    link_domain: Optional[str]
    upvote_ratio: Optional[float]
    flair: Optional[str]
    content_language: Optional[str]
    removed: Optional[bool]
    removed_by: Optional[str]
    type: Optional[str]
    content_type: Optional[str]
    ticker_symbols: Optional[List[str]]
    video_view_count: Optional[float]
    ig_play_count: Optional[float]
    repost_count: Optional[float]
    media_type: Optional[str]
    text_truncated: Optional[bool]
    ip_location: Optional[str]
    carousel_count: Optional[float]
    remix_count: Optional[float]
    audio_cluster_id: Optional[str]
    facebook_likes: Optional[float]
    facebook_comments: Optional[float]
    instagram_views: Optional[float]
    facebook_views: Optional[float]
    published_at_epoch: Optional[float]
    usertags: Optional[List[str]]
    coauthors: Optional[List[PostExtCoauthorsItem]]
    music: Optional[PostExtMusic]
    use_count: Optional[float]
    use_count_unit: Optional[str]
    shares_source: Optional[str]
    engagement_source: Optional[str]
    sponsor_tags: Optional[List[str]]
    sponsored_disclosed: Optional[bool]
    ai_label: Optional[str]
    story_mentions: Optional[List[str]]
    story_links: Optional[List[str]]
    story_reshared_posts: Optional[List[str]]
    location: Optional[PostExtLocation]
    media: Optional[List[PostExtMediaItem]]
    top_comments: Optional[List[PostExtTopCommentsItem]]
    hashtags: Optional[List[str]]
    mentions: Optional[List[str]]
    mentioned_user_ids: Optional[List[str]]
    quoted_post: Optional[PostExtQuotedPost]
    retweeted_post: Optional[PostExtRetweetedPost]
    quote_count: Optional[float]
    all_media_urls: Optional[List[str]]
    reaction_counts: Optional[List[PostExtReactionCountsItem]]
    share_urn: Optional[str]
    post_type: Optional[str]
    activity_id: Optional[str]
    published_at_precision: Optional[str]
    author_urn: Optional[str]
    author_headline: Optional[str]
    author_type: Optional[str]
    is_repost_quote: Optional[bool]
    article: Optional[PostExtArticle]
    reaction_type: Optional[str]
    reacted_at: Optional[str]
    reaction: Optional[str]
    reaction_activity_id: Optional[str]
    mentioned_accounts: Optional[List[PostExtMentionedAccountsItem]]
    text_entities: Optional[List[PostExtTextEntitiesItem]]
    outbound_links: Optional[List[str]]
    is_edited: Optional[bool]
    comments_disabled: Optional[bool]
    document: Optional[PostExtDocument]
    poll: Optional[PostExtPoll]
    job: Optional[PostExtJob]
    celebration: Optional[PostExtCelebration]
    newsletter: Optional[PostExtNewsletter]
    reposted_by: Optional[PostExtRepostedBy]
    reposted_at: Optional[str]
    author_website: Optional[str]
    author_website_label: Optional[str]
    aspect_ratio: Optional[float]
    author_is_premium: Optional[bool]
    content_credentials: Optional[PostExtContentCredentials]
    download_media_urls: Optional[List[PostExtDownloadMediaUrlsItem]]
    tags: Optional[List[str]]
    categoryId: Optional[str]
    categoryTitle: Optional[str]
    topicCategories: Optional[List[str]]
    duration: Optional[str]
    license: Optional[str]
    madeForKids: Optional[bool]
    defaultAudioLanguage: Optional[str]
    hasPaidProductPlacement: Optional[bool]
    caption: Optional[str]
    playback_availability: Optional[PostExtPlaybackAvailability]
    position: Optional[float]
    playlistId: Optional[str]
    videoOwnerChannelId: Optional[str]
    videoPublishedAt: Optional[str]
    description: Optional[str]
    default_language: Optional[str]
    localizations: Optional[Dict[str, Any]]
    playlist_item_id: Optional[str]
    playlist_owner_channel_id: Optional[str]
    playlist_owner_title: Optional[str]
    channel_id: Optional[str]
    published_label: Optional[str]
    published_precision: Optional[str]
    title_maybe_translated: Optional[bool]
    video_count: Optional[float]
    posts_count: Optional[float]
    commerce: Optional[PostExtCommerce]
    on_screen_texts: Optional[List[str]]
    topic_tag: Optional[str]
    reshare_count: Optional[float]
    dsp_ids: Optional[Dict[str, Any]]
    topic_tag_id: Optional[str]
    amazon_shop_lists: Optional[List[PostExtAmazonShopListsItem]]
    amazon_shop_trending_picks: Optional[List[PostExtAmazonShopTrendingPicksItem]]
    amazon_shop_curations: Optional[List[PostExtAmazonShopCurationsItem]]
    amazon_shop_socials: Optional[List[str]]
    ad: Optional[PostExtAd]
    apple_music: Optional[PostExtAppleMusic]
    feedback_id: Optional[str]
    question_id: Optional[str]
    answer_no: Optional[float]
    answer_nos: Optional[List[float]]
    published_at_est: Optional[str]
    date_basis: Optional[str]
    event: Optional[PostExtEvent]
    trend: Optional[PostExtTrend]
    updated_at: Optional[str]
    alt_text: Optional[str]
    board_name: Optional[str]
    topic_labels: Optional[List[str]]
    story_expires_at: Optional[str]
    numeric_id: Optional[float]
    outbound_url: Optional[str]
    group: Optional[PostExtGroup]

class Post(TypedDict, total=False):
    id: str
    url: Optional[str]
    content: PostContent
    author: PostAuthor
    engagement: PostEngagement
    flags: PostFlags
    published_at: Optional[Union[str, float]]
    ext: Optional[PostExt]

class PostListItemsItemComputedRelevance(TypedDict, total=False):
    p: float
    sense: Literal["target", "other_named_thing", "generic_word", "not_present"]
    depth: float
    spam: float

class PostListItemsItemComputed(TypedDict, total=False):
    engagement_rate: Optional[float]
    language: Optional[str]
    content_category: Optional[str]
    estimated_reach: Optional[float]
    save_rate: Optional[float]
    relevance: Optional[PostListItemsItemComputedRelevance]
    labels: Optional[Dict[str, Any]]
    labels_evidence: Optional[Dict[str, Any]]

class PostListItemsItem(TypedDict, total=False):
    post: Post
    computed: PostListItemsItemComputed

class PostList(TypedDict, total=False):
    items: List[PostListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class CommentAuthor(TypedDict, total=False):
    username: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    verified: Optional[bool]

class CommentEngagement(TypedDict, total=False):
    likes: Optional[float]
    replies: Optional[float]

class CommentFlags(TypedDict, total=False):
    pinned: Optional[bool]
    deleted: bool
    liked_by_creator: Optional[bool]

class CommentExtReactionCountsItem(TypedDict, total=False):
    type: str
    count: float

class CommentExtPreviewRepliesItemAuthorChannelId(TypedDict, total=False):
    value: str

class CommentExtPreviewRepliesItem(TypedDict, total=False):
    id: str
    channelId: str
    videoId: str
    textDisplay: str
    textOriginal: str
    parentId: str
    authorDisplayName: str
    authorProfileImageUrl: str
    authorChannelUrl: str
    authorChannelId: CommentExtPreviewRepliesItemAuthorChannelId
    canRate: bool
    viewerRating: str
    likeCount: float
    publishedAt: str
    updatedAt: str

class CommentExtLookup(TypedDict, total=False):
    found_via: str
    pages_fetched: float
    comments_scanned: float
    sort_basis: str
    position_hint: str
    post_comment_count: float

class CommentExt(TypedDict, total=False):
    replies_token: Optional[str]
    replies_cursor: Optional[str]
    depth: Optional[float]
    published_at_epoch: Optional[float]
    feedback_id: Optional[str]
    expansion_token: Optional[str]
    author_id: Optional[str]
    ip_location: Optional[str]
    urn: Optional[str]
    reaction_counts: Optional[List[CommentExtReactionCountsItem]]
    is_edited: Optional[bool]
    previous_replies_token: Optional[str]
    author_headline: Optional[str]
    author_type: Optional[str]
    author_urn: Optional[str]
    is_contribution: Optional[bool]
    has_previous_replies: Optional[bool]
    updated_at: Optional[str]
    author_channel_id: Optional[str]
    author_url: Optional[str]
    viewer_rating: Optional[str]
    text_original: Optional[str]
    preview_replies: Optional[List[CommentExtPreviewRepliesItem]]
    lookup: Optional[CommentExtLookup]
    post_title: Optional[str]
    post_url: Optional[str]
    subreddit: Optional[str]
    subreddit_subscribers: Optional[float]
    post_score: Optional[float]
    post_comment_count: Optional[float]
    post_author: Optional[str]
    post_published_at: Optional[str]
    post_flair: Optional[str]
    is_submitter: Optional[bool]
    edited_at: Optional[str]
    removed_by: Optional[str]
    controversiality: Optional[float]
    content_language: Optional[str]
    author_followers: Optional[float]
    author_following: Optional[float]
    author_posts_count: Optional[float]
    author_location: Optional[str]
    quote_count: Optional[float]
    views: Optional[float]
    saves: Optional[float]

class Comment(TypedDict, total=False):
    id: str
    url: Optional[str]
    parent_id: Optional[str]
    post_id: Optional[str]
    text: Optional[str]
    author: CommentAuthor
    engagement: CommentEngagement
    flags: CommentFlags
    published_at: Optional[Union[str, float]]
    ext: Optional[CommentExt]
    replies: Optional[List[Any]]

class CommentListItemsItemComputed(TypedDict, total=False):
    language: Optional[str]
    labels: Optional[Dict[str, Any]]
    labels_evidence: Optional[Dict[str, Any]]

class CommentListItemsItem(TypedDict, total=False):
    comment: Comment
    computed: CommentListItemsItemComputed

class CommentList(TypedDict, total=False):
    items: List[CommentListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class AudienceAudienceLocationsItem(TypedDict, total=False):
    country: str
    countryCode: str
    count: int
    percentage: str

class AudienceAudienceAgesItem(TypedDict, total=False):
    key: str
    percentage: float

class AudienceAudienceGendersItem(TypedDict, total=False):
    key: str
    percentage: float

class AudienceAudienceStatesItem(TypedDict, total=False):
    state: str
    count: int

class Audience(TypedDict, total=False):
    audienceLocations: Optional[List[AudienceAudienceLocationsItem]]
    audienceAges: Optional[List[AudienceAudienceAgesItem]]
    audienceGenders: Optional[List[AudienceAudienceGendersItem]]
    audienceStates: Optional[List[AudienceAudienceStatesItem]]

class SearchResult(TypedDict, total=False):
    items: List[Dict[str, Any]]
    next_cursor: Optional[str]
    total: Optional[int]

class Analytics(TypedDict, total=False):
    pass

class TranscriptTranscriptsItem(TypedDict, total=False):
    text: str

class Transcript(TypedDict, total=False):
    transcript: Optional[str]
    transcript_format: Literal["webvtt", "text"]
    transcripts: Optional[List[TranscriptTranscriptsItem]]

class WebPagePageContent(TypedDict, total=False):
    markdown: Optional[str]
    html: Optional[str]
    raw_html: Optional[str]
    summary: Optional[str]

class WebPagePageMedia(TypedDict, total=False):
    screenshot_url: Optional[str]
    audio_url: Optional[str]
    video_url: Optional[str]

class WebPagePagePageState(TypedDict, total=False):
    value: Literal["content", "login_or_signup_wall", "consent_wall", "challenge", "error_or_not_found", "rate_limited", "paywall_teaser", "empty_shell", "other"]
    confidence: float
    skipped_judge: bool

class WebPagePageNative(TypedDict, total=False):
    endpoint: str
    credits_used: float
    data: Any

class WebPagePageExtractionCheckRemovedItem(TypedDict, total=False):
    field: str
    value: Any
    reason: Literal["placeholder", "not_on_page"]

class WebPagePageExtractionCheck(TypedDict, total=False):
    checked: int
    found_in_text: int
    confirmed: int
    removed: List[WebPagePageExtractionCheckRemovedItem]
    unverified: List[str]

class WebPagePageFetch(TypedDict, total=False):
    cache_state: Optional[str]
    cached_at: Optional[str]
    proxy_tier: Optional[str]

class WebPagePage(TypedDict, total=False):
    url: Optional[str]
    final_url: Optional[str]
    status_code: Optional[float]
    scrape_id: Optional[str]
    fetched_at: Optional[str]
    published_at: Optional[str]
    content: WebPagePageContent
    media: WebPagePageMedia
    title: Optional[str]
    description: Optional[str]
    source_type: Optional[str]
    extraction: Optional[Dict[str, Any]]
    answer: Any
    highlights: Any
    change_tracking: Any
    page_count: Optional[float]
    total_page_count: Optional[float]
    page_state: WebPagePagePageState
    native: WebPagePageNative
    extraction_check: WebPagePageExtractionCheck
    fetch: WebPagePageFetch

class WebPage(TypedDict, total=False):
    page: WebPagePage

class WebPageList(TypedDict, total=False):
    items: List[WebPage]
    next_cursor: Optional[str]
    total: Optional[int]

class ProductPrice(TypedDict, total=False):
    current: Optional[float]
    original: Optional[float]
    currency: Optional[str]

class ProductRating(TypedDict, total=False):
    average: Optional[float]
    count: Optional[float]

class ProductSpecificationsItem(TypedDict, total=False):
    group: Optional[str]
    name: Optional[str]
    value: Optional[str]

class ProductVariationsItem(TypedDict, total=False):
    id: Optional[str]
    title: Optional[str]
    url: Optional[str]
    category: Optional[str]

class ProductExtRatingDistribution(TypedDict, total=False):
    star_1: Optional[float]
    star_2: Optional[float]
    star_3: Optional[float]
    star_4: Optional[float]
    star_5: Optional[float]

class ProductExtStoreInventoryItem(TypedDict, total=False):
    store_id: Optional[str]
    store_name: Optional[str]
    state: Optional[str]
    in_stock: Optional[bool]
    quantity: Optional[float]
    fulfillment: Optional[str]
    service: Optional[str]
    location_type: Optional[str]
    is_selected_store: Optional[bool]

class ProductExtPromotion(TypedDict, total=False):
    label: Optional[str]
    amount_off: Optional[float]
    percent_off: Optional[float]

class ProductExtSellerReputationDetailedRatings(TypedDict, total=False):
    accurate_description: Optional[float]
    reasonable_shipping_cost: Optional[float]
    shipping_speed: Optional[float]
    communication: Optional[float]

class ProductExtSellerReputation(TypedDict, total=False):
    feedback_percentage: Optional[float]
    feedback_count: Optional[float]
    top_rated: Optional[bool]
    items_sold: Optional[float]
    joined: Optional[str]
    url: Optional[str]
    detailed_ratings: Optional[ProductExtSellerReputationDetailedRatings]

class ProductExtG2CategoriesItem(TypedDict, total=False):
    name: str
    link: str

class ProductExtG2ComparisonsItem(TypedDict, total=False):
    link: str
    name: str
    logo: str
    rating: float
    reviews: float

class ProductExtG2AlternativesItem(TypedDict, total=False):
    name: str
    link: str
    logo: str
    rating: float
    reviews: float

class ProductExtG2PricingPlansItem(TypedDict, total=False):
    plan_name: str
    plan_price: str
    price: float
    billing: Optional[str]
    plan_description: str
    plan_features: List[str]

class ProductExtG2PricingDetailsFaqsItem(TypedDict, total=False):
    question: str
    answer: str

class ProductExtG2PricingDetailsAlternativesPricingItem(TypedDict, total=False):
    product: str
    plan: str
    price: str
    billing: str
    description: Optional[str]
    features: List[str]

class ProductExtG2PricingDetails(TypedDict, total=False):
    free_trial: bool
    overview: str
    last_updated: str
    faqs: List[ProductExtG2PricingDetailsFaqsItem]
    alternatives_pricing: List[ProductExtG2PricingDetailsAlternativesPricingItem]

class ProductExtG2FeaturesItem(TypedDict, total=False):
    name: str
    features: List[str]

class ProductExtG2DetailedFeaturesItemFeaturesItem(TypedDict, total=False):
    name: str
    content: str
    percentage: Optional[str]
    based_on_number_of_reviews: float

class ProductExtG2DetailedFeaturesItem(TypedDict, total=False):
    name: str
    features: List[ProductExtG2DetailedFeaturesItemFeaturesItem]

class ProductExtG2ProsDetailsItemRelatedReviewsItem(TypedDict, total=False):
    reviewer: str
    company_size: str
    rating: float
    title: str
    question: str
    content: str

class ProductExtG2ProsDetailsItem(TypedDict, total=False):
    name: str
    highlight: str
    description: str
    mentions: float
    reviews_link: str
    related_reviews: List[ProductExtG2ProsDetailsItemRelatedReviewsItem]

class ProductExtG2ConsDetailsItemRelatedReviewsItem(TypedDict, total=False):
    reviewer: str
    company_size: str
    rating: float
    title: str
    question: str
    content: str

class ProductExtG2ConsDetailsItem(TypedDict, total=False):
    name: str
    highlight: str
    description: str
    mentions: float
    reviews_link: str
    related_reviews: List[ProductExtG2ConsDetailsItemRelatedReviewsItem]

class ProductExtG2IntegrationsItemsItem(TypedDict, total=False):
    name: str
    link: str

class ProductExtG2Integrations(TypedDict, total=False):
    count: float
    items: List[ProductExtG2IntegrationsItemsItem]

class ProductExtG2(TypedDict, total=False):
    product_uuid: str
    solution_type: str
    ai_verified: bool
    g2_reviews_link: str
    categories: List[ProductExtG2CategoriesItem]
    comparisons: List[ProductExtG2ComparisonsItem]
    alternatives: List[ProductExtG2AlternativesItem]
    pricing_plans: List[ProductExtG2PricingPlansItem]
    pricing_details: ProductExtG2PricingDetails
    features: List[ProductExtG2FeaturesItem]
    detailed_features: List[ProductExtG2DetailedFeaturesItem]
    pros: List[str]
    cons: List[str]
    pros_details: List[ProductExtG2ProsDetailsItem]
    cons_details: List[ProductExtG2ConsDetailsItem]
    integrations: ProductExtG2Integrations

class ProductExtEtsy(TypedDict, total=False):
    is_handmade: bool
    favorites: float
    is_bestseller: bool
    is_top_rated: bool
    materials: List[str]
    taxonomy_path: str
    when_made: str
    user_id: str

class ProductExtSephora(TypedDict, total=False):
    sku: str
    size: str
    ingredients: str
    loves_count: float

class ProductExtHm(TypedDict, total=False):
    color: str
    category_code: str
    sizes: List[str]
    new_arrival: bool

class ProductExtKohls(TypedDict, total=False):
    colors: List[str]
    display_color: str
    sku: str
    coupon_eligible: bool
    ship: bool

class ProductExtGumtree(TypedDict, total=False):
    user_id: str
    public_user_id: str
    account_id: str
    seller_type: str
    category_id: str
    category: str
    location: str
    location_id: str

class ProductExtAliexpress(TypedDict, total=False):
    commission_rate: str
    discount: str
    category: str
    subcategory: str
    positive_rate: str
    shop_url: str

class ProductExtTiktokshop(TypedDict, total=False):
    category: str
    category_id: str
    discount_percent: float
    stock: float
    seller_name: str
    seller_location: str
    seller_rating: float
    seller_products_count: float
    seller_followers: float
    seller_sold_count: float
    shop_identity: str
    shop_performance_percentile: float
    positive_feedback_percent: float
    response_rate_24h: float
    free_shipping: bool
    shipping_fee: float
    delivery_estimate: str
    delivery_days_min: float
    delivery_days_max: float
    shop_id: str
    shop_name: str
    shop_url: str
    shop_rating: float
    shop_region: str
    shop_followers: float
    shop_products_count: float
    shop_reviews_count: float
    shop_sold_count: float
    shop_videos_count: float
    shop_logo_url: str
    trust_label: str
    promotion_labels: List[str]

class ProductExt(TypedDict, total=False):
    gid: Optional[str]
    data_docid: Optional[str]
    pvf: Optional[str]
    seller_id: Optional[str]
    sold_count: Optional[float]
    bought_past_month: Optional[float]
    bought_past_month_label: Optional[str]
    catalog_id: Optional[str]
    requested_id: Optional[str]
    rating_distribution: Optional[ProductExtRatingDistribution]
    store_inventory: Optional[List[ProductExtStoreInventoryItem]]
    promotion: Optional[ProductExtPromotion]
    price_note: Optional[str]
    condition: Optional[str]
    available_quantity: Optional[float]
    watchers: Optional[float]
    sold_at: Optional[str]
    sold_caption: Optional[str]
    buying_format: Optional[str]
    seller_reputation: Optional[ProductExtSellerReputation]
    g2: Optional[ProductExtG2]
    etsy: Optional[ProductExtEtsy]
    sephora: Optional[ProductExtSephora]
    hm: Optional[ProductExtHm]
    kohls: Optional[ProductExtKohls]
    gumtree: Optional[ProductExtGumtree]
    sku_id: Optional[str]
    aliexpress: Optional[ProductExtAliexpress]
    tiktokshop: Optional[ProductExtTiktokshop]

class Product(TypedDict, total=False):
    id: str
    url: Optional[str]
    title: Optional[str]
    description: Optional[str]
    seller: Optional[str]
    brand: Optional[str]
    price: ProductPrice
    rating: ProductRating
    image_urls: Optional[Union[str, List[str]]]
    availability: Optional[str]
    reviews_count: Optional[float]
    features: Optional[List[str]]
    specifications: Optional[List[ProductSpecificationsItem]]
    variations: Optional[List[ProductVariationsItem]]
    ext: Optional[ProductExt]

class ProductListItemsItem(TypedDict, total=False):
    product: Product

class ProductList(TypedDict, total=False):
    items: List[ProductListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class ReviewRating(TypedDict, total=False):
    value: Optional[float]
    max: Optional[float]

class ReviewAuthor(TypedDict, total=False):
    name: Optional[str]
    avatar_url: Optional[str]
    url: Optional[str]
    location: Optional[str]
    reviews_count: Optional[float]

class ReviewResponsesItem(TypedDict, total=False):
    id: Optional[str]
    author: Optional[str]
    text: Optional[str]
    published_at: Optional[Union[str, float]]

class ReviewExtAppdataRating(TypedDict, total=False):
    rating_type: str
    value: float
    votes_count: Optional[float]
    rating_max: float

class ReviewExtAppdataUserProfile(TypedDict, total=False):
    profile_name: str
    profile_image_url: Optional[str]

class ReviewExtAppdataResponsesItem(TypedDict, total=False):
    author: str
    title: Optional[str]
    text: str
    timestamp: str

class ReviewExtAppdata(TypedDict, total=False):
    type: str
    rank_group: float
    rank_absolute: float
    position: str
    id: str
    version: Optional[str]
    rating: ReviewExtAppdataRating
    timestamp: str
    title: Optional[str]
    review_text: str
    user_profile: ReviewExtAppdataUserProfile
    entity_id: str
    helpful_count: Optional[float]
    responses: Optional[List[ReviewExtAppdataResponsesItem]]

class ReviewExtTiktokshop(TypedDict, total=False):
    reviewer_id: str
    is_incentivized_review: bool
    sku_specification: str

class ReviewExtNaver(TypedDict, total=False):
    visit_count: Optional[float]
    verified_by: Optional[str]
    treatment: Optional[str]
    view_count: Optional[float]
    keywords: Optional[List[str]]
    dedupe_key: Optional[str]

class ReviewExt(TypedDict, total=False):
    appdata: Optional[ReviewExtAppdata]
    tiktokshop: Optional[ReviewExtTiktokshop]
    naver: Optional[ReviewExtNaver]
    traveler_type: Optional[str]
    stay_check_in: Optional[str]
    stay_check_out: Optional[str]
    stay_nights: Optional[float]
    room_type: Optional[str]

class Review(TypedDict, total=False):
    id: str
    entity_id: Optional[str]
    url: Optional[str]
    title: Optional[str]
    text: Optional[str]
    rating: ReviewRating
    author: ReviewAuthor
    helpful_votes: Optional[float]
    verified: Optional[bool]
    source: Optional[str]
    language: Optional[str]
    original_language: Optional[str]
    translated: Optional[bool]
    images: Optional[List[str]]
    responses: Optional[List[ReviewResponsesItem]]
    published_at: Optional[Union[str, float]]
    ext: Optional[ReviewExt]

class ReviewListItemsItem(TypedDict, total=False):
    review: Review

class ReviewList(TypedDict, total=False):
    items: List[ReviewListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class SellerPrice(TypedDict, total=False):
    base: Optional[float]
    tax: Optional[float]
    shipping: Optional[float]
    total: Optional[float]
    currency: Optional[str]

class SellerRating(TypedDict, total=False):
    average: Optional[float]
    count: Optional[float]

class Seller(TypedDict, total=False):
    id: Optional[str]
    name: Optional[str]
    domain: Optional[str]
    url: Optional[str]
    price: SellerPrice
    rating: SellerRating
    condition: Optional[str]
    availability: Optional[str]
    annotation: Optional[str]

class SellerListItemsItem(TypedDict, total=False):
    seller: Seller

class SellerList(TypedDict, total=False):
    items: List[SellerListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class PlaceRating(TypedDict, total=False):
    value: Optional[float]
    max: Optional[float]

class PlaceHotelAmenitiesItem(TypedDict, total=False):
    category: Optional[str]
    name: Optional[str]
    available: Optional[bool]
    hint: Optional[str]

class PlaceHotelReviewTopicsItem(TypedDict, total=False):
    title: Optional[str]
    positive_score: Optional[float]
    positive_count: Optional[float]
    negative_count: Optional[float]
    total_count: Optional[float]

class PlaceHotelPricesItem(TypedDict, total=False):
    title: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    url: Optional[str]
    official_site: Optional[bool]

class PlaceHotel(TypedDict, total=False):
    stars: Optional[float]
    stars_description: Optional[str]
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    amenities: Optional[List[PlaceHotelAmenitiesItem]]
    review_topics: Optional[List[PlaceHotelReviewTopicsItem]]
    prices: Optional[List[PlaceHotelPricesItem]]

class PlaceExtHoursItem(TypedDict, total=False):
    date: Optional[str]
    day_name: Optional[str]
    is_open: Optional[bool]
    opens_at: Optional[str]
    closes_at: Optional[str]

class PlaceExtAttributes(TypedDict, total=False):
    available_attributes: Dict[str, Any]
    unavailable_attributes: Dict[str, Any]

class PlaceExtPeopleAlsoSearchItemRating(TypedDict, total=False):
    value: Optional[float]
    votes_count: Optional[float]

class PlaceExtPeopleAlsoSearchItem(TypedDict, total=False):
    cid: Optional[str]
    title: Optional[str]
    rating: Optional[PlaceExtPeopleAlsoSearchItemRating]

class PlaceExtCategoryRatingsItem(TypedDict, total=False):
    category: Optional[str]
    label: Optional[str]
    value: Optional[float]
    max: Optional[float]

class PlaceExtHostProfile(TypedDict, total=False):
    id: Optional[str]
    name: Optional[str]
    avatar_url: Optional[str]
    superhost: Optional[bool]
    verified: Optional[bool]
    years_hosting: Optional[float]
    months_hosting: Optional[float]
    response_rate: Optional[str]
    response_time: Optional[str]
    about: Optional[str]
    highlights: Optional[List[str]]

class PlaceExtRoomsItem(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]
    size_sqm: Optional[float]
    occupancy: Optional[float]
    bed_configuration: Optional[str]
    image_urls: Optional[List[str]]

class PlaceExt(TypedDict, total=False):
    distance: Optional[float]
    status: Optional[str]
    timezone: Optional[str]
    hours: Optional[List[PlaceExtHoursItem]]
    place_id: Optional[str]
    attributes: Optional[PlaceExtAttributes]
    rating_distribution: Optional[Dict[str, Any]]
    people_also_search: Optional[List[PlaceExtPeopleAlsoSearchItem]]
    menu_url: Optional[str]
    domain: Optional[str]
    maps_url: Optional[str]
    rank: Optional[float]
    city: Optional[str]
    postal_code: Optional[str]
    region: Optional[str]
    country_code: Optional[str]
    posts_count: Optional[float]
    website: Optional[str]
    facebook_places_id: Optional[str]
    business_username: Optional[str]
    is_ad: Optional[bool]
    ad_rank: Optional[float]
    ad_description: Optional[str]
    status_description: Optional[str]
    visitor_reviews_count: Optional[float]
    blog_reviews_count: Optional[float]
    booking_url: Optional[str]
    keywords: Optional[List[str]]
    category_ratings: Optional[List[PlaceExtCategoryRatingsItem]]
    room_type: Optional[str]
    capacity: Optional[float]
    subtitle: Optional[str]
    listing_badges: Optional[List[str]]
    exact_location: Optional[bool]
    listing_price_note: Optional[str]
    host_profile: Optional[PlaceExtHostProfile]
    rooms: Optional[List[PlaceExtRoomsItem]]
    languages_spoken: Optional[List[str]]

class Place(TypedDict, total=False):
    id: str
    name: Optional[str]
    url: Optional[str]
    category: Optional[str]
    rating: PlaceRating
    reviews_count: Optional[float]
    price_level: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    verified: Optional[bool]
    description: Optional[str]
    image_urls: Optional[Union[str, List[str]]]
    categories: Optional[List[str]]
    hotel: Optional[PlaceHotel]
    ext: Optional[PlaceExt]

class PlaceListItemsItem(TypedDict, total=False):
    place: Place

class PlaceList(TypedDict, total=False):
    items: List[PlaceListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class AppDeveloper(TypedDict, total=False):
    id: Optional[str]
    name: Optional[str]
    url: Optional[str]
    email: Optional[str]
    address: Optional[str]
    website: Optional[str]

class AppRating(TypedDict, total=False):
    value: Optional[float]
    max: Optional[float]
    count: Optional[float]

class AppPrice(TypedDict, total=False):
    current: Optional[float]
    original: Optional[float]
    currency: Optional[str]
    is_free: Optional[bool]
    displayed: Optional[str]

class AppInstalls(TypedDict, total=False):
    display: Optional[str]
    count: Optional[float]

class AppSimilarAppsItem(TypedDict, total=False):
    id: Optional[str]
    title: Optional[str]
    url: Optional[str]

class AppMoreByDeveloperItem(TypedDict, total=False):
    id: Optional[str]
    title: Optional[str]
    url: Optional[str]

class AppExtAppdataRating(TypedDict, total=False):
    rating_type: str
    value: float
    votes_count: Optional[float]
    rating_max: float

class AppExtAppdataPrice(TypedDict, total=False):
    current: float
    regular: Optional[float]
    max_value: Optional[float]
    currency: str
    is_price_range: bool
    displayed_price: Optional[str]

class AppExtAppdataSimilarAppsItem(TypedDict, total=False):
    app_id: str
    title: str
    url: str

class AppExtAppdataMoreAppsByDeveloperItem(TypedDict, total=False):
    app_id: str
    title: str
    url: str

class AppExtAppdata(TypedDict, total=False):
    type: str
    rank_group: float
    rank_absolute: float
    position: str
    app_id: str
    title: str
    subtitle: str
    url: str
    icon: str
    description: str
    reviews_count: Optional[float]
    rating: AppExtAppdataRating
    price: AppExtAppdataPrice
    is_free: bool
    main_category: Optional[str]
    categories: Optional[List[str]]
    languages: List[str]
    advisories: List[str]
    developer: str
    developer_id: str
    developer_url: Optional[str]
    developer_website: str
    developer_email: str
    developer_address: str
    version: Optional[str]
    minimum_os_version: Optional[str]
    size: Optional[str]
    released_date: Optional[str]
    last_update_date: str
    time_update: str
    update_notes: Optional[str]
    images: List[str]
    videos: Optional[List[str]]
    similar_apps: List[AppExtAppdataSimilarAppsItem]
    more_apps_by_developer: Optional[List[AppExtAppdataMoreAppsByDeveloperItem]]
    installs: str
    installs_count: float
    genres: List[str]
    tags: List[str]
    category_drift_probe: bool

class AppExt(TypedDict, total=False):
    appdata: Optional[AppExtAppdata]

class App(TypedDict, total=False):
    id: str
    store: Literal["google_play", "app_store"]
    url: Optional[str]
    title: Optional[str]
    subtitle: Optional[str]
    icon: Optional[str]
    description: Optional[str]
    developer: AppDeveloper
    rating: AppRating
    price: AppPrice
    reviews_count: Optional[float]
    category: Optional[str]
    categories: Optional[List[str]]
    installs: Optional[AppInstalls]
    version: Optional[str]
    minimum_os_version: Optional[str]
    size: Optional[str]
    released_at: Optional[Union[str, float]]
    updated_at: Optional[Union[str, float]]
    update_notes: Optional[str]
    image_urls: Optional[List[str]]
    video_urls: Optional[List[str]]
    languages: Optional[List[str]]
    advisories: Optional[List[str]]
    genres: Optional[List[str]]
    tags: Optional[List[str]]
    similar_apps: Optional[List[AppSimilarAppsItem]]
    more_by_developer: Optional[List[AppMoreByDeveloperItem]]
    rank: Optional[float]
    ext: Optional[AppExt]

class AppListItemsItem(TypedDict, total=False):
    app: App

class AppList(TypedDict, total=False):
    items: List[AppListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class NewsArticleListItemsItemArticle(TypedDict, total=False):
    id: str
    title: Optional[str]
    url: Optional[str]
    source: Optional[str]
    domain: Optional[str]
    snippet: Optional[str]
    image_url: Optional[str]
    published_at: Optional[Union[str, float]]
    rank: Optional[float]
    placement: Optional[str]

class NewsArticleListItemsItem(TypedDict, total=False):
    article: NewsArticleListItemsItemArticle

class NewsArticleList(TypedDict, total=False):
    items: List[NewsArticleListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class QuotePair(TypedDict, total=False):
    base_symbol: Optional[str]
    quote_symbol: Optional[str]
    base_display_name: Optional[str]
    quote_display_name: Optional[str]

class QuotePrice(TypedDict, total=False):
    current: Optional[float]
    previous_close: Optional[float]
    delta: Optional[float]
    percentage_delta: Optional[float]
    trend: Optional[str]
    day_low: Optional[float]
    day_high: Optional[float]
    year_low: Optional[float]
    year_high: Optional[float]
    timestamp: Optional[str]

QuoteMetrics = TypedDict("QuoteMetrics", {"market_cap": Optional[float], "volume": Optional[float], "avg_volume": Optional[float], "pe_ratio": Optional[float], "dividend_yield": Optional[float], "ytd_return": Optional[float], "expense_ratio": Optional[float], "net_assets": Optional[float], "yield": Optional[float], "open_interest": Optional[float], "category": Optional[str], "metrics_currency": Optional[str]}, total=False)

class QuoteAbout(TypedDict, total=False):
    description: Optional[str]
    description_source_url: Optional[str]
    ceo: Optional[str]
    founded: Optional[str]
    headquarters: Optional[str]
    website: Optional[str]
    employees: Optional[float]

class QuoteGraphItem(TypedDict, total=False):
    timestamp: str
    value: float
    volume: Optional[float]

class QuoteFinancialsQuarterlyItem(TypedDict, total=False):
    type: str
    timestamp: str
    revenue: Optional[float]
    revenue_delta: Optional[float]
    operating_expense: Optional[float]
    operating_expense_delta: Optional[float]
    net_income: Optional[float]
    net_income_delta: Optional[float]
    net_profit_margin: Optional[float]
    net_profit_margin_delta: Optional[float]
    earnings_per_share: Optional[float]
    earnings_per_share_delta: Optional[float]
    ebitda: Optional[float]
    ebitda_delta: Optional[float]
    cash_and_short_term_investments: Optional[float]
    cash_and_short_term_investments_delta: Optional[float]
    total_assets: Optional[float]
    total_assets_delta: Optional[float]
    total_liabilities: Optional[float]
    total_liabilities_delta: Optional[float]
    cash_from_operations: Optional[float]
    cash_from_operations_delta: Optional[float]
    cash_from_investing: Optional[float]
    cash_from_investing_delta: Optional[float]
    cash_from_financing: Optional[float]
    cash_from_financing_delta: Optional[float]
    net_change_in_cash: Optional[float]
    net_change_in_cash_delta: Optional[float]
    free_cash_flow: Optional[float]
    free_cash_flow_delta: Optional[float]
    effective_tax_rate: Optional[float]
    total_equity: Optional[float]
    shares_outstanding: Optional[float]
    price_to_book: Optional[float]
    return_on_assets: Optional[float]
    return_on_capital: Optional[float]

class QuoteFinancialsAnnualItem(TypedDict, total=False):
    type: str
    timestamp: str
    revenue: Optional[float]
    revenue_delta: Optional[float]
    operating_expense: Optional[float]
    operating_expense_delta: Optional[float]
    net_income: Optional[float]
    net_income_delta: Optional[float]
    net_profit_margin: Optional[float]
    net_profit_margin_delta: Optional[float]
    earnings_per_share: Optional[float]
    earnings_per_share_delta: Optional[float]
    ebitda: Optional[float]
    ebitda_delta: Optional[float]
    cash_and_short_term_investments: Optional[float]
    cash_and_short_term_investments_delta: Optional[float]
    total_assets: Optional[float]
    total_assets_delta: Optional[float]
    total_liabilities: Optional[float]
    total_liabilities_delta: Optional[float]
    cash_from_operations: Optional[float]
    cash_from_operations_delta: Optional[float]
    cash_from_investing: Optional[float]
    cash_from_investing_delta: Optional[float]
    cash_from_financing: Optional[float]
    cash_from_financing_delta: Optional[float]
    net_change_in_cash: Optional[float]
    net_change_in_cash_delta: Optional[float]
    free_cash_flow: Optional[float]
    free_cash_flow_delta: Optional[float]
    effective_tax_rate: Optional[float]
    total_equity: Optional[float]
    shares_outstanding: Optional[float]
    price_to_book: Optional[float]
    return_on_assets: Optional[float]
    return_on_capital: Optional[float]

class QuoteFinancials(TypedDict, total=False):
    quarterly: Optional[List[QuoteFinancialsQuarterlyItem]]
    annual: Optional[List[QuoteFinancialsAnnualItem]]

class QuotePeersItemPair(TypedDict, total=False):
    base_symbol: Optional[str]
    quote_symbol: Optional[str]
    base_display_name: Optional[str]
    quote_display_name: Optional[str]

class QuotePeersItemPrice(TypedDict, total=False):
    current: Optional[float]
    previous_close: Optional[float]
    delta: Optional[float]
    percentage_delta: Optional[float]
    trend: Optional[str]
    day_low: Optional[float]
    day_high: Optional[float]
    year_low: Optional[float]
    year_high: Optional[float]
    timestamp: Optional[str]

QuotePeersItemMetrics = TypedDict("QuotePeersItemMetrics", {"market_cap": Optional[float], "volume": Optional[float], "avg_volume": Optional[float], "pe_ratio": Optional[float], "dividend_yield": Optional[float], "ytd_return": Optional[float], "expense_ratio": Optional[float], "net_assets": Optional[float], "yield": Optional[float], "open_interest": Optional[float], "category": Optional[str], "metrics_currency": Optional[str]}, total=False)

class QuotePeersItem(TypedDict, total=False):
    id: str
    ticker: Optional[str]
    exchange: Optional[str]
    name: Optional[str]
    type: Literal["stock", "etf", "index", "crypto", "forex", "futures", "fund", "unknown"]
    url: Optional[str]
    currency: Optional[str]
    pair: Optional[QuotePeersItemPair]
    price: QuotePeersItemPrice
    metrics: Optional[QuotePeersItemMetrics]

class QuoteExt(TypedDict, total=False):
    section: str

class Quote(TypedDict, total=False):
    id: str
    ticker: Optional[str]
    exchange: Optional[str]
    name: Optional[str]
    type: Literal["stock", "etf", "index", "crypto", "forex", "futures", "fund", "unknown"]
    url: Optional[str]
    currency: Optional[str]
    pair: Optional[QuotePair]
    price: QuotePrice
    metrics: Optional[QuoteMetrics]
    about: Optional[QuoteAbout]
    graph: Optional[List[QuoteGraphItem]]
    financials: Optional[QuoteFinancials]
    peers: Optional[List[QuotePeersItem]]
    ext: Optional[QuoteExt]

class QuoteListItemsItem(TypedDict, total=False):
    quote: Quote

class QuoteList(TypedDict, total=False):
    items: List[QuoteListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class BarListItemsItemBar(TypedDict, total=False):
    id: str
    symbol: Optional[str]
    date: Optional[Union[str, float]]
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    adj_close: Optional[float]
    volume: Optional[float]
    dividend: Optional[float]
    split_ratio: Optional[str]
    currency: Optional[str]
    interval: Optional[str]

class BarListItemsItem(TypedDict, total=False):
    bar: BarListItemsItemBar

class BarList(TypedDict, total=False):
    items: List[BarListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class FinancialStatementListItemsItemFinancialStatement(TypedDict, total=False):
    id: str
    symbol: Optional[str]
    statement: Optional[str]
    period_type: Optional[str]
    period_end: Optional[Union[str, float]]
    currency: Optional[str]
    revenue: Optional[float]
    revenue_delta: Optional[float]
    operating_expense: Optional[float]
    operating_expense_delta: Optional[float]
    net_income: Optional[float]
    net_income_delta: Optional[float]
    net_profit_margin: Optional[float]
    net_profit_margin_delta: Optional[float]
    earnings_per_share: Optional[float]
    earnings_per_share_delta: Optional[float]
    ebitda: Optional[float]
    ebitda_delta: Optional[float]
    effective_tax_rate: Optional[float]
    cash_and_short_term_investments: Optional[float]
    cash_and_short_term_investments_delta: Optional[float]
    total_assets: Optional[float]
    total_assets_delta: Optional[float]
    total_liabilities: Optional[float]
    total_liabilities_delta: Optional[float]
    total_equity: Optional[float]
    shares_outstanding: Optional[float]
    price_to_book: Optional[float]
    return_on_assets: Optional[float]
    return_on_capital: Optional[float]
    cash_from_operations: Optional[float]
    cash_from_operations_delta: Optional[float]
    cash_from_investing: Optional[float]
    cash_from_investing_delta: Optional[float]
    cash_from_financing: Optional[float]
    cash_from_financing_delta: Optional[float]
    net_change_in_cash: Optional[float]
    net_change_in_cash_delta: Optional[float]
    free_cash_flow: Optional[float]
    free_cash_flow_delta: Optional[float]

class FinancialStatementListItemsItem(TypedDict, total=False):
    financial_statement: FinancialStatementListItemsItemFinancialStatement

class FinancialStatementList(TypedDict, total=False):
    items: List[FinancialStatementListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class OptionContractListItemsItemOptionContract(TypedDict, total=False):
    id: str
    symbol: Optional[str]
    contract_symbol: Optional[str]
    type: Optional[str]
    strike: Optional[float]
    expiry: Optional[Union[str, float]]
    last_price: Optional[float]
    bid: Optional[float]
    ask: Optional[float]
    change: Optional[float]
    percent_change: Optional[float]
    volume: Optional[float]
    open_interest: Optional[float]
    implied_volatility: Optional[float]
    in_the_money: Optional[bool]
    contract_size: Optional[str]
    currency: Optional[str]
    last_trade_date: Optional[Union[str, float]]

class OptionContractListItemsItem(TypedDict, total=False):
    option_contract: OptionContractListItemsItemOptionContract

class OptionContractList(TypedDict, total=False):
    items: List[OptionContractListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class JobCompany(TypedDict, total=False):
    id: Optional[str]
    name: Optional[str]
    url: Optional[str]
    verified: Optional[bool]

class JobExt(TypedDict, total=False):
    is_promote: Optional[bool]
    applicant_count: Optional[float]
    skills: Optional[List[str]]
    job_provider: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    salary_currency: Optional[str]
    country_code: Optional[str]
    linkedin_company_name: Optional[str]
    industries: Optional[str]
    job_function: Optional[str]
    accepting_applications: Optional[bool]
    board: Optional[str]

class Job(TypedDict, total=False):
    id: str
    title: Optional[str]
    url: Optional[str]
    company: JobCompany
    location: Optional[str]
    listed_at: Optional[Union[str, float]]
    easy_apply: Optional[bool]
    remote: Optional[str]
    employment_type: Optional[str]
    experience_level: Optional[str]
    description: Optional[str]
    apply_url: Optional[str]
    ext: Optional[JobExt]

class JobListItemsItem(TypedDict, total=False):
    job: Job

class JobList(TypedDict, total=False):
    items: List[JobListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class MediaListItemsItem(TypedDict, total=False):
    url: str

class MediaList(TypedDict, total=False):
    items: List[MediaListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class AnalyticsResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: Analytics
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class AppListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: AppList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class AuthorResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: Author
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class AuthorListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: AuthorList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class CommentListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: CommentList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class JobListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: JobList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class NewsArticleListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: NewsArticleList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class PlaceListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: PlaceList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class PostListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: PostList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class ProductListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: ProductList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class QuoteResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: Quote
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class QuoteListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: QuoteList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class ReviewListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: ReviewList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class TranscriptResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: Transcript
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

class WebPageListResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: WebPageList
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str
    cached: bool
    pagination: Pagination
    idempotent_replay: bool

# Response types for the endpoints the recipes use.
PrismBrandMentionsResponse = AnalyticsResponse
SearchMultiResponse = AnalyticsResponse
PrismMentionsResponse = AnalyticsResponse
PrismShareOfVoiceResponse = AnalyticsResponse
TwitterSearchTweetsResponse = PostListResponse
RedditSearchResponse = PostListResponse
SearchForumsResponse = AnalyticsResponse
GoogleNewsSearchResponse = NewsArticleListResponse
PrismDiscoverResponse = AnalyticsResponse
PrismCreatorsResponse = AnalyticsResponse
InstagramSearchReelsResponse = PostListResponse
InstagramProfileAboutResponse = AuthorResponse
PrismCreatorVetResponse = AnalyticsResponse
YoutubeChannelAboutResponse = AuthorResponse
PrismCreatorCardResponse = AnalyticsResponse
TiktokProfileResponse = AuthorResponse
TiktokProfileVideosResponse = PostListResponse
TiktokPostCommentsResponse = CommentListResponse
PrismFindAccountsResponse = AnalyticsResponse
LinkedinProfileResponse = AuthorResponse
LinkedinProfilePostsResponse = PostListResponse
LinkedinSearchPeopleResponse = AuthorListResponse
LinkedinProfileCompleteResponse = AnalyticsResponse
PrismProfilesPostResponse = AnalyticsResponse
PrismCommentsResponse = AnalyticsResponse
YoutubeVideoTranscriptResponse = TranscriptResponse
AmazonProductSearchResponse = ProductListResponse
AmazonReviewsResponse = ReviewListResponse
WalmartSearchResponse = ProductListResponse
WalmartReviewsResponse = ReviewListResponse
HomeDepotSearchResponse = ProductListResponse
HomeDepotReviewsResponse = ReviewListResponse
PrismProductReviewsResponse = AnalyticsResponse
AppStoreAppSearchResponse = AppListResponse
AppStoreAppReviewsResponse = ReviewListResponse
YelpSearchResponse = PlaceListResponse
YelpBusinessReviewsResponse = ReviewListResponse
FacebookAdlibraryCompanyAdsResponse = PostListResponse
InstagramProfilePostsResponse = PostListResponse
YoutubeChannelVideosResponse = PostListResponse
WebMonitorsPostResponse = AnalyticsResponse
WebMonitorsMonitorIdChecksResponse = WebPageListResponse
PrismPostStatsPostResponse = AnalyticsResponse
JobsSalaryResponse = AnalyticsResponse
JobsLinkedinSearchResponse = JobListResponse
FinanceTickerSearchResponse = QuoteListResponse
FinanceQuoteResponse = QuoteResponse
FinanceNewsResponse = NewsArticleListResponse
WebCrawlPostResponse = AnalyticsResponse
WebJobsJobIdResponse = AnalyticsResponse
