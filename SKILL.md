---
name: proof-first-landing-page
description: Build a high-converting, mobile-ready landing page for any offer (membership, course, coaching program, service, product or event) from a proven 17-section layout and a proof-first workflow. Use this whenever someone wants a landing page, sales page, join page, opt-in page, Meta or Facebook ad landing page, or an A/B test version of an existing page, even if they only say "make me a page for my offer" or share a page they admire. It hunts down their real testimonials, photos, logos and videos before writing a word, turns photos into clean professional cutouts, and ships one fast HTML page with tracking, captions and desktop plus phone screenshots for review.
---

# Proof-First Landing Page

A landing page converts on proof, not adjectives. Strangers from an ad believe three things: real people who got a result, the founder's face and voice, and a clear next step. This skill builds pages in that order. You go find the owner's proof first, then write the page around it.

The layout comes from a membership page that went through two rounds of real owner feedback and an A/B test brief from a paid-ads manager. Every rule below is something an owner asked for, or a mistake that got caught. When you follow a rule, you're skipping a revision round.

## The workflow

1. **Intake.** Ask for only what you can't find yourself.
2. **Proof hunt.** Inventory everything before writing any copy. This step makes or breaks the page.
3. **Angle and outline.** Pick the copy angle and map the proof onto the 17 sections (plus the header).
4. **Media prep.** Make cutouts, single-color logos, trimmed videos with captions, a session reel and screenshots.
5. **Build.** Fill `assets/landing-template.html`. Delete any section you have no proof for, or use its no-photo fallback.
6. **Tracking and variants.** Add the pixel and conversion events, pass UTMs through, and give each A/B version its own URL.
7. **QA.** Run through the checklist, take full-page desktop and phone screenshots, and run the phone check.
8. **Hand-off.** Show the screenshots, list the open questions, and publish only after the owner says yes.

Work through these in order. Show the owner what you found after step 2 and what you built after step 7. Those are the two moments they most want to weigh in.

**When nobody is there to answer** (a background run, or an owner who said "just build it"): don't stop and wait. Make the sensible default choice, note it, and keep going. Then put the proof inventory, every choice you made for them and the open questions at the top of your final report.

## 1. Intake

Collect these. Look for each answer yourself before you ask.

- **Offer.** The name, a one-line promise, who it's for, and the price and billing.
- **One call-to-action URL.** Every button on the page goes to the same place, for example the checkout or join page.
- **Brand.** Logo file, two or three colors and fonts. If they have a website, pull these from it.
- **Where their proof lives.** Folders, spreadsheets, a notes vault, a community platform, a review page.
- **Traffic type.**
  - *Cold ad traffic:* the page has no site navigation, is marked noindex, and points its canonical to the main page. Ask for the main page's URL.
  - *Main site page:* it's indexable, the logo links home, and the footer has site links.
- **Tracking.** Ad pixel ID and analytics ID, if they use them.
- **Hosting.** Where the page will live, and its URL slug.

If the request is genuinely unclear, ask one focused clarifying question, then build. Owners would rather react to a draft than fill out a questionnaire.

## 2. Proof hunt (before any copy)

Read `references/proof-hunt.md` for where to look, how to inventory quickly, and the checks to run.

First drafts fail when they're built from the five testimonials that happen to be in the conversation, while the owner has fifty more in folders. One owner's reaction to a thin first draft was "I have SO many testimonials. I have so many pictures." Hunt wide:

- Written testimonials, reviews, chat messages, community posts and call transcripts
- Photos of the founder. Real photos beat AI-generated ones, especially near member proof.
- Logos of organizations they've trained, spoken for or worked with, if they're allowed to show them
- Videos: a founder intro or tour, member testimonial clips, and recordings of live sessions
- Their public community or course platform page (member count, rating, reviews), plus credentials and certificates
- The real calendar of recurring events

Use `scripts/contact_sheet.py` to actually look at images and video frames instead of guessing from file names. Before building, give the owner a short inventory, like "I found 31 testimonials, 4 video stories, 187 photos and 8 logos."

