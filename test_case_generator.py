import numpy as np
import pickle

def generate_test_cases(num_test_cases):
    (pkgs, pkg_samples) = pickle.load(open('pkg.pkl', 'rb'))

    num_samples = len(pkg_samples)
    num_pkgs = len(pkgs)

    pkg_sample_lengths = np.asarray([len(sample) for sample in pkg_samples])
    pkg_sample_lengths = pkg_sample_lengths / np.sum(pkg_sample_lengths)

    samples_chosen = np.random.choice(num_samples, num_test_cases, p=pkg_sample_lengths)
    choose_pos = np.random.rand(num_test_cases) < 0.25

    test_cases = [] # each element is of the form (set of package, predicted package, 0/1)
    for i in range(num_test_cases):
        sample = pkg_samples[samples_chosen[i]].copy()
        removed_el = np.random.choice(tuple(sample))
        sample.remove(removed_el)
        if choose_pos[i]:
            test_cases.append((sample, removed_el, 1))
        else:
            while True:
                wrong_num = np.random.randint(num_pkgs)
                if wrong_num != removed_el and wrong_num not in sample:
                    test_cases.append((sample, wrong_num, 0))
                    break

    return test_cases

if __name__ == "__main__":
    print(generate_test_cases(10))
