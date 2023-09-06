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
            1. Write algorithm of select strategic nodes
            2. Write algorithm of initial location of troops
    '''


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