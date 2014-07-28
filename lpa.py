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
        data['label'] = node

    return graph

def read_game_info_from_file(path):
    game = {}

    with file(path, 'r') as f:
        for line in f:
            line = line.strip()
            data = line.split('\t')
            game[data[0]] = data[1]

    return game

def estimate_stop_cond(graph):
    for node in graph.nodes_iter():
        count = {}

        for neighbor in graph.neighbors_iter(node):
            neighbor_label = graph.node[neighbor]['label']
            neighbor_weight = graph.edge[node][neighbor]['weight']
            count[neighbor_label] = count.setdefault(neighbor_label, 0.0) + neighbor_weight

        # find out labels with maximum count
        count_items = count.items()
        count_items.sort(key = lambda x: x[1], reverse = True)

        # if there is not only one label with maximum count then choose one randomly
        labels = [k for k,v in count_items if v == count_items[0][1]]

        if graph.node[node]['label'] not in labels:
            return False

    return True

# label-propagation algorithm
def lpa(graph):
    loop_count = 0

    while True:
        loop_count += 1
        print 'loop', loop_count

        for node in graph.nodes_iter():
            count = {}

            for neighbor in graph.neighbors_iter(node):
                neighbor_label = graph.node[neighbor]['label']
                neighbor_weight = graph.edge[node][neighbor]['weight']
                count[neighbor_label] = count.setdefault(neighbor_label, 0.0) + neighbor_weight

            # find out labels with maximum count
            count_sum = sum(count.values())
            for key in count:
                count[key] = count[key] / count_sum
            count_items = count.items()
            count_items.sort(key = lambda x: x[1], reverse = True)

            # if there is not only one label with maximum count then choose one randomly
            labels = [(k, v) for k, v in count_items if v == count_items[0][1]]
            if len(labels) == 0:
                continue

            label = random.sample(labels, 1)[0][0]

            graph.node[node]['label'] = label

        if estimate_stop_cond(graph) is True or loop_count > 100:
            print 'complete'
            return

def cut_large_community(graph, limit):
    label_count = {}

    for node in graph.nodes_iter():
        label_count.setdefault(graph.node[node]['label'], []).append(node)

    large_community = []
    for nodes in label_count.values():
        if len(nodes) > limit:
            sub_graph = nx.Graph(graph.subgraph(nodes))
            for node in sub_graph.node:
                sub_graph.node[node]['label'] = node
            large_community.append(sub_graph)

    return large_community

def crop_edge(graph, value):
    edges = []

    for u, v, data in graph.edges_iter(data = True):
        if data['weight'] < value:
            edges.append((u, v),)

    return edges

def fitness_proportionate_selection(weights):
    random_value = random.random() * sum(weights)
    for index, weight in enumerate(weights):
        random_value -= weight
        if random_value < 0:
            return index

def print_graph_info(graph):
    game_info = read_game_info_from_file('sample/id_name.info')
    info = {}

    for node, data in graph.nodes_iter(True):
        info.setdefault(graph.node[node]['label'], []).append(game_info.get(node, node))

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
    lpa(g)
    print_graph_info(g)

    node_color = [float(g.node[v]['label']) for v in g]
    #labels = dict([(node, node) for node, data in g.nodes_iter(True)])
    nx.draw_networkx(g, node_color = node_color)
    plt.show()

    #sys.exit(0)