**Honesty rules (non-negotiable):**
- Quote people word for word. Trim only with "...".
- Never invent a testimonial, statistic, logo or result.
- Round down only the numbers that change often, like member counts ("450+"), unless the owner already gave you a rounded figure. Keep ratings and review counts exact, and check them again right before launch.
- Show five stars only when the real rating rounds to 5.
- If someone agreed to be featured somewhere else (a partner's webinar, a podcast), flag them so the owner can confirm before they appear in an ad.
- Transcribe every video before using it. Old clips often promise things that have changed, like a free trial that's over or an old price. Trim those lines out.
- Leave out sensitive details (health, money trouble, family conflict, children's names or photos) unless the person shared them publicly for this purpose. Everyday context people give about themselves, like "mom of two" or "my kids love it", is fine.

## 3. Angle and outline

Read `references/page-outline.md` for all 17 sections: what each is for, which proof goes in it, and its copy formula. Read `references/copy-playbook.md` for the headline formulas and the fears, frustrations, dreams and desires worksheet.

There are two proven angles. Both use the same structure, so an A/B test is cheap to build:

- **Angle A, outcome-first.** The headline names the transformation and the timeframe ("Seven days from now, AI knows your business."). The hero is the founder.
- **Angle B, pain-first.** The headline calls out the audience and their burden ("You didn't start your business to do everything yourself."). B also adds a fears and frustrations section, a "Right now vs. With [offer]" table, every recurring event, and screenshots of the real platform page. Its hero is a real working photo.

**Building just one page?** Use B for cold ad traffic aimed at a specific audience, because strangers need to feel called out before they care about the result. Use A for warm traffic and main site pages, where people already know the founder. If you can't tell, build A for the main page and offer B as the test version for ads.

## 4. Media prep

Read `references/media-recipes.md` for exact commands. In short:

- **Founder cutouts:**
  - On macOS, use `scripts/cutout.swift` (Apple Vision subject lift).
  - Check the edges against the brand color.
  - If the image cuts off flat at the top of the head, let the page's arch or rounded shape crop it.
- **Logos:** `scripts/logo_mono.py` recolors every logo to one ink color so the strip looks designed.
- **Videos:**
  - Trim and re-encode to 720p H.264 with faststart.
  - Make a poster frame of the person smiling, with no caption on screen.
  - Build captions with `scripts/make_vtt.py`, then hand-fix any misheard words.
  - Skip the caption file if captions are already burned into the video.
- **Session reel:** `scripts/session_reel.py` turns 5 to 8 moments from real recordings into a silent 15 to 20 second loop with timed labels.
- **Platform screenshots:** capture the logged-out public view with headless Chrome, so no admin buttons show.
- **Image formats:** export photos as webp. Keep each photo under about 200 KB and each looping video under about 3 MB.

## 5. Build

Copy `assets/landing-template.html` into the project, named after the page slug. Then:

1. Set the brand tokens in `:root` (colors, fonts and the `--sig` sign-off emoji) and swap the Google Fonts link for the brand's fonts. Then set the `PAGE` config at the bottom of the script.
2. Fill the sections in order. Each one is marked with an HTML comment.
3. Sections marked OPTIONAL need real proof. Delete any you can't fill. A placeholder left on a live page looks worse than a missing section.
4. No usable founder photos yet? Use the no-photo fallbacks in the template: a member quote in the hero arch, a fact card for Meet the founder, and a "What happens next" card for the final call to action.
5. Replace every bracketed default, even the ones that read like finished copy ("[cancel anytime]", "[Day 1 starts today]"). Keep each one only if it's true for this offer.

Layout rules (each one came from owner feedback or a bug that shipped):

- **Nothing floats on top of the hero photo.** Badges, rating chips, quote cards and stickers go in a row or grid under the photo. One owner called floating items "distracting" on two different versions of the same page.
- **Use real photos for proof.** An AI-generated "founder on a stool next to a screen of faces" got swapped out immediately for a real screenshot of members on a call.
- **One destination for every button.** Vary the button text by section ("Start Day 1", "Save me a seat", "Get my time back").
- **Show a lot of proof, but don't make people scroll forever.** With more than 12 cards, show about 12 on the wall of love (8 on phones) and put the rest behind "Show me more love". With 12 or fewer, show them all and delete the button.
- **Design for phones first.** The hero button must be visible on the first phone screen, the sticky bar must appear once the hero scrolls away, and nothing can scroll sideways.
- **Load fast.**
  - Lazy-load everything below the fold.
  - Set `preload="none"` on click-to-play videos.
  - The silent session reel plays only while it's on screen.
- **Set `margin:0` on every `figure`.** Browsers add 40px side margins by default, which quietly shrinks photos inside their frames.

## 6. Tracking and variants

Read `references/tracking-and-testing.md`. The template already handles these, driven by `PAGE`:

- The Meta pixel fires PageView and ViewContent when the page loads, and Lead when someone clicks a join button. Navigation waits 250ms so the event can send.
- Analytics events are labeled with the variant name.
- `fbclid` and `utm_*` are copied from the page URL onto the call-to-action link, so the ad click carries through.

For an A/B test, give each version its own URL and its own variant label. Ad pages are noindex. The main page stays indexable and keeps its Product structured data, using only real numbers.

## 7. QA

Work through `references/qa-checklist.md`. Then run both scripts:

- `bash scripts/page_shots.sh <url> <out-dir>` saves a full-page desktop screenshot (1440 wide) and a true 390px phone screenshot. The phone shot is drawn in a very tall 390px iframe, because headless Chrome won't go narrower than about 500px. The sticky phone bar can't appear in that frame, so check it with the next script.
- `node scripts/phone_check.mjs <url> <out-dir>` scrolls a real phone screen and reports sideways scrolling, the hero button, the sticky bar at each stop, broken images, leftover placeholders and UTM pass-through on every button. It also saves two phone-screen shots.

Look at every screenshot yourself before showing the owner. Typical catches:
- doubled quote marks
- a photo shrunk by a default margin
- an empty dark strip under a video
- text overlapping an avatar row on phones

## 8. Hand-off

Send the owner the screenshots (split very tall phone shots into 5 or 6 parts so they stay readable). Then:

- List the open questions in plain words: consent, logos they may not want public, claims that need checking. If you used a no-photo fallback, ask for photos first, because real photos change the page more than anything else.
- Publishing is the owner's call, so ask before deploying. Give deploy steps for their host.
- After it's live, check the real URL with a cache-busting query and the plain URL both, and confirm every new asset loads.

## Voice defaults

Match the owner's voice. If they have words they never use, honor them. Without guidance:
- Write warm, direct and specific.
- Use numbers over adjectives, and one emphasized phrase per headline.
- Avoid AI-sounding filler like game-changer, unlock, elevate, seamless, dive in, unleash, revolutionize and supercharge.
