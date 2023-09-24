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

    # ----- Selecting one node -----
    for v in borjs:
        if graph.node[v].owner == -1:
            print(game.put_one_troop(v))
            game.next_state()
            return

    for v in free_nodes:
        if sum_around_borj(v, graph) > 0:
            print(game.put_one_troop(v))
            game.next_state()
            return

    # ----- Strengthening my nodes -----
    for v in my_nodes:
        if graph.node[v].is_strategic:
            if graph.node[v].troops < REQUIRED_BORJ_TROOP:
                print(game.put_one_troop(v))
                game.next_state()
                return
        else: 
            if graph.node[v].troops < REQUIRED_NODE_TROOP:
                print(game.put_one_troop(v))
                game.next_state()
                return
    
    for v in my_nodes:
        print(game.put_one_troop(v))
        game.next_state()
        return

def turn(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    turn = ceil(team.turn_number/3)-35
    # print(f"\nturn:{turn}\n")

    global flag
    REQUIRED_NODE_TROOP = 5
    MAX_NODE_TROOP = 8
    REQUIRED_BORJ_TROOP = 10
    MAX_BORJ_TROOP = 20

    nodes = graph.nodes
    my_nodes = [v for v in nodes if graph.node[v].owner == team.id]
    free_nodes = [v for v in nodes if graph.node[v].owner == -1]
    enemy_nodes = [v for v in nodes if graph.node[v].owner not in [-1, team.id]]

    borjs = [v[0] for v in graph.borj]
    my_borjs = [v for v in borjs if v in my_nodes]

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
    my_borjs.sort(key=lambda v: [graph.node[v].score, -(graph.node[v].troops + graph.node[v].fort_troops)], reverse=True)

    for v in my_borjs: # Upgrade my borjs to required troop
        if (graph.node[v].troops + graph.node[v].fort_troops) < REQUIRED_BORJ_TROOP:
            if put_for_defense > 0: 
                print(game.put_troop(v, min(2, put_for_defense)))
                put_for_defense -= min(2, put_for_defense)

    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)

    for v in my_nodes: # Upgrade my nodes to required troop
        if not graph.node[v].is_strategic: # Ignore the borjs
            if graph.node[v].troops < REQUIRED_NODE_TROOP:
                if put_for_defense > 0:
                    print(game.put_troop(v, 1))
                    put_for_defense -= 1

    my_borjs.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)

    for v in my_borjs: # Upgrade my borjs to max enemy troop
        if (graph.node[v].troops + graph.node[v].fort_troops) < MAX_BORJ_TROOP:
            if (graph.node[v].troops + graph.node[v].fort_troops) < max_around_enemy(v, graph, team):
                if put_for_defense > 0:
                    print(game.put_troop(v, min(2, put_for_defense)))
                    put_for_defense -= min(2, put_for_defense)

    my_nodes.sort(key=lambda v: [sum_around_borj(v, graph), -graph.node[v].troops], reverse=True)

    for v in my_nodes: # Upgrade my nodes to max troop
        if not graph.node[v].is_strategic: # Ignore the borjs
            if graph.node[v].troops < MAX_NODE_TROOP:
                if put_for_defense > 0:
                    print(game.put_troop(v, 1))
                    put_for_defense -= 1

    if put_for_defense > 0: # Add troops for attack
        put_for_attack += put_for_defense
        put_for_defense = 0

    # Be ready for attack!
    my_nodes.sort(key=lambda v: graph.node[v].troops, reverse=True)
    my_borjs.sort(key=lambda v: graph.node[v].troops + graph.node[v].fort_troops)

    for v in my_borjs: # Defend our weak borjs
        if (graph.node[v].troops + graph.node[v].fort_troops) < REQUIRED_BORJ_TROOP:
            if put_for_attack > 0:
                print(game.put_troop(v, put_for_attack))
                put_for_attack = 0
            
    for v in my_nodes: # Upgrade one of my nodes to attack
        if not graph.node[v].is_strategic:
            if put_for_attack > 0:
                print(game.put_troop(v, put_for_attack))
                put_for_attack = 0

    graph.update(game)
    game.next_state()

    # ----- Attack -----
    attack_options = []
    for v in my_nodes:
        for u in graph.node[v].adj:
            if u in enemy_neighbors:
                attack_options.append((v, u))

    attack_options.sort(key=lambda x: [graph.node[x[0]].troops / (graph.node[x[1]].troops + graph.node[x[1]].fort_troops), graph.node[x[0]].troops], reverse=True)

    mark = [False for v in nodes]
    selected_attack = []

    for (v, u) in attack_options:
        if not mark[v] and not mark[u]:
            selected_attack.append((v, u))
            mark[v] = mark[u] = True

    for (v, u) in selected_attack:
        if graph.node[v].is_strategic:
            if (graph.node[v].troops + graph.node[v].fort_troops) > max_around_enemy(v, graph, team):
                if graph.node[u].owner != team.id:
                    print(game.attack(v, u, 2.5, 0.2))
        else:
            if graph.node[v].troops >= REQUIRED_NODE_TROOP:
                if graph.node[u].owner != team.id:
                    print(game.attack(v, u, 1.1, 0.4))
    
    graph.update(game)
    game.next_state()

    # ----- Move troops -----
    my_borjs.sort(key=lambda v: graph.node[v].troops)
    move = False    

    for v in my_borjs:
        if not move:
            if (graph.node[v].troops + graph.node[v].fort_troops) < REQUIRED_BORJ_TROOP:
                reachable = game.get_reachable(v)['reachable']
                reachable.sort(key=lambda v: [-int(graph.node[v].is_strategic), graph.node[v].troops], reverse=True)
                for u in reachable:
                    if graph.node[v].troops - graph.node[u].troops > 2:
                        print(game.move_troop(v, u, (graph.node[v].troops - graph.node[u].troops)//2))
                        move = True
                        break

    graph.update(game)
    game.next_state()

    # ----- Fort -----
    my_borjs.sort(key=lambda v: graph.node[v].troops)
    
    for v in my_borjs:
        if not flag:
            if graph.node[v].troops > 5:
                print(game.fort(v, 5))
                flag = True
                
    game.next_state()