from bs4 import BeautifulSoup
import urllib3
import time
import re


def get_page(pool, url, pages=None):
  base_url = 'https://minecraft.gamepedia.com'
  print('Working on: '+url)
  if pages is None:
    pages = []
  
  r = pool.request('GET', url, preload_content=False)
  res = BeautifulSoup(r.read(), 'html.parser')
  r.release_conn()
  time.sleep(2)
  pages.extend([base_url+x.find('a')['href'] for x in res.find(id = "mw-content-text").find_all('li')])
  try:
    next_page = [x['href'] for x in res.find('div', {'class': 'mw-allpages-nav'}).find_all('a') if re.search('Next page', x.text)][0]
  except IndexError:
    return(pages)
  
  return get_page(pool, base_url+next_page, pages = pages)


if __name__ == 'main':
  http = urllib3.PoolManager()
  first_page = 'https://minecraft.gamepedia.com/index.php?title=Special:AllPages&hideredirects=1'
  all_pages = get_page(http, first_page)
  with open('minecraft_links.txt', 'w') as f:
    for item in all_pages:
      f.write("%s\n" % item)
