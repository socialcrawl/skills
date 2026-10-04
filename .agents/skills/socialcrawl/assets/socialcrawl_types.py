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


class ApiErrorDetail(TypedDict, total=False):
    type: str
    message: str
    status: int
    doc_url: str
    retryable: bool
    details: Dict[str, Any]


class ApiErrorBody(TypedDict, total=False):
    success: bool
    error: ApiErrorDetail
    credits_used: int
    credits_remaining: Optional[int]
    request_id: str


class AuthorExtEmployeeCountRange(TypedDict, total=False):
    start: Optional[int]
    end: Optional[int]

class AuthorExtSearchHit(TypedDict, total=False):
    match: Optional[str]
    title: Optional[str]
    snippet: Optional[str]
    evidence_url: Optional[str]

class AuthorExt(TypedDict, total=False):
    social_context: Optional[str]
    account_created: Optional[str]
    country: Optional[str]
    collects_received: Optional[int]
    former_usernames: Optional[List[str]]
    public_email: Optional[str]
    contact_email: Optional[str]
    public_phone: Optional[str]
    similar_source: Optional[str]
    instagram_username: Optional[str]
    business_category: Optional[str]
    hd_avatar_url: Optional[str]
    website: Optional[str]
    cover_url: Optional[str]
    page_active: Optional[bool]
    employee_count: Optional[int]
    employee_count_range: Optional[AuthorExtEmployeeCountRange]
    founded_year: Optional[int]
    specialities: Optional[List[str]]
    industries: Optional[List[str]]
    headquarters: Optional[str]
    locations: Optional[List[str]]
    hashtags: Optional[List[str]]
    funding: Optional[str]
    address: Optional[str]
    price_range: Optional[str]
    rating: Optional[str]
    rating_count: Optional[int]
    talking_about_count: Optional[int]
    business_hours: Optional[List[str]]
    links: Optional[List[str]]
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
    company_id: Optional[str]
    reaction_type: Optional[str]
    followers_approximate: Optional[bool]
    keywords: Optional[str]
    total_views: Optional[int]
    joined_at_timestamp: Optional[str]
    topicCategories: Optional[List[str]]
    bannerExternalUrl: Optional[str]
    madeForKids: Optional[bool]
    hiddenSubscriberCount: Optional[bool]
    related_playlists: Optional[str]
    topic_ids: Optional[List[str]]
    unsubscribed_trailer: Optional[str]
    localizations: Optional[str]
    monthly_listeners: Optional[int]
    total_ratings: Optional[int]
    average_rating: Optional[int]
    creator_username: Optional[str]
    join_policy: Optional[str]
    is_nsfw: Optional[bool]
    rules: Optional[List[str]]
    weekly_active_users: Optional[int]
    weekly_contributions: Optional[int]
    rules_text: Optional[str]
    language: Optional[str]
    post_karma: Optional[int]
    comment_karma: Optional[int]
    awardee_karma: Optional[int]
    trophy_count: Optional[int]
    banner_url: Optional[str]
    profile_title: Optional[str]
    social_links: Optional[List[str]]
    bio_link: Optional[str]
    group: Optional[str]
    search_hit: Optional[AuthorExtSearchHit]

class Author(TypedDict, total=False):
    id: str
    username: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    verified: Optional[bool]
    followers: Optional[int]
    following: Optional[int]
    posts_count: Optional[int]
    likes_count: Optional[int]
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
    duration_seconds: Optional[int]

class PostAuthor(TypedDict, total=False):
    username: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    verified: Optional[bool]

class PostEngagement(TypedDict, total=False):
    views: Optional[int]
    likes: Optional[int]
    comments: Optional[int]
    shares: Optional[int]
    saves: Optional[int]

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

