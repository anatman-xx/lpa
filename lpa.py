#coding=utf8

import random
import networkx as nx
import matplotlib.pyplot as plt

def read_file(path):
    # read edge-list from file
    graph = nx.read_edgelist(path, data = (('weight', float), ))

    # initial graph node's attribute 'label' with its id
    for node, data in graph.nodes_iter(True):
        data['label'] = node

    return graph

def a(graph):
    for node in graph.nodes_iter():
        count = {}

        for neighbor in graph.neighbors_iter(node):
            count[graph.node[neighbor]['label']]\
                    = count.setdefault(graph.node[neighbor]['label'], 0) + 1

        # find out labels with maximum count
        count_items = count.items()
        count_items.sort(key = lambda x: x[1], reverse = True)

        # if there is not only one label with maximum count then choose one randomly
        labels = [k for k,v in count_items if v == count_items[0][1]]

        if graph.node[node]['label'] not in labels:
            return False

    return True

def lpa(graph):
    loop_count = 0

    while True:
        loop_count += 1
        print 'loop', loop_count

        for node in graph.nodes_iter():
            count = {}

            for neighbor in graph.neighbors_iter(node):
                count[graph.node[neighbor]['label']]\
                        = count.setdefault(graph.node[neighbor]['label'], 0) + 1

            # find out labels with maximum count
            count_items = count.items()
            count_items.sort(key = lambda x: x[1], reverse = True)

            # if there is not only one label with maximum count then choose one randomly
            labels = [k for k,v in count_items if v == count_items[0][1]]
            label = random.sample(labels, 1)[0]

            graph.node[node]['label'] = label

        if a(graph) is True:
            print 'complete'
            return

        if loop_count > 100:
            print 'complete'
            return

def print_info(graph):
    info = {}
    for node, data in graph.nodes_iter(True):
        info.setdefault(graph.node[node]['label'], []).append(node)

    print 'node num:', len(graph.nodes())
    print 'class num:', len(info.keys())
    print 'class:', info.keys()
    print 'info:', info

if __name__ == '__main__':
    g = read_file('f.data')
    lpa(g)
    print_info(g)
    #node_color = [float(g.node[v]['label']) for v in g]
    #labels = dict([(node, node) for node, data in g.nodes_iter(True)])
    #nx.draw_networkx(g, node_color = node_color, labels = labels)
    #plt.show()
