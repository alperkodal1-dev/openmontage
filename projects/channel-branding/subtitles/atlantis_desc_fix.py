import json, time, urllib.request, urllib.error
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
vid = 'd2PR8LPYXzo'
sn = call(f'{API}?part=snippet&id={vid}')['items'][0]['snippet']
old, new = 'Atlantis sank beneath the sea... but did it?', 'Atlantis sank beneath the sea... but was it ever there?'
if old not in sn['description']: raise SystemExit('first line not found: ' + sn['description'][:80])
s = {k: sn[k] for k in ('title', 'description', 'tags', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage') if k in sn}
s['description'] = sn['description'].replace(old, new, 1)
r = call(f'{API}?part=snippet', {'id': vid, 'snippet': s}, 'PUT')['snippet']
assert r['title'] == sn['title'] and r.get('tags') == sn.get('tags')
print('ok:', r['description'][:110])
