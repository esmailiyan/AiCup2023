from math import ceil
from src.game import Game

from structure import State, Team, Graph

REQUIRED_NODE_TROOP = 5
OPTIMIZED_NODE_TROOP = 10
REQUIRED_BORJ_TROOP = 10
OPTIMIZED_BORJ_TROOP = 20

def attack(game:Game, graph:Graph, team:Team):
    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]

    my_neighbors = []
    for v in my_nodes:
        for u in graph.node[v].adj:
            if graph.node[u].owner != team.id and u not in my_neighbors:
                my_neighbors.append(u)
    enemy_neighbors = [v for v in my_neighbors if graph.node[v].owner != -1]

    my_defender = []
    my_attacker = []
    for v in borjs:
        for u in graph.node[v].adj:
            if graph.node[v].owner == team.id:
                my_defender.append(u)
            else:
                my_attacker.append(u)
    
    attack_options = []
    for v in my_nodes:
        for u in graph.node[v].adj:
            if u in enemy_neighbors:
                attack_options.append((v, u))

    attack_options.sort(key=lambda x: [graph.node[x[0]].troops, graph.node[x[0]].troops / (graph.node[x[1]].troops + graph.node[x[1]].fort_troops)], reverse=True)

    for (v, u) in attack_options:
        if graph.node[v].is_strategic:
            if (graph.node[v].troops + graph.node[v].fort_troops) >= OPTIMIZED_BORJ_TROOP:
                if graph.node[u].owner != team.id:
                    if graph.node[v].troops >= 2:
                        if graph.node[u].is_strategic:
                            print(game.attack(v, u, 1.5, 0.4))
                            graph.update(game)
                        else:
                            print(game.attack(v, u, 3, 0.2))
                            graph.update(game)
        else:
            if (graph.node[v].troops + graph.node[v].fort_troops) >= REQUIRED_NODE_TROOP:
                if graph.node[u].owner != team.id:
                    if graph.node[v].troops >= 2:
                        if graph.node[u].is_strategic:
                            print(game.attack(v, u, 1, 0.99))
                            graph.update(game)
                        else:
                            print(game.attack(v, u, 1.2, 0.3))
                            graph.update(game)
            else:
                if graph.node[u].owner != team.id:
                    if graph.node[v].troops >= 2:
                        if graph.node[u].troops <= 2:
                            if graph.node[u].is_strategic:
                                print(game.attack(v, u, 1, 0.99))
                                graph.update(game)
                            else:
                                print(game.attack(v, u, 1.5, 0.3))
                                graph.update(game)
                     
    temp_my_borjs = [v for v in graph.nodes if graph.node[v].owner == team.id and graph.node[v].is_strategic]

    if len(temp_my_borjs) > len(my_borjs):
        return True
    return False