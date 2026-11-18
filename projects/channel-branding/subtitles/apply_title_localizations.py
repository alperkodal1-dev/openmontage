"""Add localized titles (title_localizations.json) to the channel's Shorts. Add only: existing localizations are kept,
title/description/tags/category stay as they are live. Each localization gets the live English description.
Applies a video's set only if its live title matches a key in the JSON. ~51 quota units per video.
Usage: python3 apply_title_localizations.py [--dry]
Auth: YT_ACCESS_TOKEN, or YT_OAUTH_JSON (+ YT_CLIENT_ID/YT_CLIENT_SECRET, or proxy-injected client auth)."""
import json, os, sys, urllib.request, urllib.parse
H = os.path.dirname(os.path.abspath(__file__))
DRY = '--dry' in sys.argv
if os.environ.get('YT_ACCESS_TOKEN'):
    tok = os.environ['YT_ACCESS_TOKEN']
else:
    rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
    sec = os.environ.get('YT_CLIENT_SECRET', '')
    b = urllib.parse.urlencode({**({} if sec in ('', 'proxy-injected') else {'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': sec}),
                                'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
    tok = json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', b))['access_token']
A = {'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'}
API = 'https://www.googleapis.com/youtube/v3/videos'
plan = json.load(open(os.path.join(H, 'title_localizations.json')))['videos']
for vid, sets in plan.items():
    try:
        it = json.load(urllib.request.urlopen(urllib.request.Request(f'{API}?part=snippet,localizations&id={vid}', headers=A)))['items'][0]
    except urllib.error.HTTPError as e:
        print('FAIL get', vid, e.code, e.read().decode()[:150]); continue
    sn, have = it['snippet'], it.get('localizations', {})
    tr = sets.get(sn['title'])
    if not tr:
        print('SKIP', vid, 'live title not in plan:', sn['title']); continue
    dl = sn.get('defaultLanguage')
    loc = dict(have)
    for lang, title in tr.items():
        if lang in loc or lang == (dl or 'en'): continue
        loc[lang] = {'title': title[:100], 'description': sn.get('description', '')}
    new = sorted(set(loc) - set(have))
    if not new:
        print('ok  ', vid, 'nothing to add'); continue
    if dl:
        part, body = 'localizations', {'id': vid, 'localizations': loc}
    else:   # localizations need a default language; re-send the live snippet unchanged plus defaultLanguage
        s = {k: sn[k] for k in ('title', 'description', 'tags', 'categoryId', 'defaultAudioLanguage') if k in sn}
        s['defaultLanguage'] = 'en'
        part, body = 'snippet,localizations', {'id': vid, 'snippet': s, 'localizations': loc}
    if DRY:
        print('DRY ', vid, sn['title'][:50], '| part', part, '| add', new); continue
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'{API}?part={part}', json.dumps(body).encode(), A, method='PUT')))
        rs = r['snippet'] if 'snippet' in r else None
        if rs and (rs['title'] != sn['title'] or rs.get('tags') != sn.get('tags')):
            print('WARN', vid, 'snippet changed unexpectedly')
        print('ok  ', vid, 'added', new)
    except urllib.error.HTTPError as e:
        print('FAIL', vid, e.code, e.read().decode()[:200])
