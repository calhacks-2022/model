import numpy as np
import pickle

from layer_1 import layer_1
from baseline_model import BallTreeModel
from mle_model import GaussianModel

# Return top 5-10 libraries
def integration_test(user_text_input, user_dependencies):
    pass

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
