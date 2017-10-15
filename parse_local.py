import bs4
from bs4 import BeautifulSoup 

import glob
import re
import json

for en, name in enumerate(glob.glob('htmls/*')):
  if not re.search(r'review', name):
    continue
  print(en,'/', name )
  soup = BeautifulSoup(open(name).read() )

  title = soup.find_all('h2')[0].text 
  for review in soup.find_all('div', {'class': 'review'} ):
    struct = {'title':'', 'reviewTitle':'', 'review':'', 'stars':0}
    struct['title'] = title
    try:
      struct['reviewTitle'] = review.find('h3').text 
    except AttributeError as e:
      continue
    struct['review'] = review.find('p').text 
    try:
      struct['stars'] = float( review.find('strong').text )
    except:
      struct['stars'] = None
    with open('reveiws.json', 'a') as w:
      dump = json.dumps(struct, ensure_ascii=False)
      w.write( dump + '\n' )
    print( dump )
