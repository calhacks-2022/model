from base64 import encode
import numpy as np
import pickle
from sklearn.random_projection import johnson_lindenstrauss_min_dim, GaussianRandomProjection
import matplotlib.pyplot as plt

pkgs, pkg_samples = pickle.load(open('pkg.pkl', 'rb'))
num_packages = len(pkgs)
print(num_packages)
encoded_data = np.zeros((len(pkg_samples), num_packages))
for i in range(len(pkg_samples)):
    encoded_data[i][list(pkg_samples[i])] = 1

pkg_indices = [1,2,3]
print(np.cov(encoded_data[:, pkg_indices].T))

transformer = GaussianRandomProjection(n_components=120)
transformed_data = transformer.fit_transform(encoded_data)
print(transformed_data.shape)
cov = np.cov(transformed_data.T)
print(len(cov))
#generate feature covariance matrix
cov = np.cov(transformed_data.T)
mean = np.mean(transformed_data, axis=0)
cov_inv = np.linalg.inv(cov)
def log_likelihood(encoding):
    return (encoding - mean) @ (cov_inv @ (encoding - mean))


def recommend_package(pkgs, recs):
    ret = []
    for rec in recs:
        if rec == 1608:
            print('good')
        if pkgs[rec] == 1:
            return rec
        pkgs_copy = pkgs.copy()
        pkgs_copy[rec] += 1
        transformed_pkgs = np.reshape(transformer.transform(np.reshape(pkgs_copy, (1, -1))), -1)
        score = log_likelihood(transformed_pkgs)
        ret.append((score, rec))
    ret = sorted(ret)
    return ret

if __name__ == "__main__":
    cur_pkgs = [1606, 1607, 1201, 562, 18, 19, 62]
    recs = list(range(1608, 1750))
    pkgs = np.zeros(num_packages)
    pkgs[cur_pkgs] = 1
    print(recommend_package(pkgs, recs))

