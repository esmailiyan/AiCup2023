import random
from src.game import Game
from structure import State, Team, Graph
from utils import log

flag = False
team = Team()
graph = Graph()

def initializer(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    '''
        Tasks: 
            1. Write Algorithm
    '''


def turn(game: Game):
    team.update(game)
    graph.update(game)
    # ----- Write your code here -----
    '''
        Tasks: 
            1. Write Algorithm
    '''