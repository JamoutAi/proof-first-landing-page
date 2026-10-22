# Proof hunt

Spend real effort here. The difference between a forgettable page and one the owner loves is usually 25 more testimonials, 4 member videos and the right photo, all of which already exist somewhere on their computer.

## 1. Where to look

Search wide, then narrow. Typical places:

- **Notes, vault or docs folders:** files and folders named testimonial(s), review(s), wins, love, case stud(y/ies), feedback, social proof.
- **Spreadsheets of testimonials:** `.xlsx` and `.csv` often hold name, role, company, quote and photo link. Read them with Python (`openpyxl`, or unzip the xlsx and parse `xl/sharedStrings.xml` and `xl/worksheets/sheet1.xml`).
- **Screenshot folders:** names like "Testimonial Images" or "Wins", or the desktop. Screenshots of community posts and DMs are gold.
- **Photo folders:** "Pictures of [Name]", headshots, branding shoots, event photographer folders (often named after the event), phone photos (HEIC).
- **Downloads:** logos (`*logo*`), logo bars, recorded videos, exported reels.
- **Video folders:** finished-videos folders, Movies, meeting recordings (Zoom names files like `GMT2026...Recording_gallery...mp4`), screen recordings.
- **The community or course platform:**
  - Its public About page (member count, rating, price, description).
  - Its reviews.
  - Its calendar. Ask before using a logged-in browser session, and only read.
- **Call notes and transcripts:** quotes said on group calls, often already collected into a "testimonial bank" note.
- **Existing site pages:** older landing pages often hold approved quotes, member photos and structured data.

Useful commands:

```bash
# files and folders whose names suggest proof (adjust the roots)
find ~/Documents ~/Desktop ~/Downloads "<notes-folder>" -maxdepth 6 \
  \( -iname "*testimonial*" -o -iname "*review*" -o -iname "*wins*" -o -iname "*logo*" \) 2>/dev/null

# every video with its length and size
find ~/Movies ~/Downloads -maxdepth 3 -type f \( -iname "*.mp4" -o -iname "*.mov" \) -print0 \
  | xargs -0 -I{} sh -c 'printf "%s\t%s\n" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "{}")" "{}"'
```

When you search notes with `grep --include=*.md` in zsh, quote the flag (`'--include=*.md'`) or the shell will try to expand it.

## 2. Look, don't guess

- **Images:** `python3 scripts/contact_sheet.py out.jpg 6 260 list.txt` makes a numbered grid, and the matching file names are printed. View it, then pick by number.
- **Videos:** grab a frame at 30% of the way through each file, then contact-sheet the frames. For long recordings, sample a frame every 150 seconds to find the gallery-of-faces moments and the screen-share moments.
- **Words in videos:** transcribe with faster-whisper (`small.en` is fast on CPU) before choosing clips or writing bullets about the video.

## 3. Show the owner an inventory

Before building, summarize in plain words. For example: "I found 31 testimonials (12 tiles, 8 photo reviews, 9 community posts, a live-chat strip), 4 member video stories, 187 photos including real stage shots, 8 logos, your intro video and 7 sessions I can pull clips from." Owners light up at this step, and often point you to even more.

If nobody is around to answer, keep building and put this inventory at the top of your final report, along with what's missing (for example "no usable photos of you, so I used the no-photo fallbacks").

## 4. Checks before anything goes on the page

- **Consent scope.** Was the person asked to be featured for something else (a partner's webinar, a podcast, an internal group)? Build it, but flag it: "Alex and Sam agreed to the [partner] video. Worth a quick OK text before ads."
- **Brand permissions.** Client logos and client names can be confidential. Check whether the owner's own docs already list a brand as OK to mention. Leave out logos you can't trace to a real engagement.
- **Freshness.**
  - Videos and old pages often promise discontinued things: trials, prices, perks, "30 days" when it's now 7.
  - Trim the clip or leave it out.
  - Round down only the numbers that change often, like member counts, unless the owner already gave a rounded figure. Keep ratings and review counts exact, and check them again at launch.
- **Sensitive details.** Leave out posts that reveal health, money trouble, family conflict, or children's names or photos, unless the person shared them publicly for this purpose. Everyday context people give about themselves ("mom of two", "my kids love it") is fine.
- **Retired offers.** A glowing review of a perk that no longer exists misleads buyers. Skip it.
- **Image quality.** Screenshots smaller than about 1000px wide are unreadable once shrunk into a card. Retype them as styled cards, word for word.

## 5. Where each kind of proof goes

| Proof | Best section |
|---|---|
| Founder cutout or portrait | Hero, final call to action |
| Real working photo (desk, laptop, product) | Hero of variant B, the room |
| Stage or event photos | Meet the founder collage, background of the authority band |
| Member faces (avatars) | Hero proof row, wall of love photo reviews |
| One short, punchy result quote | Hero badge grid |
| Logos | Logo strip |
| Founder tour or intro video | Video tour |
| Gallery-of-faces and demo moments from recordings | Session reel in the room |
| Recurring events from the calendar | Events calendar |
| Public platform page and reviews | Platform screenshots |
| Text testimonials, posts, chat lines, result tiles | Wall of love |
| Member video clips | Video testimonials |
| Certificates and credential badges | Meet the founder |
| Partner or client quotes | Authority band |
| Real member count, rating and review count | Proof row, price section, structured data |
