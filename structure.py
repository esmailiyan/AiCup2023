from src.game import Game

class State:
    PUT_TROOP = 1
    ATTACK = 2
    MOVE_TROOP = 3
    FORT = 4


class Node():
    def __init__(self):
        self.id = 0
        self.owner = -1 
        self.adj = []
        self.is_strategic = False
        self.score = 0       
        self.troops = 0
        self.fort_troops = 0

    def __str__(self):
        # ----- Output as string -----
        return f"ID:{self.id} - Owner:{self.owner} - Troops:{self.troops}"


class Team():
    def __init__(self):
        self.id = 0
        self.free_troops = 0
        self.state = 0
        self.turn_number = 0

    def __str__(self):
        # ----- Output as string -----
        return f"id:{self.id} - turn_number:{self.turn_number} - State:{self.state} - free_troops:{self.free_troops}"

    def update(self, game:Game):
        # ----- Updating data -----
        self.id = game.get_player_id()['player_id']
        self.free_troops = game.get_number_of_troops_to_put()['number_of_troops']
        self.state = game.get_state()['state']
        self.turn_number = game.get_turn_number()['turn_number']


class Graph(Node):
    def __init__(self):
        MAXNODE = 107
        self.node = [Node() for i in range(MAXNODE)]
        self.nodes = []
        self.strategic_nodes = []
    
    def __str__(self):
        # ----- Output as string -----
        return f" Number of nodes:{len(self.nodes)} - Strategics:{self.strategic_nodes}"

    def update(self, game:Game):
        # ----- Get new data -----
        _adj = game.get_adj()
        _nodes = [int(v) for v in _adj.keys()]
        _owner = game.get_owners()
        _strategic = game.get_strategic_nodes()['strategic_nodes']
        _score = game.get_strategic_nodes()['score']
        _troops = game.get_number_of_troops()
        _fort_troops = game.get_number_of_fort_troops()
        # ----- Update data -----
        self.nodes = _nodes
        self.strategic_nodes = list(zip(_strategic, _score))
        for i in _nodes:
            self.node[i].id = i
            self.node[i].owner = _owner[str(i)]
            self.node[i].adj = _adj[str(i)]
            self.node[i].troops = _troops[str(i)]
            self.node[i].fort_troops = _fort_troops[str(i)]
        for (i, score) in self.strategic_nodes:
            self.node[i].is_strategic = True
            self.node[i].score = score
        # ----- Custom ordering data -----
        '''
            Tasks: 
                1. sorting strategic_nodes with specified formula
                2. add my_node
        '''