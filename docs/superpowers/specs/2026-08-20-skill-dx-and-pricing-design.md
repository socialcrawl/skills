# SocialCrawl Skill DX and Pricing Design

## Goal

Make the public SocialCrawl skill safe to reuse and difficult for an agent to misuse: licence the repository under MIT, quote the cost of the request that is actually about to run, protect API keys, give errors actionable retry policy, and keep every published skill copy and download artifact current.

## Findings

The enquiry is correct about the core pricing failure. Several endpoint headings show a registry base or unit cost even though the request handler bills by URL, row, probe, page, chunk, runtime, or recurring run. `prism/post-stats` is the clearest example: a successful row costs 1 credit on most platforms and 5 credits for Instagram or LinkedIn, so a 100-row request can reserve and charge up to 500 credits. `prism/ai-visibility` already exposes a generated range, but it does not make the 32-credit one-prompt default obvious.

The repository also has no licence, its manual Git installation examples clone the repository at the wrong skill depth, the three tracked skill trees and packaged `.skill` file are maintained without an in-repository build check, and the API-key workflow encourages printing or embedding a secret in commands.

## Design

### Cost gate

Add a short, hand-maintained `references/cost-gate.md` that agents read before every paid request. It distinguishes fixed per-call pricing from request-shaped pricing and supplies formulas for every special billing shape that is easy to mistake for a flat price. The main workflow will show the endpoint, billing unit, request inputs, upfront hold or maximum, and expected settlement before execution. It will request confirmation only when the user has not already clearly authorised a paid call.

Correct the affected endpoint headings and rows in the generated-looking references so a skim no longer presents a unit price as the total request cost. In particular, publish request-level spans or formulas for `prism/post-stats`, `prism/profiles`, `prism/comment-lookup`, `youtube/transcripts`, `web/batch-scrape`, and `web/sessions`, and document the 32-credit default `prism/ai-visibility` request.

### Credentials and errors

Resolve credentials without printing them. Prefer `SOCIALCRAWL_API_KEY`, fall back to the user config file, reject placeholder or malformed values, and ask the user to configure a missing key outside the chat. Never paste a key into generated code, command text, logs, or responses. Use a central error decision table that separates non-retryable request/auth/budget failures from retryable throttling and transient upstream failures, with bounded retries and idempotency guidance.

### Distribution

Treat `.agents/skills/socialcrawl` as the canonical source. Add a standard-library Python build script that synchronises `skills/socialcrawl` and `socialcrawl`, creates a deterministic `socialcrawl.skill` ZIP, and supports a read-only `--check` mode. Add CI to run the check. README instructions will use `skills.sh` for normal installation and upgrades, and expose a stable direct-download link to the committed package for users who want the latest artifact.

### Licensing and attribution

Add the standard MIT licence with SocialCrawl as the copyright holder. The README will state that derivative skills and plugins may reuse the work under MIT and that attribution through the included licence notice is sufficient.

## Verification

Automated validation will fail when:

- the three tracked trees differ;
- the `.skill` archive differs from the canonical tree;
- required files or valid skill frontmatter are missing;
- the known request-shaped endpoints regress to misleading flat headings;
- the cost-gate loses the verified formulas or examples;
- the skill tells an agent to print or inline the API key.

The final email will be drafted from the customer's two requests only, then passed through `codebase/docs/b2b/lint-oscar-voice.py` until clean.
