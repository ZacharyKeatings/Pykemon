import pygame, os
from states.state import State

class Battle(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.background_img = pygame.image.load(os.path.join(self.game.assets_dir, "battle1.png"))

    def update(self, delta_time, actions):
        pass

    def render(self, display):
        display.blit(self.background_img, (0,0))