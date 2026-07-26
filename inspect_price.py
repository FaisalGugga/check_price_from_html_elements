import re
import requests
from dotenv import dotenv_values

cfg = dotenv_values('.env')
url = cfg['URL_PAGE']
html = requests.get(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.amazon.sa/'
    },
    timeout=25,
).text

for term in ['price', 'offer', 'amount', 'currency', 'buybox', 'buy-now', 'deals', 'savings', 'priceAmount', 'displayPrice']:
    idx = html.lower().find(term.lower())
    if idx != -1:
        print('TERM', term, 'IDX', idx)
        print(html[max(0, idx-400):idx+2200])
        print('---')

for m in re.finditer(r'\d{2,6}(?:[.,]\d{2})?', html):
    print('NUM', m.group(0))
    break
