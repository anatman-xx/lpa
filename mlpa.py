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
        data['prev_label'] = {node : 1.0}
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

# COPRA - muti-label-propagation algorithm
# (can find overlapping communities)
#
# note:
#     use synchronous updating for better results
#
# parameter:
#     v : number of labels of a vertex can contain
def lpa(graph, v):
    def propagate(node):
	# calculate belonging coefficient
	labels = dict() # store vertex -> belonging coefficient

        for neighbor in graph.neighbors_iter(node):
	    for label in graph.node[neighbor]:
	        labels[label] = labels.get(label, 0.0)\
			+ graph.node[neighbor]['prev_label'][label]
	
	degree = graph.degree(node)
	for label in labels:
	    labels[label] /= degree
	
        # delete pair that is less then threshold
	threshold = 1.0 / v
	for label in labels:
	    if labels[label] < threshold:
		del labels[label]

    def normalize(node):
        sum_val = 0
        for neighbor in graph.neighbors_iter(node):
            sum_val += graph.node[neighbor]['']

        for neighbor in graph.neighbors_iter(node):
            pass

    for node in graph.nodes_iter():
        degree = graph.degree(node)

        for neighbor in graph.neighbors_iter(node):
            neighbor_label = graph.node[node]['prev_label']
            neighbor_weight = graph.edge[node][neighbor]['weight']

            neighbor_label['current_label'] = ''
            #count[neighbor_label] = count.setdefault(neighbor_label, 0.0) + 1.0

def estimate_stop_cond(graph):
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
    lpa(g, 0.5)
    print_graph_info(g)

    #node_color = [float(g.node[v]['label']) for v in g]
    #labels = dict([(node, node) for node, data in g.nodes_iter(True)])
    #nx.draw_networkx(g, node_color = node_color)
    #plt.show()
