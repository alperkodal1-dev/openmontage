"""Download public-domain images from Wikimedia Commons with backoff (the shared IP gets 429s).
Usage: python3 tools/fetch_commons.py search "query" | get "File:Name.jpg" out.jpg [width]"""
import json, sys, time, urllib.parse, urllib.request
UA = {'User-Agent': 'OpenMontageHistoryShorts/1.0 (educational history video)'}
def fetch(url, tries=10):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            ra = e.headers.get('Retry-After')
            time.sleep(int(ra) + 2 if ra and ra.isdigit() else 10 * (i + 1))
    raise SystemExit('still rate limited: ' + url)
API = 'https://commons.wikimedia.org/w/api.php?format=json&action=query&'
if sys.argv[1] == 'search':
    d = json.loads(fetch(API + 'list=search&srnamespace=6&srlimit=8&srsearch=' + urllib.parse.quote(sys.argv[2])))
    for x in d['query']['search']: print(x['title'])
else:
    title, out = sys.argv[2], sys.argv[3]; w = sys.argv[4] if len(sys.argv) > 4 else '2000'
    d = json.loads(fetch(API + f'prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth={w}&titles=' + urllib.parse.quote(title)))
    p = next(iter(d['query']['pages'].values()))
    if 'imageinfo' not in p: raise SystemExit('missing: ' + title)
    ii = p['imageinfo'][0]; md = ii['extmetadata']
    data = fetch(ii.get('thumburl') or ii['url'])
    open(out, 'wb').write(data)   # write only after a full download, so a 429 leaves no empty file
    print(out, ii['width'], ii['height'], md.get('LicenseShortName', {}).get('value'), '|', md.get('Artist', {}).get('value', '')[:80])
