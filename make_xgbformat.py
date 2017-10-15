import json
import MeCab
import pickle
import os
import sys
import math
from collections import Counter
if '--make_data' in sys.argv:
  m = MeCab.Tagger('-Owakati')
  data = []
  with open('reveiws.json') as f:
    for en, line in enumerate(f):
      line = line.strip()
      obj = json.loads(line)
      if en%1000 == 0:
        print(en, obj)
      stars = obj['stars']
      title = obj['title']
      review = obj['review']
      terms = m.parse(review).strip().split() + m.parse(title).strip().split()
      data.append( ( stars, terms ) )

  open('data.pkl', 'wb').write( pickle.dumps(data) )

if '--make_index' in sys.argv:
  data = pickle.loads( open('data.pkl', 'rb').read() ) 
  termset = set()
  for pair in data:
    star, terms = pair 
    [ termset.add(term) for term in terms ]

  term_index = {}
  for en, term in enumerate(list(termset)):
    term_index[term] = en
  open('term_index.pkl','wb').write( pickle.dumps(term_index) )

if '--make_xgb' in sys.argv:
  term_index = pickle.loads( open('term_index.pkl', 'rb').read() ) 
  #index_term = { index:term for term, index in term_index.items() }
  data = pickle.loads( open('data.pkl', 'rb').read() ) 
  f = open('xgb_format','w')
  for pair in data:
    star, terms = pair
    if star is None:
      continue
    tf = dict( Counter(terms) )
    ctext = ' '.join( ["%s:%0.5f"%(term_index[t], math.log(f+1)) for t, f in tf.items()] )
    fla = '%0.2f %s'%(float(star), ctext) 
    f.write( fla +'\n' )




  
