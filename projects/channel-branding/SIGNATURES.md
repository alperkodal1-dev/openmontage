# Unsealed History: channel signatures (read this before every new Short)

The house style of the channel, collected from the published Shorts (Noah's Ark, Piri Reis, Salem, Rome, Great
Pyramid). Every new video should use all of these unless the owner asks otherwise. Reference implementation:
`projects/egypt-pyramids/` (the newest, with every signature in place). Reusable code: `signatures/`.

## 1. The opening: a signature question, then the grey shock
- The video opens on ONE short, provocative line that states what "everyone knows" and doubts it in the same
  breath, voiced separately and placed before the narration:
  - Noah: "The Bible never says Noah's Ark landed on Mount Ararat... Not once."
  - Piri Reis: "How many of us are really sure what's in Antarctica?"
  - Pyramid: "Slaves built the pyramids... or did they?"
- On screen: the subject's picture full frame, a big two-line Cinzel title of the claim ("BUILT BY / SLAVES?",
  bone + gold), and the red stamp with the doubt ("...OR DID THEY?").
- **The grey signature** on the doubt ("or did they?" / "or does it?"): the picture snaps to
  `grayscale(1) sepia(.4) contrast(1.25) brightness(.8)`, shakes for ~0.55 s, then a bone-white flash
  (`#f4ead2`, 0.85 opacity, 0.06 s in, 0.3 s out). Sound: hit + rumble on the first word, hit on the doubt.
  Code: `signatures/grey_signature.js`.
- The question must be answered (or honestly left open) by the evidence in the body.

## 1b. The story turn: "Or so the story goes." (story-led videos)
- When a video first tells the legend as a story (Salem, Rome), the legend ends on a climax line, and the
  narrator closes it with its own short sentence: **"Or so the story goes."** Then the evidence begins with a
  plain turn: "But the records say otherwise." (Salem), Livy / the evidence chapter (Rome).
- On screen, on "Or so...": the legend picture (often the cold-open picture again, Rome) snaps to grey
  (`grayscale(1)`, a little darker), the legend's labels and chapter title drop, and the red stamp **MYTH** slams
  in (Salem) a beat later. Sound: hit + rumble on "Or", the score drops to its low bed for the evidence.
- The climax line before it gets a big Cinzel two-line title over warm, fiery light (Salem: "...AND THEY BURNED").
- Code: `signatures/grey_signature.js` (`storyGoes`).

## 2. Look
- Vertical 1080x1920. Top 250 px clear for the platform UI; karaoke captions on a dark plate at y 1235-1615.
- Fonts (self-hosted): Cinzel (titles, tags, stamps), Cormorant Garamond italic (quotes, asides), Manrope (captions).
- Palette: ink `#0a1417`, bone `#efe6d2`, gold `#d9b26a` / `#f1d49a`, red stamp `#9c2f1f` with `#ffe9c4` text.
  Mystery/legend accent (alien, magic, myth): green `#7dffb0` (tags, scan line, glow).
- One card on screen at a time; the picture changes every 1.5-3.5 s; slow Ken Burns on every background.
- Karaoke captions, word by word: spoken word turns gold; legend/myth keywords green, evidence keywords orange `#ff9a6b`.
- Archive pictures only (public domain / CC, credited): Wikimedia Commons (`tools/fetch_commons.py`, waits on 429s),
  The Met Open Access API (CC0, `collectionapi.metmuseum.org/public/collection/v1.1/search`), Natural Earth maps.
  Put a small credit line on CC BY-SA photos.
- Claims of the legend get the "clue" treatment: the picture card, a green scan line sweeping down, a grid, a ring on the
  detail, and "CLUE 1/3" above.
- Real people get a framed portrait card with name tags under it.

## 3. Story and voice
- Format: "the story everyone thinks they know, traced back to the sources". Legend told vividly but attributed
  ("some claim", "his followers", "seems to show"); evidence stated plainly; a source list in `sources.md`.
- Narrator: vidIQ voiceover, George (voiceId `JBFqnCBsd6RMkjVDRZzb`), measured ~141 wpm; 145-160 words for 60-70 s.
- Ending: the last line is an open question that returns to an earlier detail; the REAL / MYTH poll card appears with it.
  Show the subject's picture under the closing question in big Cinzel ("WHAT WERE THE PYRAMIDS, REALLY?").

## 4. Sound
- Score: generated mysterious orchestral (vidIQ), sitting 5-10 dB under the narrator (bed gains about 0.07-0.14 for a
  -10.6 LUFS track) with side-chain ducking; it lifts in the legend passages and drops under the evidence.
- End music (if the owner gives one) fades in softly under the closing question and rises slowly, never louder than
  the narration (about -20 to -16 LUFS against narration at -14.5). Warn the owner once about Content ID for
  commercial songs; the decision is theirs.
- Final mix -14 LUFS, true peak -1.5 dB.

## 5. Cover
- Vertical 1080x1920, the subject's picture, a two-line Cinzel headline (bone line + gold line, gold may be a metallic
  gradient), a red stamp at the bottom ("PIRI REIS · 1513", "ROME · 753 BC", "THE GREAT PYRAMID").
  Examples: `piri-reis-map/thumb/`, `rome-murder/thumb/`, `egypt-pyramids/thumb/`.

## 6. Delivery
- QC: duration, -14 LUFS, no black frames, no frozen picture over 3.5 s, no silence; frame sheets checked by eye.
- Turkish SRT for the owner; subtitles in en, tr, es, pt, de, fr, ja uploaded with
  `channel-branding/subtitles/yt_captions.py` (YouTube Data API; 25 tracks a day on the default quota).
- Titles scored with vidIQ before upload. Always ask the owner before spending credits and before publishing.
