import pickle
import pkg_parser

def get_dependency_graph():
    (pkgs, prob, conf) = pkg_parser.parse_pkg()
    dependency_graph = [[] for _ in range(len(pkgs))]
    for i in range(len(pkgs)):
        for j in range(len(pkgs)):
            if prob[i][j][1] < 0.1 and prob[j][i][0] > 0.9 and conf[i][j] > 0.05:
                dependency_graph[i].append(j) # i depends on j
    pickle.dump(dependency_graph, open('dependency_graph.pkl', 'wb'))
    return dependency_graph

print(get_dependency_graph())