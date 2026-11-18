"""Set English default language + localized titles/descriptions (localizations.json) on the published Economist Short.
videos.update part=snippet,localizations (50 units). Auth: YT_OAUTH_JSON + YT_CLIENT_ID + YT_CLIENT_SECRET."""
import json, os, urllib.request, urllib.parse
H = os.path.dirname(os.path.abspath(__file__))
VID = open(os.path.join(H, 'video_id.txt')).read().strip()
m = json.load(open(os.path.join(H, 'metadata.json'))); loc = json.load(open(os.path.join(H, 'localizations.json')))
rt = json.load(open(os.environ['YT_OAUTH_JSON']))['refresh_token']
b = urllib.parse.urlencode({'client_id': os.environ['YT_CLIENT_ID'], 'client_secret': os.environ['YT_CLIENT_SECRET'], 'refresh_token': rt, 'grant_type': 'refresh_token'}).encode()
A = {'Authorization': 'Bearer ' + json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', b))['access_token'], 'Content-Type': 'application/json'}
cur = json.load(urllib.request.urlopen(urllib.request.Request(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VID}', headers=A)))['items'][0]['snippet']
# keep whatever the owner set in Studio (category was changed to News & Politics on 18 Nov)
body = {'id': VID, 'snippet': {'title': cur['title'], 'description': cur.get('description', m['description']), 'tags': cur.get('tags', m['tags']), 'categoryId': cur['categoryId'],
        'defaultLanguage': 'en', 'defaultAudioLanguage': 'en'}, 'localizations': loc}
r = json.load(urllib.request.urlopen(urllib.request.Request('https://www.googleapis.com/youtube/v3/videos?part=snippet,localizations', json.dumps(body).encode(), A, method='PUT')))
print('localized:', sorted(r.get('localizations', {})))