class PostExt(TypedDict, total=False):
    music_id: Optional[str]
    author_id: Optional[str]
    author_followers: Optional[int]
    author_following: Optional[int]
    author_posts_count: Optional[int]
    author_country: Optional[str]
    author_public_email: Optional[str]
    author_public_phone: Optional[str]
    download_count: Optional[int]
    region: Optional[str]
    subreddit: Optional[str]
    title: Optional[str]
    selftext: Optional[str]
    upvote_ratio: Optional[int]
    flair: Optional[str]
    content_language: Optional[str]
    type: Optional[str]
    content_type: Optional[str]
    ticker_symbols: Optional[List[str]]
    video_view_count: Optional[int]
    ig_play_count: Optional[int]
    repost_count: Optional[int]
    media_type: Optional[str]
    text_truncated: Optional[bool]
    ip_location: Optional[str]
    carousel_count: Optional[int]
    remix_count: Optional[int]
    audio_cluster_id: Optional[str]
    facebook_likes: Optional[int]
    facebook_comments: Optional[int]
    published_at_epoch: Optional[int]
    usertags: Optional[List[str]]
    coauthors: Optional[List[str]]
    music: Optional[str]
    sponsor_tags: Optional[List[str]]
    location: Optional[str]
    quoted_post: Optional[str]
    retweeted_post: Optional[str]
    quote_count: Optional[int]
    all_media_urls: Optional[List[str]]
    reaction_counts: Optional[List[str]]
    share_urn: Optional[str]
    post_type: Optional[str]
    activity_id: Optional[str]
    published_at_precision: Optional[str]
    author_urn: Optional[str]
    author_headline: Optional[str]
    author_type: Optional[str]
    is_repost_quote: Optional[bool]
    article: Optional[str]
    reaction_type: Optional[str]
    download_media_urls: Optional[List[str]]
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
    position: Optional[int]
    playlistId: Optional[str]
    videoOwnerChannelId: Optional[str]
    videoPublishedAt: Optional[str]
    description: Optional[str]
    default_language: Optional[str]
    localizations: Optional[str]
    playlist_item_id: Optional[str]
    playlist_owner_channel_id: Optional[str]
    playlist_owner_title: Optional[str]
    channel_id: Optional[str]
    published_label: Optional[str]
    published_precision: Optional[str]
    video_count: Optional[int]
    commerce: Optional[str]
    on_screen_texts: Optional[List[str]]
    topic_tag: Optional[str]
    reshare_count: Optional[int]
    dsp_ids: Optional[str]
    topic_tag_id: Optional[str]
    amazon_shop_lists: Optional[List[str]]
    amazon_shop_trending_picks: Optional[List[str]]
    amazon_shop_curations: Optional[List[str]]
    amazon_shop_socials: Optional[List[str]]
    ad: Optional[str]
    apple_music: Optional[str]
    feedback_id: Optional[str]
    event: Optional[str]
    trend: Optional[str]
    updated_at: Optional[str]

class Post(TypedDict, total=False):
    id: str
    url: Optional[str]
    content: PostContent
    author: PostAuthor
    engagement: PostEngagement
    flags: PostFlags
    published_at: Optional[Union[str, int]]
    ext: Optional[PostExt]

class PostListItemsItemComputedRelevance(TypedDict, total=False):
    p: int
    sense: str
    depth: int
    spam: int

class PostListItemsItemComputed(TypedDict, total=False):
    engagement_rate: Optional[int]
    language: Optional[str]
    content_category: Optional[str]
    estimated_reach: Optional[int]
    relevance: Optional[PostListItemsItemComputedRelevance]
    labels: Optional[str]
    labels_evidence: Optional[str]

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
    likes: Optional[int]
    replies: Optional[int]

class CommentFlags(TypedDict, total=False):
    pinned: Optional[bool]
    deleted: bool

