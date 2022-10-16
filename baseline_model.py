from struct import pack
import numpy as np
from sklearn.neighbors import BallTree
import pickle
from sklearn.decomposition import PCA

pkgs, pkg_samples = pickle.load(open('pkg.pkl', 'rb'))
num_packages = len(pkgs)
print(num_packages)
encoded_data = np.zeros((len(pkg_samples), num_packages))
for i in range(len(pkg_samples)):
    encoded_data[i][list(pkg_samples[i])] = 1

pca = PCA(n_components=100)
transformed_data = pca.fit_transform(encoded_data)
bt = BallTree(transformed_data)

def get_most_similar(pkgs):
    transformed_package = pca.transform(np.reshape(pkgs, (1, -1)))
    return bt.query(transformed_package, k=100)

def recommend_package(pkgs, recs):
    dist, adj = get_most_similar(pkgs)
    adj = np.reshape(adj, -1)
    print(adj)
    print(encoded_data[adj].shape)
    ret = []
    for rec in recs:
        pop = np.sum(encoded_data[adj][:,rec])
        ret.append((-pop, rec))
    ret = sorted(ret)
    return ret

if __name__ == "__main__":
    cur_pkgs = [1606, 1607, 1201, 562, 18, 19, 62]
    recs = list(range(1608, 1750))
    pkgs = np.zeros(num_packages)
    pkgs[cur_pkgs] = 1
    print(recommend_package(pkgs, recs))