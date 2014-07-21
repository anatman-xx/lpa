import networkx as nx
import matplotlib.pyplot as plt

def read_file(path):
    graph = nx.read_edgelist(path, data = (('weight', float), ))
    return graph

def init(graph):
    for n, d in graph.nodes_iter():
        d['lable'] = n

def lpa(graph):
    for i in graph.nodes_iter():
        for n in graph.neighbors_iter(i):
            pass

if __name__ == '__main__':
    g = read_file('f.data')
    node_color=[float(g.degree(v)) for v in g]
    nx.draw(g, node_color = node_color)
    plt.show()