class CommentExt(TypedDict, total=False):
    replies_token: Optional[str]
    replies_cursor: Optional[str]
    depth: Optional[int]
    published_at_epoch: Optional[int]
    feedback_id: Optional[str]
    expansion_token: Optional[str]
    author_id: Optional[str]
    ip_location: Optional[str]
    urn: Optional[str]
    reaction_counts: Optional[List[str]]
    is_edited: Optional[bool]
    previous_replies_token: Optional[str]
    author_headline: Optional[str]
    updated_at: Optional[str]
    author_channel_id: Optional[str]
    author_url: Optional[str]
    viewer_rating: Optional[str]
    text_original: Optional[str]
    preview_replies: Optional[List[str]]
    lookup: Optional[str]
    post_title: Optional[str]
    post_url: Optional[str]
    subreddit: Optional[str]
    subreddit_subscribers: Optional[int]
    post_score: Optional[int]
    post_comment_count: Optional[int]
    post_author: Optional[str]
    post_published_at: Optional[str]
    post_flair: Optional[str]
    is_submitter: Optional[bool]
    edited_at: Optional[str]
    controversiality: Optional[int]
    content_language: Optional[str]
    author_followers: Optional[int]
    author_following: Optional[int]
    author_posts_count: Optional[int]
    quote_count: Optional[int]
    views: Optional[int]
    saves: Optional[int]

class Comment(TypedDict, total=False):
    id: str
    url: Optional[str]
    parent_id: Optional[str]
    post_id: Optional[str]
    text: Optional[str]
    author: CommentAuthor
    engagement: CommentEngagement
    flags: CommentFlags
    published_at: Optional[Union[str, int]]
    ext: Optional[CommentExt]
    replies: Optional[List[Dict[str, Any]]]

class CommentListItemsItem(TypedDict, total=False):
    comment: Comment

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

class AnalyticsMetrics(TypedDict, total=False):
    total_views: int
    total_likes: int
    total_comments: int
    engagement_rate: float

class Analytics(TypedDict, total=False):
    metrics: AnalyticsMetrics
    period: Optional[str]
    breakdown: Optional[List[Dict[str, Any]]]

class TranscriptTranscriptsItem(TypedDict, total=False):
    text: str

class Transcript(TypedDict, total=False):
    transcript: Optional[str]
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
    content: WebPagePageContent
    media: WebPagePageMedia
    extraction: Optional[Dict[str, Any]]
    fetch: WebPagePageFetch

class WebPage(TypedDict, total=False):
    page: WebPagePage

class WebPageList(TypedDict, total=False):
    items: List[WebPage]
    next_cursor: Optional[str]
    total: Optional[int]

class ProductPrice(TypedDict, total=False):
    current: Optional[int]
    original: Optional[int]
    currency: Optional[str]

class ProductRating(TypedDict, total=False):
    average: Optional[int]
    count: Optional[int]

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
    star_1: Optional[int]
    star_2: Optional[int]
    star_3: Optional[int]
    star_4: Optional[int]
    star_5: Optional[int]

class ProductExtStoreInventoryItem(TypedDict, total=False):
    store_id: Optional[str]
    store_name: Optional[str]
    state: Optional[str]
    in_stock: Optional[bool]
    quantity: Optional[int]
    fulfillment: Optional[str]
    service: Optional[str]
    location_type: Optional[str]
    is_selected_store: Optional[bool]

class ProductExtPromotion(TypedDict, total=False):
    label: Optional[str]
    amount_off: Optional[int]
    percent_off: Optional[int]

class ProductExtSellerReputationDetailedRatings(TypedDict, total=False):
    accurate_description: Optional[int]
    reasonable_shipping_cost: Optional[int]
    shipping_speed: Optional[int]
    communication: Optional[int]

class ProductExtSellerReputation(TypedDict, total=False):
    feedback_percentage: Optional[int]
    feedback_count: Optional[int]
    top_rated: Optional[bool]
    items_sold: Optional[int]
    joined: Optional[str]
    url: Optional[str]
    detailed_ratings: Optional[ProductExtSellerReputationDetailedRatings]

