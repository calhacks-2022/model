import json
import pickle
import pkg_parser

def predict(user_json):
    (pkgs, prob, conf) = pkg_parser.parsePkg()
    user_json = json.load(open('user_package.json', 'r'))
    user_dependencies = user_json['dependencies']
    user_pkgs = [1 for _ in range(len(pkgs))]
    pkg_suggestions = [1 for _ in range(len(pkgs))]

    for pkg in user_dependencies:
        if pkg in pkgs:
            user_pkgs[pkgs.index(pkg)] = 0
            pkg_suggestions[pkgs.index(pkg)] = 0

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

# print(predict('user_package.json'))