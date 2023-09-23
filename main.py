from math import ceil
from src.game import Game
from structure import State, Team, Graph
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
    # print(f"\initializer:{ceil(team.turn_number/3)}\n")

    REQUIRED_NODE_TROOP = 3
    REQUIRED_BORJ_TROOP = 6

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]
    free_nodes = [v for v in nodes if graph.node[v].owner == -1]

    borjs = [v[0] for v in graph.borj]

    my_nodes.sort(key=lambda v: [-graph.node[v].troops, graph.node[v].score, max_around_enemy(v, graph, team)], reverse=True)
    free_nodes.sort(key=lambda v: [int(bool(sum_around_borj(v, graph))), count_around_freind(v, graph, team), graph.node[v].score], reverse=True)
    borjs.sort(key=lambda v: [graph.node[v].score, -graph.node[v].degree], reverse=True)

    # ----- Start algorithm -----

    # Selecting one node
    for v in borjs:
        if graph.node[v].owner == -1:
            response = game.put_one_troop(v)
            print(response)
            game.next_state()
            return

    for v in free_nodes:
        if sum_around_borj(v, graph) > 0:
            response = game.put_one_troop(v)
            print(response)
            game.next_state()
            return

    # Strengthening my nodes
    for v in my_nodes:
        if graph.node[v].is_strategic:
            if graph.node[v].troops < REQUIRED_BORJ_TROOP:
                response = game.put_one_troop(v)
                print(response)
                game.next_state()
                return
        else: 
            if graph.node[v].troops < REQUIRED_NODE_TROOP:
                response = game.put_one_troop(v)
                print(response)
                game.next_state()
                return
    
    for v in my_nodes:
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
    SECOND_REQUIRED_TROOP = 5
    REQUIRED_BORJ_TROOP = 10
    MAX_BORJ_TROOP = 20

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

    try:
        for v in my_borjs: # Upgrade my borjs to required troop
            if graph.node[v].troops + graph.node[v].fort_troops < REQUIRED_BORJ_TROOP:
                if put_for_defense > 0: 
                    print(game.put_troop(v, min(2, put_for_defense)))
                    put_for_defense -= min(2, put_for_defense)
    except Exception as e:
        print(f"ERROR in part 1: {e}")

    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)

    try:
        for v in my_nodes: # Upgrade my nodes to first required troop
            if not graph.node[v].is_strategic: # Ignore the borjs
                if graph.node[v].troops < FIRST_REQUIRED_TROOP:
                    if put_for_defense > 0:
                        print(game.put_troop(v, min(1, put_for_defense)))
                        put_for_defense -= min(1, put_for_defense)
    except Exception as e:
        print(f"ERROR in part 2: {e}")

    my_borjs.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)

    try:
        for v in my_borjs: # Upgrade my borjs to max enemy troop
            if graph.node[v].troops + graph.node[v].fort_troops < MAX_BORJ_TROOP:
                if graph.node[v].troops + graph.node[v].fort_troops < max_around_enemy(v, graph, team):
                    if put_for_defense > 0:
                        print(game.put_troop(v, min(2, put_for_defense)))
                        put_for_defense -= min(2, put_for_defense)
    except Exception as e:
        print(f"ERROR in part 3: {e}")

    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)

    try:
        for v in my_nodes: # Upgrade my nodes to second required troop
            if not graph.node[v].is_strategic: # Ignore the borjs
                if graph.node[v].troops < SECOND_REQUIRED_TROOP:
                    if put_for_defense > 0:
                        print(game.put_troop(v, min(1, put_for_defense)))
                        put_for_defense -= min(1, put_for_defense)
    except Exception as e:
        print(f"ERROR in part 4: {e}")

    my_nodes.sort(key=lambda v: [int(bool(sum_around_borj(v, graph))), graph.node[v].troops, -min_around_enemy(v, graph, team)], reverse=True)

    try:
        for v in my_borjs:
            if graph.node[v].troops + graph.node[v].fort_troops < REQUIRED_BORJ_TROOP:
                if put_for_attack > 0:
                    print(game.put_troop(v, put_for_attack))
                    put_for_attack = 0
                
        for v in my_nodes: # Upgrade one of my nodes to attack
            if not graph.node[v].is_strategic:
                if put_for_attack > 0:
                    print(game.put_troop(v, put_for_attack))
                    put_for_attack = 0
    except Exception as e:
        print(f"ERROR in part 5: {e}")

    game.next_state()

    # ----- Attack -----
    graph.update(game)

    try:
        attack_options = []
        for v in my_nodes:
            for u in graph.node[v].adj:
                if u in enemy_neighbors:
                    attack_options.append((v, u))

        attack_options.sort(key=lambda x: [graph.node[x[0]].troops, graph.node[x[0]].troops / (graph.node[x[1]].troops + graph.node[x[1]].fort_troops)], reverse=True)

        for (v, u) in attack_options:
            if graph.node[v].is_strategic:
                if graph.node[v].troops + graph.node[v].fort_troops >= REQUIRED_BORJ_TROOP:
                    if graph.node[u].owner != team.id:
                        print(game.attack(v, u, 3, 0.2))
                        graph.update(game)
            else:
                if graph.node[v].troops + graph.node[v].fort_troops >= FIRST_REQUIRED_TROOP:
                    if graph.node[u].owner != team.id:
                        print(game.attack(v, u, 1.0001, 0.5))
                        graph.update(game)
    except Exception as e:
        print(f"ERROR in part 6&7: {e}")

    game.next_state()

    # ----- Move troops -----
    graph.update(game)

    try:
        moved = False
        my_borjs.sort(key=lambda v: graph.node[v].troops)
        my_nodes.sort(key=lambda v: graph.node[v].troops)

        move_options = []
        for v in my_borjs:
            if graph.node[v].troops + graph.node[v].fort_troops < REQUIRED_BORJ_TROOP:
                move_options.append(v)
        for v in my_nodes:
            if graph.node[v].troops < FIRST_REQUIRED_TROOP:
                move_options.append(v)

        for v in move_options:
            reachable = game.get_reachable(v)['reachable']
            reachable.sort(key=lambda v: [-int(graph.node[v].is_strategic), graph.node[v].troops], reverse=True)
            for u in reachable:
                if graph.node[u].troops - graph.node[v].troops > 2:
                    if not moved:
                        print(game.move_troop(u, v, (graph.node[u].troops - graph.node[v].troops)//2))
                        moved = True
                        graph.update(game)
    except Exception as e:
        print(f"ERROR in part 8: {e}")

    game.next_state()

    # ----- Fort -----
    graph.update(game)

    my_borjs.sort(key=lambda v: graph.node[v].troops, reverse=True)
    
    try:
        if not flag and len(my_borjs) != 0:
            v = my_borjs[0]
            if graph.node[v].troops > 4:
                print(game.fort(v, 4))
                flag = True
    except Exception as e:
        print(f"ERROR in part 9: {e}")

    game.next_state() # Go next turn