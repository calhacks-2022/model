import numpy as np
import pickle

def generate_test_cases(num_test_cases):
    (pkgs, pkg_samples) = pickle.load(open('pkg.pkl', 'rb'))

    num_samples = len(pkg_samples)
    num_pkgs = len(pkgs)

    pkg_freqs = np.zeros(num_pkgs)
    for sample in pkg_samples:
        for package in sample:
            pkg_freqs[package] += 1
    pkg_freqs = pkg_freqs / np.sum(pkg_freqs)

    samples_chosen = np.random.choice(num_samples, num_test_cases)
    choose_pos = np.random.rand(num_test_cases) < 0.25

    test_cases = [] # each element is of the form (set of package, predicted package, 0/1)
    for i in range(num_test_cases):
        sample = pkg_samples[samples_chosen[i]].copy()
        removed_el = np.random.choice(tuple(sample))
        sample.remove(removed_el)
        if choose_pos[i]:
            test_cases.append((sample, removed_el, 1))
        else:
            label = np.random.choice(num_pkgs, p=pkg_freqs)
            if not label in sample:
                test_cases.append((sample, label, 0))
            else:
                test_cases.append((sample, label, 1))

    return test_cases

if __name__ == "__main__":
    print(generate_test_cases(50000))