class ProductExt(TypedDict, total=False):
    gid: Optional[str]
    data_docid: Optional[str]
    pvf: Optional[str]
    seller_id: Optional[str]
    sold_count: Optional[int]
    bought_past_month: Optional[int]
    bought_past_month_label: Optional[str]
    catalog_id: Optional[str]
    requested_id: Optional[str]
    rating_distribution: Optional[ProductExtRatingDistribution]
    store_inventory: Optional[List[ProductExtStoreInventoryItem]]
    promotion: Optional[ProductExtPromotion]
    price_note: Optional[str]
    condition: Optional[str]
    available_quantity: Optional[int]
    watchers: Optional[int]
    sold_at: Optional[str]
    sold_caption: Optional[str]
    buying_format: Optional[str]
    seller_reputation: Optional[ProductExtSellerReputation]
    g2: Optional[str]
    etsy: Optional[str]
    sephora: Optional[str]
    hm: Optional[str]
    kohls: Optional[str]
    gumtree: Optional[str]
    sku_id: Optional[str]
    aliexpress: Optional[str]
    tiktokshop: Optional[str]

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
    reviews_count: Optional[int]
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
    value: Optional[int]
    max: Optional[int]

class ReviewAuthor(TypedDict, total=False):
    name: Optional[str]
    avatar_url: Optional[str]
    url: Optional[str]
    location: Optional[str]
    reviews_count: Optional[int]

class ReviewResponsesItem(TypedDict, total=False):
    id: Optional[str]
    author: Optional[str]
    text: Optional[str]
    published_at: Optional[Union[str, int]]

class ReviewExt(TypedDict, total=False):
    appdata: Optional[str]
    tiktokshop: Optional[str]

class Review(TypedDict, total=False):
    id: str
    entity_id: Optional[str]
    url: Optional[str]
    title: Optional[str]
    text: Optional[str]
    rating: ReviewRating
    author: ReviewAuthor
    helpful_votes: Optional[int]
    verified: Optional[bool]
    source: Optional[str]
    language: Optional[str]
    original_language: Optional[str]
    translated: Optional[bool]
    images: Optional[List[str]]
    responses: Optional[List[ReviewResponsesItem]]
    published_at: Optional[Union[str, int]]
    ext: Optional[ReviewExt]

class ReviewListItemsItem(TypedDict, total=False):
    review: Review

