import os
import logging
from structure import Graph, Team

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

'''
    Tasks: 
        1. Write the function of check the possibilities
'''