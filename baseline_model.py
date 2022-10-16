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
    transformed_package = pca.transform(pkgs)
    return bt.query(transformed_package, k=100)

def recommend_package(pkgs, recs):
    adj = get_most_similar(pkgs)
    best_pop = -1
    ret = recs[0]
    for rec in recs:
        pop = np.sum(encoded_data[adj,rec])
        if pop > best_pop:
            best_pop = pop
            ret = rec
    return ret
