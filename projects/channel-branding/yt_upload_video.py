"""Upload a video file to the channel (YouTube Data API v3, videos.insert with a resumable upload; 1600 quota units).
Auth: refresh token in the JSON file given by YT_OAUTH_JSON (from the OAuth code exchange) + YT_CLIENT_ID/YT_CLIENT_SECRET,
or a short-lived access token in YT_ACCESS_TOKEN_FILE.
Usage: python3 yt_upload_video.py <file.mp4> "<title>" [unlisted|private|public] [description]"""
import json, os, sys, urllib.parse, urllib.request

def token():
    if os.environ.get('YT_OAUTH_JSON'):
        rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
        body = urllib.parse.urlencode({'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET'],
                                       'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
        return json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', body))['access_token']
    return open(os.environ['YT_ACCESS_TOKEN_FILE']).read().strip()

path, title = sys.argv[1], sys.argv[2]
privacy = sys.argv[3] if len(sys.argv) > 3 else 'unlisted'
desc = sys.argv[4] if len(sys.argv) > 4 else ''
tok = token()
meta = {'snippet': {'title': title, 'description': desc, 'categoryId': '27'},
        'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False}}
size = os.path.getsize(path)
req = urllib.request.Request('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status',
                             json.dumps(meta).encode(), {'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json; charset=UTF-8',
                                                         'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(size)})
try:
    loc = urllib.request.urlopen(req).headers['Location']
except urllib.error.HTTPError as e:
    sys.exit(f'init failed: {e.code} {e.read().decode()[:600]}')
up = urllib.request.Request(loc, open(path, 'rb').read(), {'Authorization': 'Bearer ' + tok, 'Content-Type': 'video/mp4'}, method='PUT')
r = json.load(urllib.request.urlopen(up))
print(r['id'], r['status']['privacyStatus'], 'https://youtube.com/shorts/' + r['id'])
