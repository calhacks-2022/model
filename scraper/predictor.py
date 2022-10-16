import json
import pickle

(pkgs, pkg_map, pkg_samples) = pickle.load(open('pkg copy.pkl', 'rb'))
pkg_cnts = [0 for _ in range(len(pkgs))]
for sample in pkg_samples:
    for pkg in sample:
        pkg_cnts[pkg] += 1
pkg_pair_cnts = [[0 for _ in range(len(pkgs))] for _ in range(len(pkgs))]
# probability i exists given j exists, probability i exists given j does not exist
for sample in pkg_samples:
    for pkg1 in sample:
        for pkg2 in sample:
            pkg_pair_cnts[pkg1][pkg2] += 1
prob = [[(1, 1) for _ in range(len(pkgs))] for _ in range(len(pkgs))]
conf = [[1 for _ in range(len(pkgs))] for _ in range(len(pkgs))]
for i in range(len(pkgs)):
    for j in range(len(pkgs)):
        if i == j:
            continue
        prob[i][j] = (pkg_pair_cnts[i][j] / pkg_cnts[j], (pkg_cnts[j] - pkg_pair_cnts[i][j]) / (len(pkg_samples) - pkg_cnts[j]))
        conf[i][j] = (pkg_cnts[i] + pkg_cnts[j] - pkg_pair_cnts[i][j]) / len(pkg_samples)
user_json = json.load(open('user_package.json', 'r'))
user_dependencies = user_json['dependencies']
user_dev_dependencies = user_json['devDependencies']
user_peer_dependencies = user_json['peerDependencies']
user_dependencies.update(user_dev_dependencies)
user_dependencies.update(user_peer_dependencies)
user_pkgs = [1 for _ in range(len(pkgs))]
pkg_suggestions = [1 for _ in range(len(pkgs))]

for pkg in user_dependencies:
    if pkg in pkg_map:
        user_pkgs[pkg_map[pkg]] = 0
        pkg_suggestions[pkg_map[pkg]] = 0

for i in range(len(pkgs)):
    for j in range(len(pkgs)):
        if user_pkgs[j] == 0:
            pkg_suggestions[i] *= (prob[i][j][0] + 1) ** conf[i][j]
        else:
            pkg_suggestions[i] *= (prob[i][j][1] + 1) ** conf[i][j]

pkg_suggestions = [(pkg_suggestions[i], i) for i in range(len(pkgs))]
pkg_suggestions.sort(reverse=True)
for i in range(10):
    print(pkgs[pkg_suggestions[i][1]], pkg_suggestions[i][0])