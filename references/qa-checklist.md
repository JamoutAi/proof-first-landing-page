# QA checklist

Run all of this before showing the owner. Each item caught a real bug at least once.

## Content and honesty
- [ ] Every testimonial is word for word, trimmed only with "...", with the right name and role.
- [ ] No doubled quote marks. The `q` element adds its own, so don't type quotes inside it.
- [ ] Display quotes use curly quotes, not straight ones.
- [ ] No outdated claims anywhere: old trial offers, old prices, old program length, perks that no longer exist. Check the videos too.
- [ ] Numbers: member counts that change often are rounded down in text ("450+") unless the owner gave a rounded figure. Ratings and review counts are exact and were checked again today.
- [ ] Five stars appear only where the rating rounds to 5, and on reviews that gave 5.
- [ ] Tenure badges match what the platform shows.
- [ ] Credential wording is truthful ("certified", "completed").
- [ ] Defaults that read like copy are true for this offer, or gone: "cancel anytime", "every session is recorded", "Day 1 starts today", "no call to talk you out of it".
- [ ] No placeholder text or placeholder boxes left:
  - `grep -nE '\[[A-Za-z$(]' page.html | grep -vE '\[(aria|data)-'` lists any bracketed text still in the file. Searching for a bare `[` drowns in code.
  - `phone_check.mjs` reports `placeholderText` and `placeholderBoxes` from what's actually visible. Both should be empty or zero.
- [ ] Nothing the owner flagged as private (client names, logos, health details).
- [ ] The owner's banned words and punctuation preferences are respected (for example, no em dashes if they dislike them).

## Layout
- [ ] Nothing floats on the hero photo. Badges sit in the grid underneath.
- [ ] Desktop at 1440 wide: the hero's text and visual balance, and the badges fit.
- [ ] Phone at 390 wide:
  - The hero button shows on the first screen.
  - The proof-row text doesn't overlap the avatars.
  - The sticky bar appears after the hero and hides over the price card. Check this with `phone_check.mjs`. The tall iframe in `page_shots.sh` can never show the bar.
- [ ] No sideways scrolling on phones. In the browser console, `document.documentElement.scrollWidth > innerWidth` should be `false`.
- [ ] Photo frames fill their columns (`figure{margin:0}` is set).
- [ ] No empty dark strip under the session reel. The video window sizes to its video, and the side photos stretch to match.
- [ ] Section backgrounds alternate (light, tinted, light). Two of the same in a row looks like one long section. Deleting optional sections often breaks the pattern, so re-check `band--alt` after deleting.
- [ ] Certificates and screenshots keep their shape (`height:auto` when width is 100%).
- [ ] Wall of love: with 12 or fewer cards, there's no Show more button and no card has `m-hide` or `more`.
- [ ] No link points at a deleted section (for example the hero's "Watch the tour" link when the video tour is gone).

## Brand
- [ ] The tokens in `:root` are the brand's, and the Google Fonts link loads the fonts `--font` and `--script` name.
- [ ] `--sig` is the brand's sign-off emoji, or `""`.
- [ ] `meta theme-color` matches `--page`.

## Media
- [ ] Every image loads. `phone_check.mjs` lists `brokenImages` after scrolling the whole page, or run `[...document.images].filter(i=>i.complete&&!i.naturalWidth)` in the console at the bottom of the page.
- [ ] Each video plays with sound when clicked, only one plays at a time, and the poster is a good frame.
- [ ] Caption tracks show where captions aren't burned in, and misheard words are fixed.
- [ ] The session reel autoplays muted only while on screen, and its label changes with each clip.
- [ ] File sizes: photos under 200 KB, looping video under 3 MB, click-to-play clips under 10 MB.

## Tracking and SEO
- [ ] Every join button points to the same destination, with `fbclid` and `utm_*` passed through. `phone_check.mjs` loads the page with test values and reports `joinDestinations` (should list one URL) and `joinMissingPassThrough` (should be empty).
- [ ] Pixel and analytics IDs are set, or deliberately left empty.
- [ ] `PAGE.variant` is correct for this version.
- [ ] Ad page: `noindex`, canonical to the main page.
- [ ] Main page: `index`, self canonical, Product JSON-LD that parses with real numbers.
- [ ] Title and meta description describe the offer. The open graph image is set.

## Screenshots for the owner
```bash
bash scripts/page_shots.sh "http://localhost:8000/index.html" shots/
node scripts/phone_check.mjs "http://localhost:8000/index.html" shots/
```
The first makes `desktop.jpg` and `phone-1.jpg` through `phone-N.jpg`. The second prints its checks and saves `phone-viewport-midpage.png` (the sticky bar should show) and `phone-viewport-price.png` (it should hide). Look at every image yourself first, then send them.

If you script your own scroll checks, set `document.documentElement.style.scrollBehavior = 'auto'` first. The template scrolls smoothly, so a scripted `scrollTo` is still moving when you measure.
