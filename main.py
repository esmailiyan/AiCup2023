import random
from math import ceil
from src.game import Game
from structure import State, Team, Graph
from utils import log
from utils import max_around_enemy, min_around_enemy, max_around_friend
from utils import sum_around_borj, sum_around_enemy
from utils import count_around_freind, count_around_enemy

flag = False
team = Team()
graph = Graph()

def initializer(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    print(f"\initializer:{ceil(team.turn_number/3)}\n")

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
    free_nodes.sort(key=lambda v: [sum_around_borj(v, graph), count_around_freind(v, graph, team), -count_around_enemy(v, graph, team), graph.node[v].degree], reverse=True)
    borjs.sort(key=lambda v: [graph.node[v].score, -graph.node[v].degree], reverse=True)

    # ----- Start algorithm -----
    for v in borjs:
        if graph.node[v].owner == -1:
            response = game.put_one_troop(v)
            print(response)
            game.next_state()
            return

    if team.id == 1: # player 1
        for v in free_nodes:
            if sum_around_borj(v, graph) != 0 or count_around_freind(v, graph, team) != 0:
                response = game.put_one_troop(v)
                print(response)
                game.next_state()
                return

        for v in my_nodes:
            if graph.node[v].is_strategic:
                if graph.node[v].troops < max_around_enemy(v, graph, team):
                    response = game.put_one_troop(v)
                    print(response)
                    game.next_state()
                    return
            else: 
                if count_around_enemy(v, graph, team) != 0:
                    response = game.put_one_troop(v)
                    print(response)
                    game.next_state()
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
                    game.next_state()
                    return
        else: 
            # Strengthening my nodes
            for v in my_nodes:
                if graph.node[v].is_strategic:
                    if graph.node[v].troops < max_around_enemy(v, graph, team):
                        response = game.put_one_troop(v)
                        print(response)
                        game.next_state()
                        return
                else: 
                    if count_around_enemy(v, graph, team) != 0:
                        response = game.put_one_troop(v)
                        print(response)
                        game.next_state()
                        return

def turn(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    turn = ceil(team.turn_number/3)-35
    print(f"\nturn:{turn}\n")

    global flag
    FIRST_REQUIRED_TROOP = 3
    SECOND_REQUIRED_TROOP = 4
    REQUIRED_BORJ_TROOP = 10
    MAX_BORJ_TROOP = 15

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]
    free_nodes = [v for v in nodes if graph.node[v].owner == -1]
    enemy_nodes = [v for v in nodes if graph.node[v].owner not in [-1, team.id]]
    my_weak_nodes = [v for v in my_nodes if graph.node[v].troops < FIRST_REQUIRED_TROOP]

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

    # ----- Start algorithm -----
    if turn < 10:
        put_for_attack = team.free_troops // 3
        put_for_defense = team.free_troops - put_for_attack
    else:
        put_for_defense = team.free_troops // 3
        put_for_attack = team.free_troops - put_for_defense

    # ----- Locating new troops -----
    my_borjs.sort(key=lambda v: graph.node[v].score, reverse=True)

    for v in my_borjs: # Upgrade my borjs to required troop
        if graph.node[v].troops + graph.node[v].fort_troops < REQUIRED_BORJ_TROOP:
            if put_for_defense > 0: 
                print(game.put_troop(v, min(2, put_for_defense)))
                put_for_defense -= min(2, put_for_defense)
    
    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)

    for v in my_nodes: # Upgrade my nodes to first required troop
        if not graph.node[v].is_strategic: # Ignore the borjs
            if graph.node[v].troops < FIRST_REQUIRED_TROOP:
                if put_for_defense > 0:
                    print(game.put_troop(v, min(1, put_for_defense)))
                    put_for_defense -= min(1, put_for_defense)
    
    my_borjs.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)

    for v in my_borjs: # Upgrade my borjs to max enemy troop
        if graph.node[v].troops < MAX_BORJ_TROOP:
            if graph.node[v].troops < max_around_enemy(v, graph, team):
                if put_for_defense > 0:
                    print(game.put_troop(v, min(2, put_for_defense)))
                    put_for_defense -= min(2, put_for_defense)

    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)

    for v in my_nodes: # Upgrade my nodes to second required troop
        if not graph.node[v].is_strategic: # Ignore the borjs
            if graph.node[v].troops < SECOND_REQUIRED_TROOP:
                if put_for_defense > 0:
                    print(game.put_troop(v, min(1, put_for_defense)))
                    put_for_defense -= min(1, put_for_defense)
    
    my_nodes.sort(key=lambda v: [int(bool(sum_around_borj(v, graph))), graph.node[v].troops, -min_around_enemy(v, graph, team)], reverse=True)

    attacker = -1
    for v in my_nodes: # Upgrade one of my nodes to attack
        if not graph.node[v].is_strategic:
            if put_for_attack > 0:
                attacker = v
                print(game.put_troop(v, put_for_attack))
                put_for_attack = 0
    
    game.next_state()

    # ----- Attack -----
    my_neighbors.sort(key=lambda v: [graph.node[v].troops + graph.node[v].fort_troops , -max_around_friend(v, graph, team)])

    for v in my_neighbors:
        graph.node[v].adj.sort(key=lambda v: graph.node[v].troops)
        for u in graph.node[v].adj:
            if graph.node[u].owner == team.id:
                if graph.node[u].troops > graph.node[v].troops + graph.node[v].fort_troops:
                    print(game.attack(u, v, 1.1, 0.5))
                    graph.update(game)
                    break
    
    my_nodes.sort(key=lambda v: [graph.node[v].troops, -min_around_enemy(v, graph, team)])

    for v in my_nodes:
        graph.node[v].adj.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)
        for u in graph.node[v].adj:
            if graph.node[u].owner not in [-1, team.id]:
                if graph.node[v].troops > graph.node[v].troops + graph.node[v].fort_troops and graph.node[v].troops + graph.node[v].fort_troops >= FIRST_REQUIRED_TROOP:
                    print(game.attack(v, u, 1.5, 0.5))
                    graph.update(game)
    
    game.next_state()

    # ----- Move troops -----
    my_nodes.sort(key=lambda v: graph.node[v].troops)

    destination = my_nodes[0]
    reachable = game.get_reachable(destination)['reachable']
    reachable.sort(key=lambda v: graph.node[v].troops, reverse=True)
    source = reachable[0]
    print(game.move_troop(source, destination, (graph.node[source].troops - graph.node[destination].troops)//2))


    game.next_state()

    # ----- Fort -----
    my_borjs.sort(key=lambda v: graph.node[v].score, reverse=True)

    selected_borj = my_borjs[0]
    if not flag:
        if graph.node[selected_borj].troops > 4:
            print(game.fort(selected_borj, 4))
            flag = True

    game.next_state() # Go next turn