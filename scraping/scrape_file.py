from bs4 import BeautifulSoup
import urllib3
import time
import re
from tqdm import tqdm
import json
import os

if not os.path.isdir('pages'):
    os.mkdir('pages')


def ner_extractor(text, ner):
    return [x for x in ner if re.search(x, text, re.IGNORECASE)]


def get_page(pool, url, ner):
  r = pool.request('GET', url, preload_content=False)
  res = BeautifulSoup(r.read(), 'html.parser')
  r.release_conn()
  time.sleep(1)
  body = res.find(id='mw-content-text')
  ps = [BeautifulSoup(x, 'html.parser').text for x in str(body).split('<h2>')]
  ps = [re.sub('\[.*?\]', '', x) for x in ps]
  title = res.find(id='firstHeading').text
  if not re.search('/', title):
    for i, p in enumerate(ps):
      ners = ner_extractor(p, ner).append(title)
      output = {
          'p': p,
          'ner': ners,
          'url': url
      }
      with open('pages/'+title+'_'+str(i)+'.json', 'w') as f:
        json.dump(output, f)


with open('scraping/ner.json') as j:
  full_ner = json.load(j)

with open('scraping/minecraft_links.txt') as l:
  links = l.read().split('\n')

http = urllib3.PoolManager()
for link in tqdm(links):
  get_page(http, link, full_ner)   
