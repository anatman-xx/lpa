#coding=utf8

import sys
import random
import networkx as nx
import matplotlib.pyplot as plt

def read_graph_from_file(path):
    # read edge-list from file
    graph = nx.read_edgelist(path, data = (('weight', float), ))

    # initial graph's node's attribute 'label' with its id
    for node, data in graph.nodes_iter(True):
        data['prev_label'] = dict()
        data['current_label'] = {node : 1.0}

    return graph

def read_game_info_from_file(path):
    game = {}

    with file(path, 'r') as f:
        for line in f:
            line = line.strip()
            data = line.split('\t')
            game[data[0]] = data[1]

    return game

# COPRA - label-propagation algorithm
# (can find overlapping communities)
#
# note:
#     use synchronous updating for better results
#
# parameter:
#     v : number of labels of a vertex can contain
def lpa(graph, v):
    def propagate(node):
        'calculate belonging coefficient'
        labels = dict() # store vertex -> belonging coefficient

        degree = float(graph.degree(node))
        for neighbor in graph.neighbors_iter(node):
            prev_label = graph.node[neighbor]['prev_label']

            for label in prev_label:
                labels[label] = labels.get(label, 0.0)\
                    + prev_label[label] / degree
	
        # delete pair that is less then threshold
        threshold = 1.0 / v
        current_label = graph.node[node]['current_label']
        for label, coefficient in labels.items():
            if coefficient >= threshold:
                current_label[label] = coefficient

        if len(current_label) == 0:
            label_items = labels.items()
            label_items.sort(key = lambda x: x[1], reverse = True)
            maximum_coefficient_labels = [l for l, c in label_items\
                    if c == label_items[0][1]]

            label = random.sample(maximum_coefficient_labels, 1)[0]
            current_label[label] = labels[label]

        normalize(node)

        print node, current_label

    def normalize(node):
        'normalize coefficients so that they can sums to 1'
        current_label = graph.node[node]['current_label']
        sum_val = sum(current_label.values())

        if sum_val == 1:
            return

        for l in current_label:
            current_label[l] = current_label[l] / sum_val

    def reset_current_label():
        for node in graph.nodes_iter():
            graph.node[node]['prev_label'] = graph.node[node]['current_label']
            graph.node[node]['current_label'] = dict()

    loop_count = 0

    while True:
        loop_count += 1
        print 'loop', loop_count

        reset_current_label()

        for node in graph.nodes_iter():
            propagate(node)

        if estimate_stop_cond(graph) is True or loop_count >= 6:
            return

def estimate_stop_cond(graph):
    return False

def print_graph_info(graph):
    game_info = read_game_info_from_file('sample/id_name.info')
    info = {}

    for node in graph.nodes_iter():
        current_label = graph.node[node]['current_label']

        for label in current_label:
            info.setdefault(label, []).append(game_info.get(node, node))

    print 'node num:', len(graph.nodes())
    print 'class num:', len(info.keys())
    print 'class:', info.keys()
    print 'info:'
    for clazz in info:
        print '\t', clazz, ':',
        for label in info[clazz]:
            print '\'' + label + '\'',
        print '\n',

if __name__ == '__main__':
    g = read_graph_from_file('sample/k.data')
    lpa(g, 1)
    print_graph_info(g)

    node_color = [float(g.node[v]['current_label'].keys()[0]) for v in g]
    labels = dict([(node, node) for node in g.nodes_iter()])
    nx.draw_networkx(g, node_color = node_color)
    plt.show()
