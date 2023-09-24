from src.game import Game

from structure import State, Team, Graph
from utils import max_around_enemy
from utils import sum_around_borj
from utils import count_around_freind, count_around_enemy

REQUIRED_NODE_TROOP = 3
REQUIRED_BORJ_TROOP = 6

def put_one_troop(game:Game, graph:Graph, team:Team):

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]
    free_nodes = [v for v in nodes if graph.node[v].owner == -1]
    my_weak_nodes = [v for v in my_nodes if graph.node[v].troops < REQUIRED_NODE_TROOP and not graph.node[v].is_strategic]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]
    my_weak_borjs = [v for v in my_borjs if graph.node[v].troops < REQUIRED_BORJ_TROOP]

    my_nodes.sort(key=lambda v: [-graph.node[v].troops, graph.node[v].score, max_around_enemy(v, graph, team)], reverse=True)
    my_borjs.sort(key=lambda v: [max_around_enemy(v, graph, team), -graph.node[v].troops, graph.node[v].score], reverse=True)
    free_nodes.sort(key=lambda v: [sum_around_borj(v, graph), count_around_freind(v, graph, team), -count_around_enemy(v, graph, team), graph.node[v].degree], reverse=True)
    borjs.sort(key=lambda v: [graph.node[v].score, -graph.node[v].degree], reverse=True)

    # Get strategic nodes
    for v in borjs:
        if graph.node[v].owner == -1:
            return print(game.put_one_troop(v))

    required_troops = 0
    for v in my_weak_borjs:
        required_troops += (REQUIRED_BORJ_TROOP - graph.node[v].troops)
    for v in my_weak_nodes:
        required_troops += (REQUIRED_NODE_TROOP - graph.node[v].troops)

    if team.id == 1:
        required_troops -= len(my_nodes)//4
        for v in my_borjs:
            required_troops -= graph.node[v].score

    # Get new nodes
    if team.free_troops > required_troops:
        for v in free_nodes:
            if sum_around_borj(v, graph) != 0 or count_around_freind(v, graph, team) != 0:
                return print(game.put_one_troop(v))

    # Strengthening my nodes
    for v in my_nodes:
        if graph.node[v].is_strategic:
            if graph.node[v].troops < max_around_enemy(v, graph, team):
                return print(game.put_one_troop(v))
        else: 
            if count_around_enemy(v, graph, team) != 0:
                return print(game.put_one_troop(v))

    for v in my_borjs:
        return print(game.put_one_troop(v))