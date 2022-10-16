import sys
import pickle
from time import sleep
import requests
import random
from bs4 import BeautifulSoup

NPMJS_URL = 'https://www.npmjs.com/package/{}'
README_URL = 'https://raw.githubusercontent.com/{}/{}/README.md'

pkgs = []
(pkgs, _) = pickle.load(open('pkg.pkl', 'rb'))
readmes = [''] * len(pkgs)

readmes = pickle.load(open('readme.pkl', 'rb'))

for i in range(185, len(pkgs)):
    if readmes[i] != '':
        continue
    sleep(random.random() + 0.5)
    url = NPMJS_URL.format(pkgs[i])
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        wait = 1
        repo = soup.find('span', {'id': 'repository-link'})
        while not repo and wait < 10:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            repo = soup.find('span', {'id': 'repository-link'})
            sleep(wait)
            wait *= 2
        if repo:
            repo = repo.text
            repo = repo.replace('github.com/', '')
            url = README_URL.format(repo, 'main')
            r = requests.get(url)
            if r.status_code == 200:
                readmes[i] = r.text
            else:
                url = README_URL.format(repo, 'master')
                r = requests.get(url)
                if r.status_code == 200:
                    readmes[i] = r.text
                else:
                    print('Failed to get readme for {}, url {}'.format(pkgs[i], url))
                    readmes[i] = ' '
    pickle.dump(readmes, open('readme.pkl', 'wb'))
    count = 0
    for readme in readmes:
        if len(readme) > 2:
            count += 1
    print('Processed {} packages, total packages {}, total readmes {}'.format(i, len(pkgs), count))