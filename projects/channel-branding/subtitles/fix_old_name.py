"""Replace the old channel name in descriptions: 'Subscribe to Unsealed History' -> 'Subscribe to Or So The Story Goes'.
Only that phrase changes; title/tags/category/languages are re-sent unchanged. Usage: python3 fix_old_name.py VIDEO_ID [...]
Auth: /root/.yt_access_token (temporary token)."""
import json, sys, time, urllib.request, urllib.error
T = open('/root/.yt_access_token').read().strip()
A = {'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json'}
API = 'https://www.googleapis.com/youtube/v3/videos'
def call(url, body=None, method='GET'):
    for i in range(40):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, json.dumps(body).encode() if body else None, A, method=method)))
        except urllib.error.HTTPError as e:
            m = e.read().decode()
            if e.code == 403 and 'quota' in m: time.sleep(6); continue
            raise SystemExit(f'FAIL {e.code} {m[:200]}')
    raise SystemExit('FAIL quota')
for vid in sys.argv[1:]:
    sn = call(f'{API}?part=snippet&id={vid}')['items'][0]['snippet']
    if 'Unsealed History' not in sn['description']: print('ok  ', vid, 'old name not in description'); continue
    s = {k: sn[k] for k in ('title', 'description', 'tags', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage') if k in sn}
    s['description'] = sn['description'].replace('Subscribe to Unsealed History', 'Subscribe to Or So The Story Goes')
    if 'Unsealed History' in s['description']: print('NOTE', vid, 'old name also appears elsewhere; left as is')
    r = call(f'{API}?part=snippet', {'id': vid, 'snippet': s}, 'PUT')['snippet']
    assert r['title'] == sn['title'] and r.get('tags') == sn.get('tags')
    print('ok  ', vid, 'description updated')
