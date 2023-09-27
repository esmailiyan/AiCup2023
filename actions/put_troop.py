from math import ceil
from src.game import Game

from structure import State, Team, Graph
from utils import max_around_enemy, min_around_enemy
from utils import sum_around_borj

REQUIRED_NODE_TROOP = 4
MAX_NODE_TROOP = 6
REQUIRED_BORJ_TROOP = 10
MAX_BORJ_TROOP = 20

def put_troop(game:Game, graph:Graph, team:Team):
    turn = ceil(team.turn_number/3)-35

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]

    # Split troops
    if turn < 10:
        put_for_attack = team.free_troops // 3
        put_for_defense = team.free_troops - put_for_attack
    else:
        put_for_defense = team.free_troops // 3
        put_for_attack = team.free_troops - put_for_defense

    # Upgrade my borjs to required troop
    my_borjs.sort(key=lambda v: graph.node[v].score, reverse=True)

    for v in my_borjs: 
        if graph.node[v].troops + graph.node[v].fort_troops < REQUIRED_BORJ_TROOP:
            if put_for_defense > 0: 
                print(game.put_troop(v, min(2, put_for_defense)))
                put_for_defense -= min(2, put_for_defense)

    # Upgrade my nodes to first required troop
    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)
    
    for v in my_nodes: 
        if not graph.node[v].is_strategic: # Ignore the borjs
            if graph.node[v].troops < REQUIRED_NODE_TROOP:
                if put_for_defense > 0:
                    print(game.put_troop(v, 1))
                    put_for_defense -= 1

    # Upgrade my borjs to max enemy troop
    my_borjs.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)

    for v in my_borjs: 
        if graph.node[v].troops + graph.node[v].fort_troops < MAX_BORJ_TROOP:
            if graph.node[v].troops + graph.node[v].fort_troops < max_around_enemy(v, graph, team):
                if put_for_defense > 0:
                    print(game.put_troop(v, min(2, put_for_defense)))
                    put_for_defense -= min(2, put_for_defense)

    # Upgrade my nodes to max node troop
    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)
    
    for v in my_nodes: 
        if not graph.node[v].is_strategic: # Ignore the borjs
            if graph.node[v].troops < MAX_NODE_TROOP:
                if put_for_defense > 0:
                    print(game.put_troop(v, 1))
                    put_for_defense -= 1

    # the end of upgrade defense 
    if put_for_defense > 0:
        put_for_attack += put_for_defense
        put_for_defense = 0

    # Handle emergenci mode
    my_borjs.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)

    for v in my_borjs: 
        if (graph.node[v].troops + graph.node[v].fort_troops) < REQUIRED_BORJ_TROOP:
            if put_for_attack > 0:
                print(game.put_troop(v, put_for_attack))
                put_for_attack = 0

    # Upgrade one of my nodes to attack
    my_nodes.sort(key=lambda v: [int(bool(sum_around_borj(v, graph))), graph.node[v].troops, -min_around_enemy(v, graph, team)], reverse=True)

    for v in my_nodes: 
        if not graph.node[v].is_strategic:
            if put_for_attack > 0:
                print(game.put_troop(v, put_for_attack))
                put_for_attack = 0

    # the end of action
    return None
