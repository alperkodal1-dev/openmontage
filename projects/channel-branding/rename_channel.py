"""After the channel is renamed in Studio: swap "Unsealed History" for the new name in every video's description and tags,
and set the channel description and keywords from channel_settings_en.md. ~50 quota units per video + 50 for the channel.
Auth: YT_OAUTH_JSON + YT_CLIENT_ID + YT_CLIENT_SECRET (as yt_upload_video.py)."""
import json, os, re, urllib.request, urllib.parse
NEW = 'Or So The Story Goes'
rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
b = urllib.parse.urlencode({**({} if os.environ.get('YT_CLIENT_SECRET', '') in ('', 'proxy-injected') else {'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET']}), 'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
A = {'Authorization': 'Bearer ' + json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', b))['access_token']}
g = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers=A)))
def put(u, body, what):
    try: urllib.request.urlopen(urllib.request.Request(u, json.dumps(body).encode(), {**A, 'Content-Type': 'application/json'}, method='PUT')); print('ok  ', what)
    except urllib.error.HTTPError as e: print('FAIL', what, e.code, e.read().decode()[:200])
ch = g('https://www.googleapis.com/youtube/v3/channels?part=contentDetails,brandingSettings&mine=true')['items'][0]
up = ch['contentDetails']['relatedPlaylists']['uploads']
ids, tok = [], ''
while True:
    r = g(f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={up}' + (f'&pageToken={tok}' if tok else ''))
    ids += [i['snippet']['resourceId']['videoId'] for i in r['items']]; tok = r.get('nextPageToken')
    if not tok: break
for k in range(0, len(ids), 50):
    for v in g('https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + ','.join(ids[k:k+50]))['items']:
        sn = v['snippet']; d = sn.get('description', ''); t = sn.get('tags', [])
        nd = d.replace('Unsealed History', NEW); nt = [NEW.lower() if x.lower() == 'unsealed history' else x for x in t]
        if nd == d and nt == t: continue
        body = {'id': v['id'], 'snippet': {k2: sn[k2] for k2 in ('title', 'categoryId') if k2 in sn}}
        body['snippet'].update(description=nd, tags=nt)
        for k2 in ('defaultLanguage', 'defaultAudioLanguage'):
            if k2 in sn: body['snippet'][k2] = sn[k2]
        put('https://www.googleapis.com/youtube/v3/videos?part=snippet', body, 'video ' + v['id'])
s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'channel_settings_en.md')).read()
desc = s.split('## Channel description')[1].split('## Channel keywords')[0].strip()
desc = '\n'.join(l for l in desc.splitlines() if not l.startswith('Business inquiries')).strip()
kw = s.split('## Channel keywords')[1].split('\n\n')[1].strip()
bs = ch['brandingSettings']; bs.setdefault('channel', {})
bs['channel']['description'] = desc
bs['channel']['keywords'] = ' '.join(f'"{x.strip()}"' if ' ' in x.strip() else x.strip() for x in kw.split(','))
put('https://www.googleapis.com/youtube/v3/channels?part=brandingSettings', {'id': ch['id'], 'brandingSettings': bs}, 'channel description + keywords')
