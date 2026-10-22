# Tracking, SEO and A/B variants

The template handles all of this from one `PAGE` config object near the bottom of the file:

```js
const PAGE = {
  ctaUrl:      "https://example.com/join",   // every .js-join button points here
  variant:     "A",                          // "A" or "B", added to every event
  pixelId:     "",                           // Meta pixel ID; leave empty to skip loading it
  gaId:        "",                           // Google Analytics 4 ID (G-XXXX); leave empty to skip
  contentName: "Offer page",                 // shows up in Events Manager
  value:       47,
  currency:    "USD"
};
```

## Events the template fires
| When | Meta pixel | GA4 |
|---|---|---|
| Page load | `PageView`, `ViewContent` {content_name: contentName + variant} | page_view (automatic) |
| Any join button click | `Lead` {content_name, content_category: button's `data-spot`} | `join_click` {spot, variant} |
| Video play | none | `video_play` {video, variant} |

The click handler waits 250ms before navigating so the Lead event has time to send. Clicks with Cmd or Ctrl held (opening a new tab) go through immediately.

**Pick one conversion event on purpose.** A Lead on click measures intent to join. If the owner's checkout can fire a Purchase event (for example through Conversions API on a thank-you page), tell the ads manager. Many campaigns should optimize for Purchase, not Lead.

## Passing attribution through
The template copies `fbclid` and `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` and `utm_term` from the page URL onto every join link. When the checkout lives on another domain (a community platform, a cart), this keeps the ad click attached to the conversion as far as that platform allows. `scripts/phone_check.mjs` loads the page with test values and reports any join button that drops them.

## Ad page vs. main site page
| | Cold ad page | Main site page |
|---|---|---|
| `meta robots` | `noindex, follow` | `index, follow` |
| canonical | points to the main page | points to itself |
| Header | no navigation | logo links home |
| Footer | legal links + "More about [offer]" | full site links + legal |
| Structured data | not needed | `Product` JSON-LD with real price, rating and review count |
| Tag Manager | only if the site uses it | keep whatever the old page had |

If the site loads both Tag Manager and an inline pixel, check that the Tag Manager container doesn't fire the same pixel again. Otherwise PageView gets counted twice.

## Product JSON-LD (main pages)
```json
{
  "@context": "https://schema.org", "@type": "Product", "name": "[Offer]",
  "description": "[What it is, who it's for, the format, the price, the cancel policy]",
  "url": "https://example.com/offer", "image": "https://example.com/og.jpg",
  "brand": {"@type": "Brand", "name": "[Brand]"},
  "offers": {"@type": "Offer", "price": "47", "priceCurrency": "USD",
             "url": "https://example.com/join", "availability": "https://schema.org/InStock"},
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "bestRating": "5", "reviewCount": "10"}
}
```
Use only numbers you can see on the public review page.

## Running an A/B test
1. Build both versions on the same template. Version B usually changes the hero image, the angle and the sections listed in `copy-playbook.md`.
2. Give each version its own URL (for example `/join` and `/offer`) and its own `PAGE.variant`.
3. The ads manager points one ad set at each URL with identical creative and budget, inside the ad platform's A/B test tool, so the platform splits traffic fairly.
4. When a page that already gets organic traffic becomes one of the variants, its numbers mix ad and organic visitors. Compare the two by ad set inside the ad platform, not by raw page events.
5. If a URL ever changes, add a redirect from the old one (for example `/join-b` to `/join`) in case an ad was already built with it.
6. Decide the winner on the conversion that pays (purchases or joins), not on clicks.

## Publishing safely
- Never publish without the owner's go-ahead. Pages are public the moment they deploy.
- Static hosts (Vercel, Netlify, GitHub Pages, Cloudflare Pages) serve the HTML and the assets folder as-is.
- When the site deploys from git:
  - Commit only the files you changed.
  - If another deploy is building, wait for it to finish before pushing, because overlapping deploys can let an older build win.
  - Some automated jobs commit everything in the folder. Build unfinished pages on a branch or in a separate worktree so they can't ship by accident.
- After deploying, check the URL with a cache-busting query (`?cb=123`) and without one. Then confirm each new asset returns 200 or 206.
