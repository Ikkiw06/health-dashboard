import urllib.request, urllib.error, json, base64, os

TOKEN = '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'
OWNER = 'Ikkiw06'
REPO  = 'health-dashboard'
FILE  = 'index.html'

script_dir = os.path.dirname(os.path.abspath(__file__))
html_path  = os.path.join(script_dir, 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_b64 = base64.b64encode(content.encode('utf-8')).decode()

headers = {
    'Authorization': f'token {TOKEN}',
    'User-Agent': 'dashboard-deploy',
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.github+json'
}

api_url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE}'

print('Getting current file SHA...')
req = urllib.request.Request(api_url, headers=headers)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        sha = data['sha']
        print(f'SHA: {sha}')
except urllib.error.HTTPError as e:
    sha = None
    print(f'No existing file: {e}')

print('Pushing...')
payload = json.dumps({
    'message': 'Fix Top 5: embed real employee names (บุญเที่ยง, เอกรินทร์, etc.)',
    'content': content_b64,
    **(({'sha': sha}) if sha else {})
}).encode('utf-8')

req2 = urllib.request.Request(api_url, data=payload, headers=headers, method='PUT')
try:
    with urllib.request.urlopen(req2) as r:
        result = json.loads(r.read())
        commit_url = result.get('commit', {}).get('html_url', '')
        print(f'\n✅ DONE! Vercel will deploy in ~30s.')
        print(f'Commit: {commit_url}')
except urllib.error.HTTPError as e:
    print(f'ERROR: {e.read().decode()}')

input('\nPress Enter to close...')
