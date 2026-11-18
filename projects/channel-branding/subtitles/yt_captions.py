"""Upload the SRT files in out/ to YouTube as caption tracks (YouTube Data API v3, captions.insert, 400 quota units each).
Auth: YT_CLIENT_ID + YT_CLIENT_SECRET + YT_REFRESH_TOKEN (environment variables; a fresh access token is fetched),
or YT_ACCESS_TOKEN_FILE pointing at a file holding a short-lived access token.
Usage: python3 yt_captions.py [--dry-run] [--limit N] [video ...]     (videos: piri noah atlantis salem ankara)
Already uploaded tracks are recorded in uploaded.json and skipped."""
import json, os, sys, urllib.parse, urllib.request, uuid
VIDEOS = {'piri': '5SXAmr8qgFM', 'noah': '68mjjXGN5EI', 'atlantis': '_PpRv_GMMlk', 'salem': '5phbMr3egWo', 'ankara': 'MP9oLB-ND9A'}
LANGS = ['en', 'tr', 'es', 'pt', 'de', 'fr', 'ja']
DONE = 'uploaded.json'

def token():
    if os.environ.get('YT_REFRESH_TOKEN'):
        body = urllib.parse.urlencode({**({} if os.environ.get('YT_CLIENT_SECRET', '') in ('', 'proxy-injected') else {'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET']}),
                                       'refresh_token': os.environ['YT_REFRESH_TOKEN'], 'grant_type': 'refresh_token'}).encode()
        return json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', body))['access_token']
    return open(os.environ['YT_ACCESS_TOKEN_FILE']).read().strip()

def insert(tok, vid, lang, path):
    meta = json.dumps({'snippet': {'videoId': vid, 'language': lang, 'name': '', 'isDraft': False}}).encode()
    b = uuid.uuid4().hex
    body = (f'--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode() + meta +
            f'\r\n--{b}\r\nContent-Type: application/octet-stream\r\n\r\n'.encode() + open(path, 'rb').read() + f'\r\n--{b}--\r\n'.encode())
    req = urllib.request.Request('https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart', body,
                                 {'Authorization': 'Bearer ' + tok, 'Content-Type': f'multipart/related; boundary={b}'})
    try:
        return json.load(urllib.request.urlopen(req))['id'], None
    except urllib.error.HTTPError as e:
        return None, f'{e.code} {e.read().decode()[:300]}'

args = sys.argv[1:]; dry = '--dry-run' in args
limit = int(args[args.index('--limit') + 1]) if '--limit' in args else 25
names = [a for a in args if a in VIDEOS] or list(VIDEOS)
done = json.load(open(DONE)) if os.path.exists(DONE) else {}
tok = None if dry else token()
n = 0
# language by language across the videos, so every Short gets English, Turkish, Spanish... before the next language
for lang, name in [(l, v) for l in LANGS for v in names]:
    vid = VIDEOS[name]
    if True:
        key = f'{vid}:{lang}'
        if key in done: continue
        if n >= limit: print('limit reached'); break
        path = f'out/{name}_{vid}/{name}_{lang}.srt'
        if dry: print('would upload', key, path); n += 1; continue
        cid, err = insert(tok, vid, lang, path)
        if err:
            print('FAIL', key, err)
            if 'quota' in err.lower(): sys.exit(1)
            continue
        done[key] = cid; json.dump(done, open(DONE, 'w'), indent=1); n += 1
        print('ok', key, cid)
print(n, 'uploaded' if not dry else 'planned')
