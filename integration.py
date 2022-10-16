import numpy as np
import pickle

from layer_1 import layer_1
from baseline_model import BallTreeModel
from mle_model import GaussianModel

# Return top 5-10 libraries
def integration_test(user_text_input, user_dependencies):
    plausible_libs = layer_1(user_text_input)
    gaussian_model = pickle.load(open("gaussian_model.pkl", "rb"))
    pkgs, _ = pickle.load(open("pkg.pkl", "rb"))
    recs = []
    print("successfully load")
    for lib in plausible_libs:
        if lib in pkgs:
            recs.append(pkgs.index(lib))
    pkg_lst = []
    for dep in user_dependencies:
        if dep in pkgs:
            pkg_lst.append(pkgs.index(dep))
    print(recs)
    print(pkg_lst)
    ranking = gaussian_model.recommend_package(pkg_lst, recs)
    print(ranking)
    print(pkgs[ranking[0][1]])
    print(pkgs[ranking[1][1]])
    print(pkgs[ranking[2][1]])

user_dependencies = [
    '@testing-library/jest-dom',
    '@testing-library/react',
    '@testing-library/user-event',
    'axios',
    'react',
    'react-dom',
    'react-drag-drop-files',
    'react-force-graph-3d',
    'react-scripts',
    'three',
    'three-spritetext',
    'web-vitals'
]

user_text_input = "I want to include data visualization"

integration_test(user_text_input, user_dependencies)
