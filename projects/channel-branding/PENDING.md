# Handoff — Or So The Story Goes (state on 18 Nov 2026, ~12:20 Istanbul)

Branch: claude/history-shorts-design-9f809x. Read SIGNATURES.md first. All conversation with the owner in Turkish; videos in English.
Standing owner rules: ask before spending credits (vidIQ / ElevenLabs) and before publishing; never delete + re-upload a PUBLISHED video; one Short a day at 20:00 Istanbul (17:00 UTC); no reused third-party audio/footage (Content ID risk); only add tags, do not remove existing ones.

## Channel videos
| Video | ID | State |
|---|---|---|
| Economist 2027 cover | 3lRSiGfhOw0 | public 18 Nov; captions 10 langs; localized titles 9 langs; thumb "2027 WARNING?" (no ring); category News & Politics (set by owner) |
| Alexander (v3, infinite worlds) | 4G-MdMl5PGg | scheduled 18 Nov 17:00 UTC; thumb cover_g (WHY HE WEPT, vidIQ 92); title vidIQ 98; tag "ancient people" added |
| Piri Reis | 5SXAmr8qgFM | public; captions 9 langs |
| Noah | x5FLR7Iwv_A | public; captions 9 langs; "ancient people" tag pending (trigger 19 Nov 11:40) |
| Salem | Y_Apy6CZdHI | public; captions pending (19 Nov 11:05) |
| Pyramid | 5xT5DXyXcVA | public; captions pending (19 Nov 11:05); "ancient people" added, which pushed out "who built the pyramids" — owner to decide |
| Atlantis | d2PR8LPYXzo | public; captions pending (20 Nov 11:05); "ancient people" added |
| Ankara (long) | MP9oLB-ND9A | public; 4 caption langs; left out of caption plan by owner |
Leftover non-public copies the owner may delete in Studio: yp6RSu-8kl0 (old Alexander, unlisted), z15OEpavQ5I (Economist review copy, unlisted).

## Scheduled tasks (this old session)
- 19 Nov 11:05 TR: captions day2 (Salem, Pyramid) — subtitles/upload_plan.py day2
- 19 Nov 11:40 TR: add "ancient people" to Noah (add only)
- 20 Nov 11:05 TR: captions day3 (Atlantis, Alexander 4G-MdMl5PGg, then re-check all)
These fire into the OLD session. If the new session should run them instead, recreate them there.

## Credits
vidIQ ~11 left (voiceover 28, thumbnail 22, watch 10). ElevenLabs 6 left. YouTube API quota 10k/day, resets 11:00 TR (captions 400 each).

## Ideas queue
- "Scientists said the world would end on Friday 13 Nov 2026" (von Foerster 1960, Science) — recommended next.
- Baba Vanga 2027 predictions; Simpsons Nov 17 blackout (no Simpsons footage).
- Assassins (script ready: assassins-alamut/script.md), Machiavelli, Mona Lisa 1911, Mary Celeste, Sphinx.
- Cancelled: cab comedy (projects/cab-comedy); "What Did Ancient Humans Actually Do All Day?" (projects/ancient-day, script only, 18 Nov).
- OWNER RULE (18 Nov): spend nothing new. All remaining vidIQ / ElevenLabs / API usage is for caption uploads (or something urgent) only.
## Lessons (vidIQ + jury)
Shorts that win: 20-40 s, hook in first 1-2 s, snap zooms, karaoke captions, trending topic, comment-bait ending that loops. vidIQ can only watch PUBLIC videos via vidiq_video_watch (long-form tool works on unlisted). Thumbnails with a big human face score 90+.

## 18 Nov afternoon (new session)
- Salem 9/9 captions, Pyramid 8/9 (ur missing). Salem + Atlantis titles now end with hashtags (owner approved).
- OWNER PRIORITY: localized titles (tr es pt de fr ja hi ur) on Alexander, Piri, Noah, Salem, Pyramid, Atlantis: subtitles/title_localizations.json + apply_title_localizations.py (add only). Not applied yet (quota).
- Piri Reis: add tag "or so the story goes" (approved, failed on quota) -> 19 Nov 11:40 task.
- Auth: no refresh token yet (client 253977889197 seems gone: 'Client missing a project id'). Owner sends temporary OAuth Playground tokens; they use Playground's shared quota (busy; resets 11:00 TR). Long-term fix: owner creates own Google Cloud project.
