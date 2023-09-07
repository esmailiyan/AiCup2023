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
        self.degree = 0
        self.is_strategic = False
        self.score = 0       
        self.troops = 0
        self.fort_troops = 0

    def __str__(self):
        # ----- Output as string -----
        return f"Node:{self.id}\n- owner:{self.owner}\n- troops:{self.troops}\n"


# class Situation():
#     def __init__(self, attacker_damage:int, defendant_damages:int, probability:float):
#         self.Attacker_damage = attacker_damage
#         self.Defendant_damages = defendant_damages
#         self.Probability = probability

#     def __str__(self) -> str:
#         return f"Attacker damage:{self.Attacker_damage:<3} | Defendant damages:{self.Defendant_damages:<3} | Probability:{self.Probability:.4f}"

class Team():
    def __init__(self):
        self.id = 0
        self.free_troops = 0
        self.state = 0
        self.turn_number = 0

    def __str__(self):
        # ----- Output as string -----
        return f"Team:\n- id:{self.id}\n- state:{self.state}\n- turn_number:{self.turn_number}\n- free_troops:{self.free_troops}\n"

    def update(self, game:Game):
        # ----- Updating data -----
        self.id = game.get_player_id()['player_id']
        self.free_troops = game.get_number_of_troops_to_put()['number_of_troops']
        self.state = game.get_state()['state']
        self.turn_number = game.get_turn_number()['turn_number']


class Graph(Node):
    def __init__(self):
        self.node = []
        self.nodes = []
        self.borj = []
    
    def __str__(self):
        # ----- Output as string -----
        return f"Graph:\n- number of nodes:{len(self.nodes)}\n- strategics:{self.borj}\n"

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
        self.node = [Node() for i in range(len(_nodes))]
        self.borj = list(zip(_strategic, _score))
        for i in _nodes:
            self.node[i].id = i
            self.node[i].owner = _owner[str(i)]
            self.node[i].adj = _adj[str(i)]
            self.node[i].degree = len(_adj[str(i)])
            self.node[i].troops = _troops[str(i)]
            self.node[i].fort_troops = _fort_troops[str(i)]
        for (i, score) in self.borj:
            self.node[i].is_strategic = True
            self.node[i].score = score