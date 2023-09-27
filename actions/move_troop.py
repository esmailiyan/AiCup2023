from src.game import Game

from structure import State, Team, Graph

REQUIRED_NODE_TROOP = 4
MAX_NODE_TROOP = 6
REQUIRED_BORJ_TROOP = 10
MAX_BORJ_TROOP = 20

def move_troop(game:Game, graph:Graph, team:Team):

    flag = False

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]

    my_borjs.sort(key=lambda v: graph.node[v].troops)
    my_nodes.sort(key=lambda v: graph.node[v].troops)

    move_options = []
    for v in my_borjs:
        if graph.node[v].troops + graph.node[v].fort_troops < REQUIRED_BORJ_TROOP:
            move_options.append(v)
    for v in my_nodes:
        if graph.node[v].troops < REQUIRED_NODE_TROOP:
            move_options.append(v)

    for v in move_options:
        if not flag:
            reachable = game.get_reachable(v)['reachable']
            reachable.sort(key=lambda v: [-int(graph.node[v].is_strategic), graph.node[v].troops], reverse=True)
            for u in reachable:
                if graph.node[u].troops - graph.node[v].troops > 2:
                    if not flag:
                        print(game.move_troop(u, v, (graph.node[u].troops - graph.node[v].troops)//2))
                        flag = True
                        break

    # the end of action
    return None