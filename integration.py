from .cohere.layer_1 import layer_1

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
