import requests
from bs4 import BeautifulSoup

def getNpmPackage(text):
    url = 'https://www.google.com/search?q=site:npmjs.com+' + text
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = [
        {
            'name': t.find('a').text,
            'url': t.find('a')['href']
        }
        for t in soup.findAll('div', {'class': 'yuRUbf'})
    ]
    return [d['url'] for d in data]

print(getNpmPackage('react-ui'))