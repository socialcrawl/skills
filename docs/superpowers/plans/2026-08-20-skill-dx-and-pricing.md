# SocialCrawl Skill DX and Pricing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a licensed, cost-safe, securely configured, reproducibly packaged SocialCrawl skill with a customer reply in Oscar's voice.

**Architecture:** `.agents/skills/socialcrawl` remains the canonical skill tree. A Python standard-library build/check script synchronises the two public mirrors and deterministically rebuilds `socialcrawl.skill`; the skill itself routes paid work through a new request-shaped cost gate before execution.

**Tech Stack:** Markdown, Python 3 standard library, GitHub Actions, ZIP-compatible `.skill` packaging

---

### Task 1: Add failing distribution and content checks

**Files:**
- Create: `scripts/build_skill.py`
- Create: `.github/workflows/validate-skill.yml`

- [ ] **Step 1: Implement `--check` validation**

Validate the canonical frontmatter, required references, mirror equality, packaged archive equality, key-safety phrases, and request-shaped pricing invariants. Exit non-zero and name every mismatch.

- [ ] **Step 2: Run the check to verify the current repository fails**

Run: `python scripts/build_skill.py --check`

Expected: FAIL because there is no licence or cost-gate reference and the affected headings still advertise unit costs as request totals.

- [ ] **Step 3: Add CI**

Run the same command on pushes and pull requests with Python 3.12.

### Task 2: Add licensing and distribution documentation

**Files:**
- Create: `LICENSE`
- Create: `CHANGELOG.md`
- Modify: `README.md`

- [ ] **Step 1: Add the MIT licence**

Use the standard MIT grant and notice, with copyright year 2026 and SocialCrawl.

- [ ] **Step 2: Fix install and update paths**

Keep `npx skills add socialcrawl/skills` as the recommended installer, document the upgrade command, replace the broken clone-at-skill-root example, and link the latest committed `.skill` download.

- [ ] **Step 3: Document derivative use and this release**

State that the bundled skill can be reused under MIT with the licence notice retained, and add a concise changelog entry covering pricing, secrets, errors, and deterministic packaging.

### Task 3: Harden the canonical skill

**Files:**
- Modify: `.agents/skills/socialcrawl/SKILL.md`
- Modify: `.agents/skills/socialcrawl/references/api-overview.md`
- Create: `.agents/skills/socialcrawl/references/cost-gate.md`

- [ ] **Step 1: Replace secret-revealing key resolution**

Do not echo, interpolate, or persist pasted keys from chat. Resolve environment and config sources silently, validate the `sc_` shape, give secure setup instructions when missing, and use variable references in examples.

- [ ] **Step 2: Make the cost gate universal**

Before every paid call, calculate the request-shaped estimate and display endpoint, formula, hold or maximum, refund behaviour, and balance impact. Skip an extra confirmation only when the user already authorised that exact paid request.

- [ ] **Step 3: Make retry behaviour bounded and actionable**

Separate fix-before-retry errors from `Retry-After` errors and transient errors. Require idempotency keys on retryable paid non-streaming requests and cap automatic transient retries.

### Task 4: Correct request-shaped pricing references

**Files:**
- Modify: `.agents/skills/socialcrawl/references/pricing.md`
- Modify: `.agents/skills/socialcrawl/references/prism.md`
- Modify: `.agents/skills/socialcrawl/references/youtube.md`
- Modify: `.agents/skills/socialcrawl/references/web.md`

- [ ] **Step 1: Correct batch endpoint headings and table rows**

Publish `prism/post-stats` as 1 to 500 credits per request, `prism/profiles` as 1 to 250, `prism/comment-lookup` as 2 to 100, and `youtube/transcripts` as 3 to 300, with successful-row settlement and failed-row refunds.

- [ ] **Step 2: Correct web request-shaped costs**

Describe `web/batch-scrape` as N credits for N submitted URLs and `web/sessions` as a 5 to 20 credit TTL-shaped hold. Preserve the existing crawl and recurring-monitor warnings.

- [ ] **Step 3: Make AI visibility's default concrete**

Document `2 × prompts × runs × engines`, with a one-prompt default of `2 × 1 × 8 × 2 = 32` credits and the optional 5-credit web baseline.

### Task 5: Synchronise, package, and verify

**Files:**
- Regenerate: `skills/socialcrawl/**`
- Regenerate: `socialcrawl/**`
- Regenerate: `socialcrawl.skill`

- [ ] **Step 1: Build all distribution forms**

Run: `python scripts/build_skill.py`

Expected: the two mirrors become byte-identical to the canonical tree and `socialcrawl.skill` is rebuilt deterministically.

- [ ] **Step 2: Run the complete validation**

Run: `python scripts/build_skill.py --check`

Expected: PASS with mirror, archive, frontmatter, key-safety, licensing, and pricing checks listed.

- [ ] **Step 3: Inspect repository state**

Run: `git diff --check` and `git status --short`

Expected: no whitespace errors; only intended skill, documentation, automation, and package files changed.

### Task 6: Draft and lint the customer reply

**Files:**
- Create: `docs/b2b/skill-enquiry/200826/enquiry-and-reply.md`

- [ ] **Step 1: Answer the two requests only**

Confirm the MIT licence, acceptable attribution, corrected pricing, and availability of the full list, without adding unasked commercial or contractual claims.

- [ ] **Step 2: Run Oscar's voice lint**

Run from `../codebase`: `python docs/b2b/lint-oscar-voice.py ../socialcrawl-skills/docs/b2b/skill-enquiry/200826/enquiry-and-reply.md`

Expected: PASS with a complete coverage ledger.

- [ ] **Step 3: Include the final reply in the handoff**

Provide the clean draft verbatim and identify the local draft path.
