import bs4
import sys
import urllib.request, urllib.error, urllib.parse
import http.client
from socket import error as SocketError
import ssl
import os.path
import argparse
import multiprocessing as mp
import datetime
import pickle as pickle
import re
import json
import random
import signal
import concurrent.futures
import time
from multiprocessing import Process
import http.cookiejar, random
import re
import shutil

SEED_EXIST          = True
SEED_NO_EXIST       = False
# set default state to scrape web pages in Amazon Kindle
def get_html(url, phost):
  html = None
  for _ in range(10) :
    headers = {"Accept-Language": "en-US,en;q=0.5","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Referer": "http://thewebsite.com","Connection": "keep-alive" } 
    request = urllib.request.Request(url=url, headers=headers)
    proxy = urllib.request.ProxyHandler({'http': phost})
    opener = urllib.request.build_opener( proxy )
    TIME_OUT = 5.
    try:
      html = opener.open(request, timeout = TIME_OUT).read()
    except Exception as e:
      print(e)
      continue
    break
  if html == None:
    return (None, None, None)

  soup = bs4.BeautifulSoup(html, "html.parser")
  title = (lambda x:str(x.string) if x != None else 'Untitled')(soup.title )
  return (html, title, soup)

def analyzing(soup):

  internal_links = []
  for link in soup.find_all('a'):
    url = link.get('href')
    if url is None:
      continue
    if len(url) >= 1 and ( 'http://eiga.com' in url or url[0] == '/' ):
      url = 'http://eiga.com' + url if url[0] == '/' else url
      internal_links.append( url )
  return internal_links

def _map(arr):
  link, phost = arr
  ents = link.split('/')
  ents.pop(0)
  ents.pop(0)
  save_name = '_'.join( ents )
  print( save_name )
  if os.path.exists("htmls/" + save_name) and random.random() < 0.2:
    return []
  html, title, soup = get_html(link, phost)
  time.sleep(1)
  if soup is None:
    return []

  try:
    open('htmls/{}'.format(save_name), 'w').write( html.decode('utf8') )
  except OSError as e:
    return []
  except UnicodeDecodeError as e:
    return []
  internal_links = analyzing(soup)

  return internal_links

import concurrent.futures 
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
  parser.add_argument('--URL', help='set default URL which to scrape at first')
  parser.add_argument('--depth', help='how number of url this program will scrape')
  parser.add_argument('--mode', help='you can specify mode...')
  parser.add_argument('--refresh', help='create snapshot(true|false)')
  parser.add_argument('--file', help='input filespath')
  parser.add_argument('--active', help='spcific active thread number')
  parser.add_argument('--proxy', help='you can specify mode...')

  args_obj = vars(parser.parse_args())
  depth    = (lambda x:int(x) if x else 300)( args_obj.get('depth') )
  mode     = (lambda x:x if x else 'undefined')( args_obj.get('mode') )
  refresh  = (lambda x:False if x=='false' else True)( args_obj.get('refresh') )
  active   = (lambda x:15 if x==None else int(x) )( args_obj.get('active') )
  proxy = (lambda x:x if x else 'undefined')( args_obj.get('proxy') )
  phosts = ['http://{proxy}:{proxy}awr003@{phost}:8086'.format(proxy=proxy, phost=phost.strip()) for phost in open('proxys.txt')] 

  filename = args_obj.get('file')

  seed = "http://eiga.com/movie/85936/review/" 
  link_status = {seed: False}

  while True:
    links =  [ (link, random.choice(phosts) ) for link, status in filter(lambda x:x[1] == False, link_status.items()) ]
    with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
      for ilinks in executor.map( _map, links):
        for ilink in ilinks: 
          if link_status.get(ilink) is None:
            link_status[ilink] = False
      for link in links:
        link_status[link] = True


