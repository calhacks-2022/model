import time
import pickle
import requests
# import pkg_parser
from bs4 import BeautifulSoup

(pkgs, pkg_samples) = pickle.load(open('pkg copy.pkl', 'rb'))
npmjs_url = 'https://www.npmjs.com/package/{}?activeTab=dependencies'
extra_pkgs = [] # extra_pkgs[0] -> -1, extra_pkgs[1] -> -2, etc.
dependency_graph = {}

# def getDependencyGraph1():
#     (pkgs, prob, conf) = pkg_parser.parse_pkg()
#     for i in range(len(pkgs)):
#         for j in range(len(pkgs)):
#             if prob[i][j][1] < 0.1 and prob[j][i][0] > 0.9 and conf[i][j] > 0.05:
#                 dependency_graph[i].add(j) # i depends on j
#     pickle.dump(dependency_graph, open('dependency_graph.pkl', 'wb'))
#     return dependency_graph

def pkgToIdx(pkg):
    if pkg not in pkgs:
        if pkg not in extra_pkgs:
            extra_pkgs.append(pkg)
        return -extra_pkgs.index(pkg) - 1
    return pkgs.index(pkg)

def idxToPkg(idx):
    if idx < 0:
        return extra_pkgs[-idx - 1]
    return pkgs[idx]

def searchDependencies(pkg):
    if pkgToIdx(pkg) not in dependency_graph:
        dependency_graph[pkgToIdx(pkg)] = set()
        url = npmjs_url.format(pkg)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        dependencies = soup.find_all('ul', {'aria-label': 'Dependencies'})
        if len(dependencies) > 0:
            dependencies = dependencies[0].find_all('a')
            for dependency in dependencies:
                pkg_dependency = dependency.text
                dependency_graph[pkgToIdx(pkg)].add(pkgToIdx(pkg_dependency))
                dependency_graph[pkgToIdx(pkg)].update(searchDependencies(pkg_dependency))
    return dependency_graph[pkgToIdx(pkg)]

def getDependencyGraph2():
    len_pkgs = len(pkgs)
    for i in range(len_pkgs):
        searchDependencies(pkgs[i])
        pickle.dump((dependency_graph, extra_pkgs), open('dependency_graph.pkl', 'wb'))
        print('Processed {} out of {} packages'.format(i + 1, len_pkgs))
        time.sleep(0.2)

getDependencyGraph2()