import pygame

class Trainer:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.badges = 0
        self.pokemon = []


        # #Battle image
        # front = pygame.image.load(f'assets/images/pokemon/front-{"shiny" if self.shiny else "normal"}/{self.pokedex_number}{self.name.lower()}.png').convert_alpha()
        # self.battle_front = pygame.transform.scale(front, (224, 224))
        # self.front_rect = self.battle_front.get_rect()
        # self.front_rect.center = (496, 112)