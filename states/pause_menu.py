import pygame, os
from states.state import State

class PauseMenu(State):
    def __init__(self, game):
        self.game = game
        super().__init__(game)
        #Set the menu
        self.menu_img = pygame.image.load(os.path.join(self.game.assets_dir, "Pause_Menu.png"))
        self.menu_rect = self.menu_img.get_rect()
        self.menu_rect.center = (self.game.GAME_W*.85, self.game.GAME_H*.4)

    def update(self, delta_time, actions):
        if actions["back"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self,display):
        self.prev_state.render(display)
        display.blit(self.menu_img, self.menu_rect)
