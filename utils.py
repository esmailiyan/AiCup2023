import os
import logging
from structure import Graph, Team
import networkx as nx
import matplotlib.pyplot as plt

draw_flag = True
G = nx.Graph()
pos = None

def log(data:str) -> bool:
    # Set the logging configuration
    log_file = '.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

    # Log some data
    logging.info(data)

def sum_around_score(v:int, graph: Graph) -> int:
    sum_score = 0
    for u in graph.node[v].adj:
        sum_score += graph.node[u].score
    return sum_score

def min_around_enemy(v:int, graph: Graph, team: Team) -> int:
    min_enemy = 1e6+7
    counter = 0
    for u in graph.node[v].adj:
        if graph.node[u].owner in [-1, team.id]:
            continue
        if graph.node[u].troops == min_enemy:
            counter += 1
        elif graph.node[u].troops < min_enemy:
            min_enemy = graph.node[u].troops
            counter = 1
    return [min_enemy, counter]

def max_around_enemy(v:int, graph: Graph, team: Team) -> int:
    max_enemy = 0
    counter = 0
    for u in graph.node[v].adj:
        if graph.node[u].owner in [-1, team.id]:
            continue
        if graph.node[u].troops == max_enemy:
            counter += 1
        elif graph.node[u].troops > max_enemy:
            max_enemy = graph.node[u].troops
            counter = 1
    return [max_enemy, counter]

def count_around_freind(v:int, graph: Graph, team: Team) -> int:
    counter = 0
    for u in graph.node[v].adj:
        if graph.node[u].owner == team.id:
            counter += 1
    return counter

def count_around_enemy(v:int, graph: Graph, team: Team) -> int:
    counter = 0
    for u in graph.node[v].adj:
        if graph.node[u].owner not in [-1, team.id]:
            counter += 1
    return counter

def draw_graph(graph: Graph, team: Team):
    global draw_flag, g, pos

    if draw_flag:
        for i in graph.nodes:
            G.add_node(i)
            for j in graph.node[i].adj:
                G.add_edge(i, j) 
            draw_flag = False
        pos = nx.spring_layout(G)
        
    node_colors = []
    for i in G.nodes():
        if graph.node[i].owner == team.id:
            if graph.node[i].is_strategic:
                node_colors.append("red")
            else:
                node_colors.append("green")
        elif graph.node[i].owner == -1:
            if graph.node[i].is_strategic:
                node_colors.append("orange")
            else:
                node_colors.append("blue")
        else:
            if graph.node[i].is_strategic:
                node_colors.append("black")
            else:
                node_colors.append("gray")
    nx.draw(G, pos, with_labels=True, node_size=400, node_color=node_colors, font_size=12, font_color='black', font_weight='normal')
    plt.title("Undirected Graph")
    plt.show()

'''
    Tasks: 
        1. Write the function of check the possibilities
'''