class ReviewList(TypedDict, total=False):
    items: List[ReviewListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class SellerPrice(TypedDict, total=False):
    base: Optional[int]
    tax: Optional[int]
    shipping: Optional[int]
    total: Optional[int]
    currency: Optional[str]

class SellerRating(TypedDict, total=False):
    average: Optional[int]
    count: Optional[int]

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
    value: Optional[int]
    max: Optional[int]

class PlaceHotelAmenitiesItem(TypedDict, total=False):
    category: Optional[str]
    name: Optional[str]
    available: Optional[bool]
    hint: Optional[str]

class PlaceHotelReviewTopicsItem(TypedDict, total=False):
    title: Optional[str]
    positive_score: Optional[int]
    positive_count: Optional[int]
    negative_count: Optional[int]
    total_count: Optional[int]

class PlaceHotelPricesItem(TypedDict, total=False):
    title: Optional[str]
    price: Optional[int]
    currency: Optional[str]
    url: Optional[str]
    official_site: Optional[bool]

class PlaceHotel(TypedDict, total=False):
    stars: Optional[int]
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

class PlaceExtPeopleAlsoSearchItemRating(TypedDict, total=False):
    value: Optional[int]
    votes_count: Optional[int]

class PlaceExtPeopleAlsoSearchItem(TypedDict, total=False):
    cid: Optional[str]
    title: Optional[str]
    rating: Optional[PlaceExtPeopleAlsoSearchItemRating]

class PlaceExt(TypedDict, total=False):
    distance: Optional[int]
    status: Optional[str]
    timezone: Optional[str]
    hours: Optional[List[PlaceExtHoursItem]]
    place_id: Optional[str]
    attributes: Optional[str]
    rating_distribution: Optional[str]
    people_also_search: Optional[List[PlaceExtPeopleAlsoSearchItem]]
    menu_url: Optional[str]

class Place(TypedDict, total=False):
    id: str
    name: Optional[str]
    url: Optional[str]
    category: Optional[str]
    rating: PlaceRating
    reviews_count: Optional[int]
    price_level: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    latitude: Optional[int]
    longitude: Optional[int]
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
    value: Optional[int]
    max: Optional[int]
    count: Optional[int]

class AppPrice(TypedDict, total=False):
    current: Optional[int]
    original: Optional[int]
    currency: Optional[str]
    is_free: Optional[bool]
    displayed: Optional[str]

class AppInstalls(TypedDict, total=False):
    display: Optional[str]
    count: Optional[int]

class AppSimilarAppsItem(TypedDict, total=False):
    id: Optional[str]
    title: Optional[str]
    url: Optional[str]

class AppMoreByDeveloperItem(TypedDict, total=False):
    id: Optional[str]
    title: Optional[str]
    url: Optional[str]

class AppExt(TypedDict, total=False):
    appdata: Optional[str]

class App(TypedDict, total=False):
    id: str
    store: str
    url: Optional[str]
    title: Optional[str]
    subtitle: Optional[str]
    icon: Optional[str]
    description: Optional[str]
    developer: AppDeveloper
    rating: AppRating
    price: AppPrice
    reviews_count: Optional[int]
    category: Optional[str]
    categories: Optional[List[str]]
    installs: Optional[AppInstalls]
    version: Optional[str]
    minimum_os_version: Optional[str]
    size: Optional[str]
    released_at: Optional[Union[str, int]]
    updated_at: Optional[Union[str, int]]
    update_notes: Optional[str]
    image_urls: Optional[List[str]]
    video_urls: Optional[List[str]]
    languages: Optional[List[str]]
    advisories: Optional[List[str]]
    genres: Optional[List[str]]
    tags: Optional[List[str]]
    similar_apps: Optional[List[AppSimilarAppsItem]]
    more_by_developer: Optional[List[AppMoreByDeveloperItem]]
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
    published_at: Optional[Union[str, int]]
    rank: Optional[int]
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
    current: Optional[int]
    previous_close: Optional[int]
    delta: Optional[int]
    percentage_delta: Optional[int]
    trend: Optional[str]
    day_low: Optional[int]
    day_high: Optional[int]
    year_low: Optional[int]
    year_high: Optional[int]
    timestamp: Optional[str]

QuoteMetrics = TypedDict("QuoteMetrics", {"market_cap": Optional[int], "volume": Optional[int], "avg_volume": Optional[int], "pe_ratio": Optional[int], "dividend_yield": Optional[int], "ytd_return": Optional[int], "expense_ratio": Optional[int], "net_assets": Optional[int], "yield": Optional[int], "open_interest": Optional[int], "category": Optional[str], "metrics_currency": Optional[str]}, total=False)

class QuoteAbout(TypedDict, total=False):
    description: Optional[str]
    description_source_url: Optional[str]
    ceo: Optional[str]
    founded: Optional[str]
    headquarters: Optional[str]
    website: Optional[str]
    employees: Optional[int]

class QuoteGraphItem(TypedDict, total=False):
    timestamp: str
    value: int
    volume: Optional[int]

class QuoteFinancials(TypedDict, total=False):
    quarterly: Optional[List[str]]
    annual: Optional[List[str]]

class QuotePeersItemPair(TypedDict, total=False):
    base_symbol: Optional[str]
    quote_symbol: Optional[str]
    base_display_name: Optional[str]
    quote_display_name: Optional[str]

class QuotePeersItemPrice(TypedDict, total=False):
    current: Optional[int]
    previous_close: Optional[int]
    delta: Optional[int]
    percentage_delta: Optional[int]
    trend: Optional[str]
    day_low: Optional[int]
    day_high: Optional[int]
    year_low: Optional[int]
    year_high: Optional[int]
    timestamp: Optional[str]

QuotePeersItemMetrics = TypedDict("QuotePeersItemMetrics", {"market_cap": Optional[int], "volume": Optional[int], "avg_volume": Optional[int], "pe_ratio": Optional[int], "dividend_yield": Optional[int], "ytd_return": Optional[int], "expense_ratio": Optional[int], "net_assets": Optional[int], "yield": Optional[int], "open_interest": Optional[int], "category": Optional[str], "metrics_currency": Optional[str]}, total=False)

class QuotePeersItem(TypedDict, total=False):
    id: str
    ticker: Optional[str]
    exchange: Optional[str]
    name: Optional[str]
    type: str
    url: Optional[str]
    currency: Optional[str]
    pair: Optional[QuotePeersItemPair]
    price: QuotePeersItemPrice
    metrics: Optional[QuotePeersItemMetrics]

class Quote(TypedDict, total=False):
    id: str
    ticker: Optional[str]
    exchange: Optional[str]
    name: Optional[str]
    type: str
    url: Optional[str]
    currency: Optional[str]
    pair: Optional[QuotePair]
    price: QuotePrice
    metrics: Optional[QuoteMetrics]
    about: Optional[QuoteAbout]
    graph: Optional[List[QuoteGraphItem]]
    financials: Optional[QuoteFinancials]
    peers: Optional[List[QuotePeersItem]]
    ext: Optional[str]

class QuoteListItemsItem(TypedDict, total=False):
    quote: Quote

class QuoteList(TypedDict, total=False):
    items: List[QuoteListItemsItem]
    next_cursor: Optional[str]
    total: Optional[int]

class BarListItemsItemBar(TypedDict, total=False):
    id: str
    symbol: Optional[str]
    date: Optional[Union[str, int]]
    open: Optional[int]
    high: Optional[int]
    low: Optional[int]
    close: Optional[int]
    adj_close: Optional[int]
    volume: Optional[int]
    dividend: Optional[int]
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
    period_end: Optional[Union[str, int]]
    currency: Optional[str]
    revenue: Optional[int]
    revenue_delta: Optional[int]
    operating_expense: Optional[int]
    operating_expense_delta: Optional[int]
    net_income: Optional[int]
    net_income_delta: Optional[int]
    net_profit_margin: Optional[int]
    net_profit_margin_delta: Optional[int]
    earnings_per_share: Optional[int]
    earnings_per_share_delta: Optional[int]
    ebitda: Optional[int]
    ebitda_delta: Optional[int]
    effective_tax_rate: Optional[int]
    cash_and_short_term_investments: Optional[int]
    cash_and_short_term_investments_delta: Optional[int]
    total_assets: Optional[int]
    total_assets_delta: Optional[int]
    total_liabilities: Optional[int]
    total_liabilities_delta: Optional[int]
    total_equity: Optional[int]
    shares_outstanding: Optional[int]
    price_to_book: Optional[int]
    return_on_assets: Optional[int]
    return_on_capital: Optional[int]
    cash_from_operations: Optional[int]
    cash_from_operations_delta: Optional[int]
    cash_from_investing: Optional[int]
    cash_from_investing_delta: Optional[int]
    cash_from_financing: Optional[int]
    cash_from_financing_delta: Optional[int]
    net_change_in_cash: Optional[int]
    net_change_in_cash_delta: Optional[int]
    free_cash_flow: Optional[int]
    free_cash_flow_delta: Optional[int]

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
    strike: Optional[int]
    expiry: Optional[Union[str, int]]
    last_price: Optional[int]
    bid: Optional[int]
    ask: Optional[int]
    change: Optional[int]
    percent_change: Optional[int]
    volume: Optional[int]
    open_interest: Optional[int]
    implied_volatility: Optional[int]
    in_the_money: Optional[bool]
    contract_size: Optional[str]
    currency: Optional[str]
    last_trade_date: Optional[Union[str, int]]

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
    applicant_count: Optional[int]
    skills: Optional[List[str]]
    job_provider: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
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
    listed_at: Optional[Union[str, int]]
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

class WebPageResponse(TypedDict, total=False):
    success: bool
    platform: str
    endpoint: str
    data: WebPage
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
SearchCreatorsResponse = AnalyticsResponse
InstagramSearchReelsResponse = PostListResponse
InstagramProfileAboutResponse = AuthorResponse
PrismCreatorVetResponse = AnalyticsResponse
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
WebExtractResponse = WebPageResponse
NaverBriefResponse = AnalyticsResponse
