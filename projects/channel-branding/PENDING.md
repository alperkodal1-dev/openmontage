# Open items (as of 2026-11-17) — read this at the start of a new chat

Channel: renaming from "Unsealed History" to "Or So The Story Goes" (UC-56SCswc-CVcH835YjGyow). Owner renames it in Studio; then run `channel-branding/rename_channel.py` (video descriptions/tags + channel description/keywords). House style: `SIGNATURES.md` (incl. section 7, vidIQ lessons).

## Waiting for the owner's channel verification (custom thumbnails)
Thumbnail uploads are blocked ("too many thumbnails" / verification). Once https://www.youtube.com/features shows
custom thumbnails enabled, set (owner may do it in Studio):
| Video | ID | State | Cover (vidIQ score) |
|---|---|---|---|
| Great Pyramid | eb9hr58dpCI | public | `egypt-pyramids/thumb/pyramid_cover_e.jpg` (86) |
| Noah, 59 s Shorts cut | hgJgE_9AVFo | public | `noah-ark/thumb/noah_cover_b.jpg` (91) |
| Noah, 72 s long cut | AuveB2unXDM | private draft | `noah-ark/thumb/noah_cover_b.jpg` (owner sets it) |

## Other open items
- Noah long cut (AuveB2unXDM): captions tr, es, de, fr, ja hit the daily API quota; upload with
  `noah-ark/publish_long/captions_rest.py` (a reminder was scheduled for 2026-11-18 08:20 UTC in the old session).
  Title is the proven original "The Mistake Everyone Makes About Noah's Ark #shorts #bible".
- When the owner publishes the long cut: post the comment (from `publish_long/metadata.json`), and ask whether to
  take down the 59 s cut (hgJgE_9AVFo) so the same video is not up twice.
- Pin the comments on eb9hr58dpCI and hgJgE_9AVFo in Studio (the API cannot pin).
- Remaining caption tracks on older videos (Ankara de; fr and ja on the five older Shorts): `subtitles/yt_captions.py`.
- Owner should rotate the OAuth client secret (it was pasted in chat). The refresh token lived only in the old session's
  scratchpad and expires after ~7 days in Testing mode: a new chat needs a fresh OAuth code
  (`yt_upload_video.py`, `egypt-pyramids/publish/finish.py` read YT_OAUTH_JSON / YT_CLIENT_ID / YT_CLIENT_SECRET).

## Tools
- Upload with metadata: `yt_upload_video.py <mp4> @<publish>/metadata.json [private|public]`
- Everything after upload (metadata, captions, comment, optional thumbnail): `egypt-pyramids/publish/finish.py <id> <privacy> <publish dir>`
- YouTube API daily quota: 10,000 units (upload 1600, caption 400).

## Parked ideas (owner: on hold until Noah and Pyramid are finished)
- Assassins of Alamut: script v2 ready (`assassins-alamut/script.md`, 128 words, ~58 s, includes Nizam al-Mulk 1092).
  Next step: owner approval for the voiceover (~28 vidIQ credits). Search ~45k/month, low competition.
- Machiavelli ("The end justifies the means. He never said it."): ~476k searches/month, high competition. Not written yet.
- Other researched topics: Sphinx's nose (sphinx +845%), Mary Celeste (178k, +152%), Mona Lisa theft 1911.

## Salem re-upload (2026-11-17)
- New Salem with own music is live: F_HL18etevs (title, description, tags set at upload).
- Quota ran out: tomorrow run `python3 egypt-pyramids/publish/finish.py F_HL18etevs public salem-remix/publish`
  (sets metadata again, 7 captions, posts the comment; owner pins it). Owner deletes the old Salem (5phbMr3egWo) in Studio.
- Atlantis v4 script waits for the owner's OK on the voiceover (~28 credits): `atlantis-story/v4/script.md`.
