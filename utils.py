import os
import logging
from structure import Graph, Team

def log(data:str) -> bool:
    # Set the logging configuration
    log_file = '.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

    # Log some data
    logging.info(data)

def sum_around_borj(v:int, graph: Graph) -> int:
    sum_score = 0
    for u in graph.node[v].adj:
        sum_score += graph.node[u].score
    return sum_score

def sum_around_enemy(v:int, graph: Graph, team: Team) -> int:
    counter = 0
    for u in graph.node[v].adj:
        if graph.node[u].owner not in [-1, team.id]:
            counter += graph.node[u].troops
    return counter

def max_around_enemy(v:int, graph: Graph, team: Team) -> int:
    max_enemy = 0
    for u in graph.node[v].adj:
        if graph.node[u].owner not in [-1, team.id]:
            if graph.node[u].troops > max_enemy:
                max_enemy = graph.node[u].troops
    return max_enemy

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

def need_troop(v:int, graph: Graph, team: Team) -> int:
    if graph.node[v].is_strategic:
        if graph.node[v].troops < max_around_enemy(v, graph, team):
            return max(min(max_around_enemy(v, graph, team), 10) - graph.node[v].troops, 0)
        else:
            return 0
    else: 
        if graph.node[v].troops == 1:
            return 1
        else:
            return 0

'''
    Tasks: 
        1. Write the function of check the possibilities
'''