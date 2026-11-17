# Subtitles for the Unsealed History videos

`python3 build_srt.py` writes `out/<video>_<videoId>/<video>_<lang>.srt` for English, Spanish, Portuguese, German,
French and Japanese (Turkish SRTs already live in each project's `out/`). Texts and times are in `data_*.py`.

| Video | ID | Timing source |
|---|---|---|
| Piri Reis | 5SXAmr8qgFM | narration word timings (exact) |
| Noah's Ark | 68mjjXGN5EI | narration word timings (exact) |
| Atlantis | _PpRv_GMMlk | whisper on the final video (exact) |
| Salem | 5phbMr3egWo | vidIQ transcript blocks, spread by sentence length (about ±1 s) |
| Battle of Ankara | MP9oLB-ND9A | vidIQ transcript blocks, spread by sentence length (about ±1-2 s) |

## Uploading (YouTube Studio)
1. Studio > Subtitles > pick the video > Add language > choose the language.
2. Subtitles: Add > Upload file > With timing > pick the matching `.srt`. Publish.
3. Salem and Ankara, English: upload `*_en_transcript.txt` with "Without timing"; YouTube syncs it to the voice.
   After that, open each translated language and use "Edit timings" if a line drifts.
4. Also add the translated title and description (Studio > Subtitles > Title & description) for the same languages.
