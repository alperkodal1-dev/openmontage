"""After the video is on YouTube (Studio upload), set everything else with one command:
title, description, tags, languages, thumbnail (cover C), 7 caption tracks, and the comment to pin.
Usage: python3 finish.py <videoId> [public] [publish_dir]   (publish_dir holds metadata.json and the SRTs; default: this folder)   (auth: the same env as channel-branding/yt_upload_video.py)"""
import json, os, sys, urllib.request, uuid

def token():
    import urllib.parse
    if os.environ.get('YT_OAUTH_JSON'):
        rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
        body = urllib.parse.urlencode({'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET'],
                                       'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
        return json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', body))['access_token']
    return open(os.environ['YT_ACCESS_TOKEN_FILE']).read().strip()

def call(req, what):
    try:
        r = urllib.request.urlopen(req); print('ok  ', what); return json.load(r)
    except urllib.error.HTTPError as e:
        print('FAIL', what, e.code, e.read().decode()[:300])

vid = sys.argv[1]; privacy = sys.argv[2] if len(sys.argv) > 2 else 'public'
H = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.dirname(os.path.abspath(__file__))
tok = token(); A = {'Authorization': 'Bearer ' + tok}
m = json.load(open(f'{H}/metadata.json'))
meta = {'id': vid, 'snippet': {'title': m['title'], 'description': m['description'], 'tags': m['tags'], 'categoryId': '27',
                               'defaultLanguage': 'en', 'defaultAudioLanguage': 'en'},
        'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': False}}
call(urllib.request.Request('https://www.googleapis.com/youtube/v3/videos?part=snippet,status', json.dumps(meta).encode(),
                            {**A, 'Content-Type': 'application/json'}, method='PUT'), 'metadata')
if m.get('thumb'):
  call(urllib.request.Request(f'https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}',
                            open(os.path.join(H, m['thumb']), 'rb').read(), {**A, 'Content-Type': 'image/jpeg'}), 'thumbnail')
names = {'en': 'English', 'tr': 'Türkçe', 'es': 'Español', 'pt': 'Português', 'de': 'Deutsch', 'fr': 'Français', 'ja': '日本語'}
for lang, name in names.items():
    b = uuid.uuid4().hex
    snip = json.dumps({'snippet': {'videoId': vid, 'language': lang, 'name': name}})
    body = (f'--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{snip}\r\n--{b}\r\nContent-Type: application/octet-stream\r\n\r\n'
            ).encode() + open(os.path.join(H, m['srt'].format(lang=lang)), 'rb').read() + f'\r\n--{b}--\r\n'.encode()
    call(urllib.request.Request('https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart', body,
                                {**A, 'Content-Type': f'multipart/related; boundary={b}'}), 'caption ' + lang)
c = {'snippet': {'videoId': vid, 'topLevelComment': {'snippet': {'textOriginal': m['pinned_comment']}}}}
call(urllib.request.Request('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet', json.dumps(c).encode(),
                            {**A, 'Content-Type': 'application/json'}), 'comment (pin it in Studio)')
print('https://youtube.com/shorts/' + vid)
