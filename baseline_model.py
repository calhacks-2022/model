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

train_ratio = 0.9
train_indices = np.random.choice(len(pkg_samples), round(train_ratio * len(pkg_samples)), replace=False)
test_indices = np.asarray([i for i in range(len(pkg_samples)) if i not in train_indices])
train_encoded_data = encoded_data[train_indices]
test_encoded_data = encoded_data[test_indices]

pca = PCA(n_components=100)
transformed_data = pca.fit_transform(train_encoded_data)
bt = BallTree(transformed_data)

def get_most_similar(pkgs):
    transformed_package = pca.transform(np.reshape(pkgs, (1, -1)))
    return bt.query(transformed_package, k=100)

def recommend_package(pkgs, recs):
    dist, adj = get_most_similar(pkgs)
    adj = np.reshape(adj, -1)
    # print(adj)
    # print(train_encoded_data[adj].shape)
    ret = []
    for rec in recs:
        pop = np.sum(train_encoded_data[adj][:,rec])
        ret.append((-pop, rec))
    ret = sorted(ret)
    return ret

def test_model():
    success = []
    num_recs_per_test = 25
    for test_index in test_indices:
        sample_encoded_copy = encoded_data[test_index].copy()
        ans = np.random.choice(np.asarray(list(pkg_samples[test_index])))
        sample_encoded_copy[ans] = 0
        recs = np.random.choice(num_packages, num_recs_per_test, replace=False)
        recs = np.append(recs, ans)
        recommended_packages = recommend_package(sample_encoded_copy, recs)
        # print(ans)
        # print(pkgs[recommended_packages[0][1]])
        # print(pkgs[recommended_packages[1][1]])
        # print(pkgs[recommended_packages[2][1]])
        # print(pkgs[ans])
        # print(recommended_packages)
        test_success = recommended_packages[0][1] == ans
        # print(test_success)
        success.append(test_success)
    return sum(success) / len(success)

if __name__ == "__main__":
    # cur_pkgs = [1606, 1607, 1201, 562, 18, 19, 62]
    # recs = list(range(1608, 1750))
    # pkgs = np.zeros(num_packages)
    # pkgs[cur_pkgs] = 1
    # print(recommend_package(pkgs, recs))
    print(test_model())
