from src.game import Game
from structure import State, Team, Graph

from actions.put_one_troop import put_one_troop
from actions.put_troop import put_troop
from actions.attack import attack
from actions.move_troop import move_troop
from actions.fort import fort

flag = False
team = Team()
graph = Graph()

def initializer(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Start here -----
    put_one_troop(game, graph, team)
    game.next_state()

def turn(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Start here -----
    global flag
    # ----- Put troop -----
    put_troop(game, graph, team)
    game.next_state()
    # ----- Attack -----
    graph.update(game)
    attack(game, graph, team)
    game.next_state()
    # ----- Move troops -----
    graph.update(game)
    move_troop(game, graph, team)
    game.next_state()
    # ----- Fort -----
    graph.update(game)
    if not flag:
        flag = fort(game, graph, team)
    game.next_state()