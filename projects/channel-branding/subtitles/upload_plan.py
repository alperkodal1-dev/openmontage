"""Upload caption tracks for a planned day (YouTube API captions.insert, 400 units each; ~24 tracks fit in a day).
Skips tracks already on the video (captions.list, 50 units per video) and records uploads in uploaded.json.
Usage: python3 upload_plan.py day1|day2|day3   (auth: YT_OAUTH_JSON + YT_CLIENT_ID + YT_CLIENT_SECRET)"""
import json, os, sys, urllib.request, urllib.parse, uuid
P = '/home/user/openmontage/projects/'
HU = P + 'channel-branding/subtitles/hi_ur/out/'
ALL7 = ['en', 'tr', 'es', 'pt', 'de', 'fr', 'ja']
def seven(d, stem): return {l: f'{P}{d}/{stem}_{l}.srt' for l in ALL7}
AID_F = P + 'alexander-great/publish/video_id.txt'   # written after the Alexander upload succeeds
AID = open(AID_F).read().strip() if os.path.exists(AID_F) else None
PLAN = {
 'day1': ([(AID, 'Alexander', {**seven('alexander-great/publish', 'alexander'), 'hi': P + 'alexander-great/publish/alexander_hi.srt', 'ur': P + 'alexander-great/publish/alexander_ur.srt'})] if AID else []) + [
  ('x5FLR7Iwv_A', 'Noah', {**seven('noah-ark/publish_long', 'noah'), 'hi': HU + 'noah_hi.srt', 'ur': HU + 'noah_ur.srt'}),
 ],
 'day2': [
  ('5SXAmr8qgFM', 'Piri Reis', {'fr': P + 'channel-branding/subtitles/out/piri_5SXAmr8qgFM/piri_fr.srt', 'ja': P + 'channel-branding/subtitles/out/piri_5SXAmr8qgFM/piri_ja.srt', 'hi': HU + 'piri_hi.srt', 'ur': HU + 'piri_ur.srt'}),
  ('Y_Apy6CZdHI', 'Salem', {**seven('salem-remix/publish', 'salem'), 'hi': HU + 'salem_hi.srt', 'ur': HU + 'salem_ur.srt'}),
  ('5xT5DXyXcVA', 'Pyramid', {**seven('egypt-pyramids/publish', 'pyramid'), 'hi': HU + 'pyramid_hi.srt', 'ur': HU + 'pyramid_ur.srt'}),
 ],
 'day3': [
  ('d2PR8LPYXzo', 'Atlantis', {**seven('atlantis-story/v4/publish', 'atlantis'), 'hi': HU + 'atlantis_hi.srt', 'ur': HU + 'atlantis_ur.srt'}),
 ]}  # Ankara left out at the owner's request
NAMES = {'en': 'English', 'tr': 'Türkçe', 'es': 'Español', 'pt': 'Português', 'de': 'Deutsch', 'fr': 'Français', 'ja': '日本語', 'hi': 'हिन्दी', 'ur': 'اردو'}
rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
b = urllib.parse.urlencode({'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET'], 'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
A = {'Authorization': 'Bearer ' + json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', b))['access_token']}
log_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded.json'); log = json.load(open(log_p))
for vid, name, tracks in PLAN[sys.argv[1]]:
    try:
        have = {c['snippet']['language'] for c in json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={vid}', headers=A)))['items']}
    except urllib.error.HTTPError as e:
        print('FAIL list', name, e.code, e.read().decode()[:150]); continue
    for lang, path in tracks.items():
        if lang in have: print('skip', name, lang, '(already on the video)'); continue
        bd = uuid.uuid4().hex
        snip = json.dumps({'snippet': {'videoId': vid, 'language': lang, 'name': NAMES[lang]}})
        body = (f'--{bd}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{snip}\r\n--{bd}\r\nContent-Type: application/octet-stream\r\n\r\n').encode() \
            + open(path, 'rb').read() + f'\r\n--{bd}--\r\n'.encode()
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request('https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart', body,
                                                                        {**A, 'Content-Type': f'multipart/related; boundary={bd}'})))
            log[f'{vid}:{lang}'] = r['id']; json.dump(log, open(log_p, 'w'), indent=1); print('ok  ', name, lang)
        except urllib.error.HTTPError as e:
            print('FAIL', name, lang, e.code, e.read().decode()[:150])
