from src.game import Game

from structure import State, Team, Graph

REQUIRED_NODE_TROOP = 5
OPTIMIZED_NODE_TROOP = 10
REQUIRED_BORJ_TROOP = 10
OPTIMIZED_BORJ_TROOP = 20

def move_troop(game:Game, graph:Graph, team:Team):

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]

    my_borjs.sort(key=lambda v: graph.node[v].troops)
    my_nodes.sort(key=lambda v: graph.node[v].troops)

    my_borjs.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)

    for v in my_borjs:
        reachable = game.get_reachable(v)['reachable']
        reachable.sort(key=lambda v: [-int(bool(graph.node[v].is_strategic)), graph.node[v].troops], reverse=True)
        required_troop = REQUIRED_BORJ_TROOP - (graph.node[v].troops + graph.node[v].fort_troops) 
        for u in reachable:
            if graph.node[v].is_strategic:
                max_transport = (graph.node[v].troops + graph.node[v].fort_troops) - REQUIRED_BORJ_TROOP
            else:
                max_transport = graph.node[u].troops - REQUIRED_NODE_TROOP

            if required_troop > 0 and max_transport > 0:
                return print(game.move_troop(u, v, max_transport))
    # the end of action
    return None