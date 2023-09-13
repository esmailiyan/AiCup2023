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

def max_around_friend(v:int, graph: Graph, team: Team) -> int:
    max_friend = 0
    for u in graph.node[v].adj:
        if graph.node[u].owner == team.id:
            if graph.node[u].troops > max_friend:
                max_friend = graph.node[u].troops
    return max_friend

def min_around_enemy(v:int, graph: Graph, team: Team) -> int:
    min_enemy = 1000
    for u in graph.node[v].adj:
        if graph.node[u].owner not in [-1, team.id]:
            if graph.node[u].troops < min_enemy:
                min_enemy = graph.node[u].troops
    return min_enemy

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