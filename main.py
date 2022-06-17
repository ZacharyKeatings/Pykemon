from pokemon import Pokemon
from battle import Battle
import pygame

pygame.init()


WIDTH = 640
HEIGHT = 576
SCALE = 4
CLOCK = pygame.time.Clock()
FPS = 2

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pykemon")
background = pygame.image.load('assets/battle1.png').convert_alpha()
scaled_background = pygame.transform.scale(background, (background.get_width() * SCALE, background.get_height() * SCALE))
font = pygame.font.Font('assets/font/pokemon_generation_1.ttf', 34)

#colours
BLACK = (0, 0, 0)
RED = (248, 0, 0)
GREEN = (0, 184, 0)
BLUE = (32, 136, 248)
YELLOW = (248, 168, 0)


charmander = Pokemon("Charmander", ['Scratch', 'Tail Whip'])
bulbasaur = Pokemon("Bulbasaur", ['Scratch', 'Tail Whip'])
squirtle = Pokemon("Squirtle", ['Scratch', 'Tail Whip'])
ivysaur = Pokemon("Venusaur", ['Scratch', 'Tail Whip'])

ivysaur.curr_xp = 96
ivysaur.set_level()
ivysaur.level_up()
ivysaur.currentHP = ivysaur.maxHP

# xp_needed = ivysaur.next_level_xp - ivysaur.current_level_xp
# xp_in_level = ivysaur.current_level_xp - ivysaur.curr_xp
# to_next_level = xp_in_level / xp_needed
# print(xp_needed)
# print(xp_in_level)
# print(to_next_level)


def draw_bg():
    window.blit(scaled_background, (0, 0))

def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    window.blit(img, (x, y))

def draw_pokemon_front(pokemon):
    window.blit(pokemon.battle_front, pokemon.front_rect)

def draw_pokemon_back(pokemon):
    window.blit(pokemon.battle_back, pokemon.back_rect)

def draw_hp_bar(pokemon, x, y):
    def hp_bar_colour(pokemon):
        ratio = pokemon.currentHP / pokemon.maxHP
        if ratio > 0.5625:
            return GREEN
        elif 0.5625 >= ratio > 0.29167:
            return YELLOW
        elif ratio <= 0.29167:
            return RED

    def hp_bar_length(pokemon):
        ratio = pokemon.currentHP / pokemon.maxHP
        length = ratio * (48 * SCALE)
        return int(length)

    pygame.draw.rect(window, hp_bar_colour(pokemon), (x, y, hp_bar_length(pokemon), 2 * SCALE))

def draw_xp_bar(pokemon, x, y):
    def xp_bar_length(pokemon):
        ratio = (pokemon.curr_xp - pokemon.current_level_xp) / (pokemon.next_level_xp - pokemon.current_level_xp)
        length = ratio * (64 * SCALE)
        return int(length)

    pygame.draw.rect(window, BLUE, (x, y, xp_bar_length(pokemon), 2 * SCALE))

running = True
while running:

    CLOCK.tick(FPS)

    #All game code here
    draw_bg()

    #foe
    draw_text(ivysaur.name.upper(), font, BLACK, 35, -3)
    draw_text(str(ivysaur.level), font, BLACK, 227, 27)
    draw_hp_bar(ivysaur, 128, 75)
    draw_pokemon_front(ivysaur)

    #friend
    draw_text(ivysaur.name.upper(), font, BLACK, 320, 220)
    draw_text(f"{str(ivysaur.level)}", font, BLACK, 482, 250)
    draw_hp_bar(ivysaur, 384, 300)
    draw_xp_bar(ivysaur, 320, 365)
    draw_text(f"{str(ivysaur.currentHP)}/{str(ivysaur.maxHP)}", font, BLACK, 385, 315)
    draw_pokemon_back(ivysaur)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()



# attacker, defender = charmander, bulbasaur
# fight = Battle(attacker, defender)
# fight.battle_loop() pkmn

