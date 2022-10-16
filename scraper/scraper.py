import sys
import pickle
import requests
from bs4 import BeautifulSoup

MAX_PAGES = int(1e6)

REACT_REPOS_URL = 'https://github.com/topics/react'
PKG_JSON_URL = 'https://raw.githubusercontent.com/{}/main/package.json'
DEPENDENTS_URL = 'https://github.com/{}/network/dependents'

pkgs = []
pkg_map = {} # map of pkg to idx
pkg_samples = []

(pkgs, pkg_map, pkg_samples) = pickle.load(open('pkg.pkl', 'rb'))

def sampleDependentPkgJson(repo):
    sample = set()
    url = PKG_JSON_URL.format(repo)
    r = requests.get(url)
    if r.status_code == 200:
        pkg_json = r.json()
        dependencies = pkg_json.get('dependencies', {})
        dev_dependencies = pkg_json.get('devDependencies', {})
        peer_dependencies = pkg_json.get('peerDependencies', {})
        dependencies.update(dev_dependencies)
        dependencies.update(peer_dependencies)
        for dependency in dependencies:
            if dependency not in pkg_map:
                pkg_map[dependency] = len(pkg_map)
                pkgs.append(dependency)
            sample.add(pkg_map[dependency])
        if sample:
            pkg_samples.append(sample)

def searchDependents(repo):
    dependents = []
    url = DEPENDENTS_URL.format(repo)
    for _ in range(MAX_PAGES):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        data = [
            {
                'name': '{}/{}'.format(
                    t.find('a', {'data-repository-hovercards-enabled':''}).text,
                    t.find('a', {'data-hovercard-type':'repository'}).text
                ),
                'stars': int(t.find('svg', {'class': 'octicon-star'}).parent.text.strip().replace(',', ''))
            }
            for t in soup.findAll('div', {'class': 'Box-row'})
        ]
        data = [d['name'] for d in data if d['stars'] > 0]
        if len(data) > 0:
            dependents.extend(data)
            for dependent in data:
                sampleDependentPkgJson(dependent)
            print('Processed {} dependents for {}'.format(len(dependents), repo))
            pkl = open('pkg.pkl', 'wb')
            pickle.dump((pkgs, pkg_map, pkg_samples), pkl)
            pkl.close()
        paginateContainer = soup.find('div', {'class': 'paginate-container'}).find('a')
        if paginateContainer is None:
            break
        url = paginateContainer['href']

url = 'https://github.com/mui/material-ui'
repo = url[url.find('github.com/') + len('github.com/'):]
print('Processing {}'.format(repo))
searchDependents(repo)