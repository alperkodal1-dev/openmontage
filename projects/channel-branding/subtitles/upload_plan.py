"""Upload caption tracks for a planned day (YouTube API captions.insert, 400 units each; ~24 tracks fit in a day).
Skips tracks already on the video (captions.list, 50 units per video) and records uploads in uploaded.json.
Usage: python3 upload_plan.py day1|day2|day3   (auth: YT_OAUTH_JSON + YT_CLIENT_ID + YT_CLIENT_SECRET)"""
import json, os, sys, urllib.request, urllib.parse, uuid
P = '/home/user/openmontage/projects/'
HU = P + 'channel-branding/subtitles/hi_ur/out/'
ALL7 = ['en', 'tr', 'es', 'pt', 'de', 'fr', 'ja']
def seven(d, stem): return {l: f'{P}{d}/{stem}_{l}.srt' for l in ALL7}
PIRI = {'fr': P + 'channel-branding/subtitles/out/piri_5SXAmr8qgFM/piri_fr.srt', 'ja': P + 'channel-branding/subtitles/out/piri_5SXAmr8qgFM/piri_ja.srt', 'hi': HU + 'piri_hi.srt', 'ur': HU + 'piri_ur.srt'}
V = {
 'economist': ('3lRSiGfhOw0', 'Economist 2027', {l: P + f'economist-2027/publish/economist_{l}.srt' for l in ALL7 + ['hi', 'ur', 'ru']}),
 'alexander': ('4G-MdMl5PGg', 'Alexander', {**seven('alexander-great/publish', 'alexander'), 'hi': P + 'alexander-great/publish/alexander_hi.srt', 'ur': P + 'alexander-great/publish/alexander_ur.srt'}),
 'piri': ('5SXAmr8qgFM', 'Piri Reis', PIRI),
 'noah': ('x5FLR7Iwv_A', 'Noah', {**seven('noah-ark/publish_long', 'noah'), 'hi': HU + 'noah_hi.srt', 'ur': HU + 'noah_ur.srt'}),
 'salem': ('Y_Apy6CZdHI', 'Salem', {**seven('salem-remix/publish', 'salem'), 'hi': HU + 'salem_hi.srt', 'ur': HU + 'salem_ur.srt'}),
 'pyramid': ('5xT5DXyXcVA', 'Pyramid', {**seven('egypt-pyramids/publish', 'pyramid'), 'hi': HU + 'pyramid_hi.srt', 'ur': HU + 'pyramid_ur.srt'}),
 'atlantis': ('d2PR8LPYXzo', 'Atlantis', {**seven('atlantis-story/v4/publish', 'atlantis'), 'hi': HU + 'atlantis_hi.srt', 'ur': HU + 'atlantis_ur.srt'}),
}
# Owner (17 Nov): this week's only job is captions on every Short on the channel. ~24 tracks fit in a day's quota.
PLAN = {'day1': [V['economist'], V['piri'], V['noah']],   # 10 + 4 + 9 = 23 tracks (Economist first: it is trending)
        'day2': [V['salem'], V['pyramid']],                  # 9 + 9 = 18 tracks
        'day3': [V['atlantis'], V['alexander']] + list(V.values()),   # Atlantis 9 + Alexander 9 = 18, then re-check all
        'en_fix': [(V['economist'][0], 'Economist 2027', {'en': V['economist'][2]['en']}), (V['noah'][0], 'Noah', {'en': V['noah'][2]['en']})]}   # Atlantis (9) + retry anything missing on every Short
# Owner (18 Nov): Arabic, Pashto, Dari/Persian on every Short (21 tracks; ~8,400 units)
NEW3 = lambda key, stem: (V[key][0], V[key][1], {l: HU + f'{stem}_{l}.srt' for l in ('ar', 'ps', 'fa')})
PLAN['arpsfa'] = [NEW3(k, k) for k in ('atlantis', 'salem', 'pyramid', 'noah', 'piri', 'alexander', 'economist')]
# Ankara (long video) left out at the owner's request
NAMES = {'ar': 'العربية', 'ps': 'پښتو', 'fa': 'فارسی (دری)', 'ru': 'Русский', 'en': 'English', 'tr': 'Türkçe', 'es': 'Español', 'pt': 'Português', 'de': 'Deutsch', 'fr': 'Français', 'ja': '日本語', 'hi': 'हिन्दी', 'ur': 'اردو'}
if os.environ.get('YT_ACCESS_TOKEN'):   # short-lived token (e.g. from OAuth Playground) instead of a refresh token
    A = {'Authorization': 'Bearer ' + os.environ['YT_ACCESS_TOKEN']}
else:
  rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
  b = urllib.parse.urlencode({**({} if os.environ.get('YT_CLIENT_SECRET', '') in ('', 'proxy-injected') else {'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET']}), 'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
  A = {'Authorization': 'Bearer ' + json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', b))['access_token']}
log_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded.json'); log = json.load(open(log_p))
for vid, name, tracks in PLAN[sys.argv[1]]:
    try:
        have = {c['snippet']['language'] for c in json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={vid}', headers=A)))['items'] if c['snippet'].get('trackKind') != 'asr'}   # YouTube's auto captions do not count
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
