import json
import pickle

(pkgs, pkg_samples) = pickle.load(open('pkg copy.pkl', 'rb'))

def parseJsonToSet(package_json):
    dependencies = package_json['dependencies']
    res = set()
    for dependency in dependencies:
        res.add(pkgs.index(dependency))
    return res

def parseJsonToArray(package_json):
    dependencies = package_json['dependencies']
    res = [0 for _ in range(len(pkgs))]
    for dependency in dependencies:
        res[pkgs.index(dependency)] = 1
    return res

# print(parseJsonToArray(json.loads(open('user_package.json', 'r').read())))