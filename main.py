import random
from src.game import Game
from structure import State, Team, Graph
from utils import log
from utils import max_around_enemy
from utils import sum_around_borj, sum_around_enemy
from utils import count_around_freind, count_around_enemy

flag = False
team = Team()
graph = Graph()

def initializer(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    REQUIRED_TROOP = 2

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]
    free_nodes = [v for v in nodes if graph.node[v].owner == -1]
    enemy_nodes = [v for v in nodes if graph.node[v].owner not in [-1, team.id]]
    my_weak_nodes = [v for v in my_nodes if graph.node[v].troops < REQUIRED_TROOP]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]
    my_weak_borjs = [v for v in my_borjs if graph.node[v].troops < max_around_enemy(v, graph, team)]

    my_neighbors = []
    for v in my_nodes:
        for u in graph.node[v].adj:
            if graph.node[u].owner != team.id and u not in my_neighbors:
                my_neighbors.append(u)
    free_neighbors = [v for v in my_neighbors if graph.node[v].owner == -1]
    enemy_neighbors = [v for v in my_neighbors if graph.node[v].owner != -1]

    my_nodes.sort(key=lambda v: [graph.node[v].score, -graph.node[v].troops, max_around_enemy(v, graph, team)], reverse=True)
    free_nodes.sort(key=lambda v: [sum_around_borj(v, graph), count_around_freind(v, graph, team), -count_around_enemy(v, graph, team)], reverse=True)
    borjs.sort(key=lambda v: [graph.node[v].score, -graph.node[v].degree], reverse=True)

    for v in borjs:
        if graph.node[v].owner == -1:
            response = game.put_one_troop(v)
            print(response)
            return

    if team.id == 1: # player 1
        for v in free_nodes:
            if sum_around_borj(v, graph) != 0 or count_around_freind(v, graph, team) != 0:
                response = game.put_one_troop(v)
                print(response)
                return

        for v in my_nodes:
            if graph.node[v].is_strategic:
                if graph.node[v].troops < max_around_enemy(v, graph, team):
                    response = game.put_one_troop(v)
                    print(response)
                    return
            else: 
                if count_around_enemy(v, graph, team) != 0:
                    response = game.put_one_troop(v)
                    print(response)
                    return

    else: # Player 2 , 3
        required_troops = 0
        for v in my_weak_borjs:
            required_troops += (max_around_enemy(v, graph, team) - graph.node[v].troops)
        for v in my_weak_nodes:
            required_troops += (REQUIRED_TROOP - graph.node[v].troops)

        if team.free_troops > required_troops: 
            # Get new nodes
            for v in free_nodes:
                if sum_around_borj(v, graph) != 0 or count_around_freind(v, graph, team) != 0:
                    response = game.put_one_troop(v)
                    print(response)
                    return
        else: 
            # Strengthening my nodes
            for v in my_nodes:
                if graph.node[v].is_strategic:
                    if graph.node[v].troops < max_around_enemy(v, graph, team):
                        response = game.put_one_troop(v)
                        print(response)
                        return
                else: 
                    if count_around_enemy(v, graph, team) != 0:
                        response = game.put_one_troop(v)
                        print(response)
                        return

def turn(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    '''
        Tasks: 
            1. Write algorithm of locating new troops
            2. Write algorithm of attack
            3. Write algorithm of move troops
            4. Write algorithm of transformation the defense troops
    '''