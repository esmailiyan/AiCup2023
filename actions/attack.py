from math import ceil
from src.game import Game

from structure import State, Team, Graph

REQUIRED_NODE_TROOP = 3
MAX_NODE_TROOP = 5
REQUIRED_BORJ_TROOP = 10
MAX_BORJ_TROOP = 20

def attack(game:Game, graph:Graph, team:Team):
    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]

    my_neighbors = []
    for v in my_nodes:
        for u in graph.node[v].adj:
            if graph.node[u].owner != team.id and u not in my_neighbors:
                my_neighbors.append(u)
    enemy_neighbors = [v for v in my_neighbors if graph.node[v].owner != -1]

    
    attack_options = []
    for v in my_nodes:
        for u in graph.node[v].adj:
            if u in enemy_neighbors:
                attack_options.append((v, u))

    attack_options.sort(key=lambda x: [graph.node[x[0]].troops, graph.node[x[0]].troops / (graph.node[x[1]].troops + graph.node[x[1]].fort_troops)], reverse=True)

    for (v, u) in attack_options:
        if graph.node[v].is_strategic:
            if (graph.node[v].troops + graph.node[v].fort_troops) >= REQUIRED_BORJ_TROOP:
                if graph.node[u].owner != team.id:
                    print(game.attack(v, u, 3, 0.2))
                    graph.update(game)
        else:
            if (graph.node[v].troops + graph.node[v].fort_troops) >= REQUIRED_NODE_TROOP:
                if graph.node[u].owner != team.id:
                    print(game.attack(v, u, 1.1, 0.5))
                    graph.update(game)

    # the end of action
    return None