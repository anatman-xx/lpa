#coding=utf8

import sys
import random
import networkx as nx
import matplotlib.pyplot as plt

def read_graph_from_file(path):
    # read edge-list from file
    graph = nx.read_edgelist(path, data = (('weight', float), ))

    # initial graph node's attribute 'label' with its id
    for node, data in graph.nodes_iter(True):
        data['pre_label'] = {node : 1.0}
        data['current_label'] = dict()

    return graph

def read_game_info_from_file(path):
    game = {}

    with file(path, 'r') as f:
        for line in f:
            line = line.strip()
            data = line.split('\t')
            game[data[0]] = data[1]

    return game

# muti-label-propagation algorithm (can find overlapping communities)
# use synchronous updating for better results
def mlpa(graph, v):
    def label(graph, x, c):
        pass

    for node in graph.nodes_iter():
        count = {}
        degree = graph.degree(node)

        for neighbor in graph.neighbors_iter(node):
            neighbor_label = graph.node[node]['pre_label']
            neighbor_weight = graph.edge[node][neighbor]['weight']

            count[neighbor_label] = count.setdefault(neighbor_label, 0.0) + 1.0

        print count
        print degree

def estimate_stop_cond(graph):
    for node in graph.nodes_iter():
        count = {}

        for neighbor in graph.neighbors_iter(node):
            pass

def print_graph_info(graph):
    game_info = read_game_info_from_file('sample/id_name.info')
    info = {}

    for node, data in graph.nodes_iter(True):
        info.setdefault(graph.node[node]['current_label'], []).append(game_info.get(node, node))

    print 'node num:', len(graph.nodes())
    print 'class num:', len(info.keys())
    print 'class:', info.keys()
    print 'info:\n'
    for clazz in info:
        print clazz, ':',
        for label in info[clazz]:
            print '\'' + label + '\'',
        print '\n',

if __name__ == '__main__':
    g = read_graph_from_file('sample/t.data')
    mlpa(g, 0.5)
    #print_graph_info(g)

    #node_color = [float(g.node[v]['label']) for v in g]
    ##labels = dict([(node, node) for node, data in g.nodes_iter(True)])
    #nx.draw_networkx(g, node_color = node_color)
    #plt.show()
