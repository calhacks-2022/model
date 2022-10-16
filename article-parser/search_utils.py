import pandas as pd
import requests
import re
import numpy as np
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
from googlesearch import search
from time import sleep

query = "best ui libraries in react"
 
def getPageText(url): #Returns one long string
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    req = urllib.request.Request(url, headers=hdr)
    html = urllib.request.urlopen(req).read()
    return text_from_html(html)

def getWebpageLinks(searchPhrase, count=10):
    res = []
    return list(search(searchPhrase, stop=count))