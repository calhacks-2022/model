from base64 import encode
import numpy as np
import pickle
from sklearn.random_projection import johnson_lindenstrauss_min_dim, GaussianRandomProjection
import matplotlib.pyplot as plt

class GaussianModel():
    def __init__(self):
        self.random_projection = None
        self.cov = None
        self.mean = None
        self.num_packages = None
    
    def train(self, pkgs, pkg_samples):
        num_packages = len(pkgs)
        self.num_packages = num_packages
        print(num_packages)
        encoded_data = np.zeros((len(pkg_samples), num_packages))
        for i in range(len(pkg_samples)):
            encoded_data[i][list(pkg_samples[i])] = 1
        self.random_projection = GaussianRandomProjection(n_components=120).fit(encoded_data).components_
        transformed_data = encoded_data @ self.random_projection.T
        self.cov = np.cov(transformed_data.T)
        self.mean = np.mean(transformed_data, axis=0)
        self.cov_inv = np.linalg.inv(self.cov)
    
    def log_likelihood(self, encoding):
        return (encoding - self.mean) @ (self.cov_inv @ (encoding - self.mean))
    
    def recommend_package(self, pkgs, recs):
        new_pkgs = np.zeros(self.num_packages)
        new_pkgs[pkgs] = 1
        ret = []
        for rec in recs:
            '''
            if rec == 1608:
                print('good')
            if pkgs[rec] == 1:
                return rec
            '''
            pkgs_copy = new_pkgs.copy()
            pkgs_copy[rec] += 1
            transformed_pkgs = pkgs_copy @ self.random_projection.T
            score = self.log_likelihood(transformed_pkgs)
            ret.append((score, rec))
        ret = sorted(ret)
        return ret
    
    def save_model(self, name='gaussian_model.pkl'):
        pickle.dump(self, open(name, 'wb'))

    def load_model(name='gaussian_model.pkl'):
        return pickle.load(open(name, 'rb'))
'''
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


if __name__ == "__main__":
    cur_pkgs = [1606, 1607, 1201, 562, 18, 19, 62]
    recs = list(range(1608, 1750))
    pkgs = np.zeros(num_packages)
    pkgs[cur_pkgs] = 1
    print(recommend_package(pkgs, recs))

'''


if __name__ == "__main__":
    pkgs, pkg_samples = pickle.load(open('pkg.pkl', 'rb'))
    train_ratio = 1
    train_indices = np.random.choice(len(pkg_samples), round(train_ratio * len(pkg_samples)), replace=False)
    test_indices = np.asarray([i for i in range(len(pkg_samples)) if i not in train_indices])
    pkg_samples_train = np.array(pkg_samples)[train_indices]
    model = pickle.load(open("gaussian_model.pkl", "rb"))
    #model = GaussianModel()
    #model.train(pkgs, pkg_samples_train)
    cur_pkgs = [1606, 1607, 1201, 562, 18, 19, 62]
    recs = list(range(1608, 1700))
    print(model.recommend_package(cur_pkgs, recs))
    #model.save_model()