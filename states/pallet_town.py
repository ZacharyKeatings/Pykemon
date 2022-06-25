import pygame, os
from states.state import State

class Pallet_Town(State):
    def __init__(self, game):
        super().__init__(game)
        self.background_img = pygame.image.load(os.path.join(self.game.assets_dir, "pallet_town.png"))

    def update(self, delta_time, actions):
        pass

    def render(self, display):
        display.blit(self.background_img, (0,0))
    