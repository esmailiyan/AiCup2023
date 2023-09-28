from src.game import Game
from structure import State, Team, Graph

from actions.put_one_troop import put_one_troop
from actions.put_troop import put_troop
from actions.attack import attack
from actions.move_troop import move_troop
from actions.fort import fort

forted = False
do_fort = False
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
    global forted
    global do_fort
    # ----- Put troop -----
    put_troop(game, graph, team)
    game.next_state()
    # ----- Attack -----
    graph.update(game)
    do_fort = attack(game, graph, team)
    game.next_state()
    # ----- Move troops -----
    graph.update(game)
    move_troop(game, graph, team)
    game.next_state()
    # ----- Fort -----
    graph.update(game)
    if not forted:
        if do_fort:
            forted = fort(game, graph, team)
    game.next_state()