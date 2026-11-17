"""Upload the caption tracks that hit the daily quota on the first run (AuveB2unXDM)."""
import json, os, sys, urllib.request, urllib.parse, uuid
H = os.path.dirname(os.path.abspath(__file__)); vid = 'AuveB2unXDM'
LANGS = sys.argv[1:] or ['tr', 'es', 'de', 'fr', 'ja']
names = {'tr': 'Türkçe', 'es': 'Español', 'de': 'Deutsch', 'fr': 'Français', 'ja': '日本語', 'en': 'English', 'pt': 'Português'}
rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
b = urllib.parse.urlencode({'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET'], 'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
tok = json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', b))['access_token']
for lang in LANGS:
    bd = uuid.uuid4().hex
    snip = json.dumps({'snippet': {'videoId': vid, 'language': lang, 'name': names[lang]}})
    body = (f'--{bd}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{snip}\r\n--{bd}\r\nContent-Type: application/octet-stream\r\n\r\n').encode() \
        + open(f'{H}/noah_{lang}.srt', 'rb').read() + f'\r\n--{bd}--\r\n'.encode()
    try:
        urllib.request.urlopen(urllib.request.Request('https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart', body,
                               {'Authorization': 'Bearer ' + tok, 'Content-Type': f'multipart/related; boundary={bd}'})); print('ok', lang)
    except urllib.error.HTTPError as e:
        print('FAIL', lang, e.code, e.read().decode()[:120])
