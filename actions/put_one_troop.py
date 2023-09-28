from src.game import Game

from structure import State, Team, Graph
from utils import max_around_enemy
from utils import sum_around_borj
from utils import count_around_freind, count_around_enemy

def put_one_troop(game:Game, graph:Graph, team:Team):

    if team.id == 1: # Attacker mode
        REQUIRED_NODE_TROOP = 2
        REQUIRED_BORJ_TROOP = 6
    else: # Normal mode
        REQUIRED_NODE_TROOP = 3
        REQUIRED_BORJ_TROOP = 8

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]

    # Get strategic nodes
    borjs.sort(key=lambda v: [graph.node[v].score, -graph.node[v].degree], reverse=True)

    for v in borjs:
        if graph.node[v].owner == -1:
            return print(game.put_one_troop(v))

    # Get other nodes
    for v in borjs:
        if count_around_freind(v, graph, team) < 1: # یادم باشه باگ اینکه اون مجاور استراتژیکمون باشه رو درست کنم 
            free_neighbors = [u for u in graph.node[v].adj if graph.node[u].owner == -1]
            free_neighbors.sort(key=lambda v: [sum_around_borj(v, graph), graph.node[v].degree], reverse=True)
            for u in free_neighbors:
                return print(game.put_one_troop(u))
                
    # Strengthening my nodes to required
    my_nodes.sort(key=lambda v: [int(bool(graph.node[v].is_strategic)), -graph.node[v].troops, max_around_enemy(v, graph, team)], reverse=True)

    for v in my_nodes:
        if graph.node[v].is_strategic:
            if graph.node[v].troops < REQUIRED_BORJ_TROOP:
                return print(game.put_one_troop(v))
        else: 
            if graph.node[v].troops < REQUIRED_NODE_TROOP:
                return print(game.put_one_troop(v))

    # in the end
    my_nodes.sort(key=lambda v: [-graph.node[v].troops, graph.node[v].score], reverse=True)

    for v in my_borjs:
        return print(game.put_one_troop(v))