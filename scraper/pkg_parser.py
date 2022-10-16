import pickle

def parsePkg():
    (pkgs, pkg_samples) = pickle.load(open('pkg copy.pkl', 'rb'))
    pkg_cnts = [0 for _ in range(len(pkgs))]
    for sample in pkg_samples:
        for pkg in sample:
            pkg_cnts[pkg] += 1
    pkg_pair_cnts = [[0 for _ in range(len(pkgs))] for _ in range(len(pkgs))]
    for sample in pkg_samples:
        for pkg1 in sample:
            for pkg2 in sample:
                pkg_pair_cnts[pkg1][pkg2] += 1
    # (probability i given j, probability i given NOT j)
    prob = [[(1, 1) for _ in range(len(pkgs))] for _ in range(len(pkgs))]
    conf = [[1 for _ in range(len(pkgs))] for _ in range(len(pkgs))]
    for i in range(len(pkgs)):
        for j in range(len(pkgs)):
            if i == j:
                continue
            if pkg_cnts[j] == 0:
                prob[i][j] = (0, 1)
            else:
                prob[i][j] = (pkg_pair_cnts[i][j] / pkg_cnts[j],
                                (pkg_cnts[i] - pkg_pair_cnts[i][j]) / (len(pkg_samples) - pkg_cnts[j]))
            conf[i][j] = (pkg_cnts[i] + pkg_cnts[j] - pkg_pair_cnts[i][j]) / len(pkg_samples)
    return (pkgs, prob, conf)

print(parsePkg()[1])