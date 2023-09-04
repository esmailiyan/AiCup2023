from src.game import Game

class State:
    PUT_TROOP = 1
    ATTACK = 2
    MOVE_TROOP = 3
    FORT = 4

class Data():
    def __init__(self, game:Game):
        # ----- Structures -----
        self.id = 0
        self.free_troops = 0
        self.state = 0
        self.turn_number = 0
        # ----- First update -----
        self.update(self)

    def update(self):
        # ----- Updating data -----
        self.id = game.get_player_id()['player_id']
        self.free_troops = game.get_number_of_troops_to_put()['number_of_troops']
        self.state = game.get_state()['state']
        self.turn_number = game.get_turn_number()['turn_number']