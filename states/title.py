from states.state import State
from states.battle import Battle
from states.pallet_town import Pallet_Town
from states.pause_menu import PauseMenu

class Title(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, delta_time, actions):
        if actions["select"]:
            new_state = Battle(self.game)
            new_state.enter_state()
        self.game.reset_keys()

    def render(self, display):
        display.fill((248,248,248))
        self.game.draw_text(display, "Pykemon", (0,0,0), self.game.GAME_W*0.35, self.game.GAME_H/2)