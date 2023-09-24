from src.game import Game

from structure import State, Team, Graph

def fort(game:Game, graph:Graph, team:Team):

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if graph.node[v].owner == team.id]
    
    my_borjs.sort(key=lambda v: graph.node[v].troops, reverse=True)
    
    for v in my_borjs:
        if graph.node[v].troops > 5:
            print(game.fort(v, graph.node[v].troops-1))
            return True

    # the end of action
    return False