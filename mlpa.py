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
        data['label'] = set()

    return graph

def read_game_info_from_file(path):
    game = {}

    with file(path, 'r') as f:
        for line in f:
            line = line.strip()
            data = line.split('\t')
            game[data[0]] = data[1]

    return game

def mlpa(grash):
    pass

