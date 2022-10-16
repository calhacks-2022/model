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

'''
plt.hist(np.minimum(np.array([log_likelihood(encoding) for encoding in transformed_data]), 300*np.ones(len(transformed_data))), bins=60)
plt.show()
'''

plt.imshow(np.cov(encoded_data.T))
plt.colorbar()
plt.show()