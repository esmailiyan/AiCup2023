import random
from src.game import Game
from structure import State, Team, Graph
from utils import log, sum_around_score, min_around_enemy, max_around_enemy, count_around_freind, count_around_enemy, draw_graph

flag = False
team = Team()
graph = Graph()

''' Initializer 1 '''
def initializer(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    my_nodes = [v for v in graph.nodes if graph.node[v].owner == team.id]
    free_nodes = [v for v in graph.nodes if graph.node[v].owner == -1]
    enemy_nodes = [v for v in graph.nodes if graph.node[v].owner not in [-1, team.id]]

    borjs = [v[0] for v in graph.borj]

    my_neighbors = []
    for v in my_nodes:
        for u in graph.node[v].adj:
            if graph.node[u].owner != team.id and u not in my_neighbors:
                my_neighbors.append(u)
    
    free_neighbors = []
    enemy_neighbors = []
    for v in my_neighbors:
        if graph.node[v].owner == -1:
            free_neighbors.append(v)
        else:
            enemy_neighbors.append(v)

    my_nodes.sort(key=lambda v: [graph.node[v].score, -graph.node[v].troops, max_around_enemy(v, graph, team)[0]], reverse=True)
    free_nodes.sort(key=lambda v: [sum_around_score(v, graph), count_around_freind(v, graph, team), -count_around_enemy(v, graph, team)], reverse=True)
    borjs.sort(key=lambda v: [graph.node[v].score, -graph.node[v].degree], reverse=True)

    # log("----------------------------")
    # log(team)
    # log(graph)
    # log("my_nodes: " + str(my_nodes) + '\n')
    # log("free_nodes: " + str(free_nodes) + '\n')
    # log("enemy_nodes: " + str(enemy_nodes) + '\n')
    # log("my_neighbors: " + str(my_neighbors))
    # log("free_neighbors: " + str(free_neighbors))
    # log("enemy_neighbors: " + str(enemy_neighbors))
    # for i in range(len(borjs)):     log(f"Borj:\n- index:{i}\n- id:{graph.node[borjs[i]].id}\n- score:{graph.node[borjs[i]].score}\n- degree:{graph.node[borjs[i]].degree}\n")
    # for i in graph.node:    log(str(i))
    # log("putting_one_troop: " + str(response) + '\n')

    for v in borjs:
        if v in free_nodes:
            response = game.put_one_troop(v)
            log(f"putting_one_troop on {v}, " + str(response) + '\n')
            graph.update(game)
            draw_graph(graph, team)
            return
    
    for v in free_nodes:
        response = game.put_one_troop(v)
        log(f"putting_one_troop on {v}, " + str(response) + '\n')
        graph.update(game)
        draw_graph(graph, team)
        return

    for v in my_nodes:
        if graph.node[v].is_strategic:
            if graph.node[v].troops + graph.node[v].fort_troops < max_around_enemy(v, graph, team)[0]:
                response = game.put_one_troop(v)
                log(f"putting_one_troop on {v}, " + str(response) + '\n')
                graph.update(game)
                draw_graph(graph, team)
                return
        else: 
            if count_around_enemy(v, graph, team) != 0:
                response = game.put_one_troop(v)
                log(f"putting_one_troop on {v}, " + str(response) + '\n')
                graph.update(game)
                draw_graph(graph, team)
                return
    
    for v in my_nodes:
        response = game.put_one_troop(v)
        log(f"putting_one_troop on {v}, " + str(response) + '\n')
        graph.update(game)
        draw_graph(graph, team)
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