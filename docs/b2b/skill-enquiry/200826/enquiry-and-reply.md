# SocialCrawl skill licensing and pricing enquiry

## Enquiry

Hi,

I've been building a SocialCrawl plugin for Claude Code. It wraps your API with a per-platform reference set, a cost gate that shows credit prices before a call runs, and guidance that steers agents to the cheapest endpoint that answers the question. It's been a genuinely good API to build on.

Two things brought me to you.

First, licensing. Parts of my skill are derived from github.com/socialcrawl/skills, especially the key-resolution steps and the error-code handling. That repo has no LICENSE file, while socialcrawl/mcp is MIT, so I'm assuming the omission is an oversight rather than intent. I'd like to publish my plugin publicly, and I don't want to do that on top of your work without knowing where you stand. Would you be willing to add a LICENSE to the skills repo? If MIT matches your intent there, that would settle it. Happy to attribute however you prefer.

Second, a bug worth your time regardless of the licensing answer. Your published pricing lists prism/post-stats at 1 credit, but it bills per URL. A 100-URL batch is 500 credits, not 1. The same pattern affects several other endpoints that meter per row, probe, or page; prism/ai-visibility is listed at 2 credits but bills 2 per probe, so a default call with 8 runs and 2 engines is 32. Agents read those numbers and act on them, so the gap tends to surface as a surprise bill rather than an error. Glad to send the full list I've compiled.

Thanks,

## Reply

Hi there,

Thank you for the message.

We have now made the licensing and pricing changes.

Yes, MIT matches our intent for the skills repository. We have added the licence and rebuilt the latest skill package in the repository. You are welcome to publish your plugin and reuse the key resolution and error handling material under those terms. Retaining the MIT notice is sufficient attribution. A link to the SocialCrawl skills repository is appreciated but is not required by the licence.

We traced the pricing issue across every request shaped endpoint and corrected the skill so it calculates the whole request before making a paid call. `prism/post-stats` now shows its per URL billing and maximum batch exposure, while `prism/ai-visibility` shows the probe formula and default request cost. We also added release checks that prevent these figures and the downloadable package from drifting.

Please do send over the full list you compiled. We have covered the batch, probe, page, runtime and recurring billing paths in this release, but comparing your list against ours would still be useful as a final cross check. Thank you for taking the time to document the cases you found while building the plugin.

Hope that this helps!

As always, please let me know if you have any questions.

Best regards,
Oscar
Co-founder of SocialCrawl
