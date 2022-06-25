import pygame, os
from states.state import State
from states.pause_menu import PauseMenu
from pokemon import Pokemon
from move import Move

class Battle(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.background_img = pygame.image.load(os.path.join(self.game.assets_dir, "battle1.png"))
        self.scaled_background_img = pygame.transform.scale(self.background_img, (self.background_img.get_width() * self.game.SCALE, self.background_img.get_height() * self.game.SCALE))

        #Main Menu
        self.main_battle_menu = pygame.image.load(os.path.join(self.game.assets_dir, "main_battle_menu.png"))
        self.scaled_main_battle_menu = pygame.transform.scale(self.main_battle_menu, (self.main_battle_menu.get_width() * self.game.SCALE, self.main_battle_menu.get_height() * self.game.SCALE))
        self.scaled_main_battle_menu_rect = self.scaled_main_battle_menu.get_rect()
        self.scaled_main_battle_menu_rect.x, self.scaled_main_battle_menu_rect.y = self.game.GAME_W - self.scaled_main_battle_menu.get_width(), self.game.GAME_H - self.scaled_main_battle_menu.get_height()

        #Move Menu
        self.battle_move_menu = pygame.image.load(os.path.join(self.game.assets_dir, "battle_move_menu.png"))
        self.scaled_battle_move_menu = pygame.transform.scale(self.battle_move_menu, (self.battle_move_menu.get_width() * self.game.SCALE, self.battle_move_menu.get_height() * self.game.SCALE))
        self.scaled_battle_move_menu_rect = self.scaled_battle_move_menu.get_rect()
        self.scaled_battle_move_menu_rect.x, self.scaled_battle_move_menu_rect.y = self.game.GAME_W - self.scaled_battle_move_menu.get_width(), self.game.GAME_H - self.scaled_battle_move_menu.get_height()

        #State data
        self.main_battle_menu_options = {0: "Fight", 1: "Pack", 2: "Pkmn", 3: "Run"}
        self.menu_state = 'main'
        self.cursor_on_move = 0
        self.selected_move = None
        self.index = 0

        #Cursor Data
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "cursor-filled.png"))
        self.scaled_cursor_img = pygame.transform.scale(self.cursor_img, (self.cursor_img.get_width() * self.game.SCALE, self.cursor_img.get_height() * self.game.SCALE))
        self.cursor_rect = self.scaled_cursor_img.get_rect()
        self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

        #!Test Pokemon
        self.bulbasaur = Pokemon("Bulbasaur")
        self.bulbasaur.curr_xp = 2000
        self.bulbasaur.set_level()
        self.bulbasaur.level_up()
        self.bulbasaur.set_moves()
        self.bulbasaur.currentHP = self.bulbasaur.maxHP

        # ivysaur = Pokemon("Ivysaur")
        # ivysaur.curr_xp = 3000
        # ivysaur.set_level()
        # ivysaur.level_up()
        # ivysaur.set_moves()
        # ivysaur.currentHP = ivysaur.maxHP

        # venusaur = Pokemon("Venusaur")
        # venusaur.curr_xp = 1600
        # venusaur.set_level()
        # venusaur.level_up()
        # venusaur.set_moves()
        # venusaur.currentHP = venusaur.maxHP
        #!-------------------

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions['select']:
            if self.index == 0: #fight
                self.menu_state = 'fight'
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_battle_move_menu_rect.x + (40 * self.game.SCALE), self.scaled_battle_move_menu_rect.y + (38 * self.game.SCALE)
            if self.index == 1: #pack
                pass
            if self.index == 2: #pkmn
                pass
            if self.index == 3: #run
                self.game.playing = False
                self.game.running = False
        if actions['back']:
            self.menu_state = 'main'
            self.index = 0
            self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)
        self.game.reset_keys()

    def render(self, display):
        display.blit(self.scaled_background_img, (0,0))
        display.blit(self.scaled_main_battle_menu, self.scaled_main_battle_menu_rect)
        if self.menu_state == 'main':
            display.blit(self.scaled_cursor_img, self.cursor_rect)
        if self.menu_state == 'fight':
            display.blit(self.scaled_battle_move_menu, self.scaled_battle_move_menu_rect)
            display.blit(self.scaled_cursor_img, self.cursor_rect)
            num_moves = len(self.bulbasaur.moves)
            for index, move in enumerate(self.bulbasaur.moves):
                self.game.draw_text(display, move.upper(), self.game.BLACK, self.scaled_battle_move_menu_rect.x + (48*self.game.SCALE), self.scaled_battle_move_menu_rect.y + (37*self.game.SCALE) + (32*index))
            for blank_move in range(len(self.bulbasaur.moves), 4):
                self.game.draw_text(display, "-", self.game.BLACK, self.scaled_battle_move_menu_rect.x + (48*self.game.SCALE), self.scaled_battle_move_menu_rect.y + (37*self.game.SCALE) + (32*blank_move))
            self.game.draw_text(display, Move(self.bulbasaur.moves[self.cursor_on_move]).get_type().upper(), self.game.BLACK, self.scaled_battle_move_menu_rect.x + (16*self.game.SCALE), self.scaled_battle_move_menu_rect.y + (13*self.game.SCALE))

    def update_cursor(self, actions):
        if self.menu_state == 'main':
            if actions['down']:
                if self.index == 0:
                    self.index = 2
                    self.cursor_rect.y = self.cursor_rect.y + (16 * self.game.SCALE)
                if self.index == 1:
                    self.index = 3
                    self.cursor_rect.y = self.cursor_rect.y + (16 * self.game.SCALE)
            if actions['up']:
                if self.index == 2:
                    self.index = 0
                    self.cursor_rect.y = self.cursor_rect.y - (16 * self.game.SCALE)
                if self.index == 3:
                    self.index = 1
                    self.cursor_rect.y = self.cursor_rect.y - (16 * self.game.SCALE)
            if actions['left']:
                if self.index == 1:
                    self.index = 0
                    self.cursor_rect.x = self.cursor_rect.x - (48 * self.game.SCALE)
                if self.index == 3:
                    self.index = 2
                    self.cursor_rect.x = self.cursor_rect.x - (48 * self.game.SCALE)
            if actions['right']:
                if self.index == 0:
                    self.index = 1
                    self.cursor_rect.x = self.cursor_rect.x + (48 * self.game.SCALE)
                if self.index == 2:
                    self.index = 3
                    self.cursor_rect.x = self.cursor_rect.x + (48 * self.game.SCALE)
        if self.menu_state == 'fight':
            if actions['down']:
                if self.index < len(self.bulbasaur.moves)-1:
                    self.index += 1
                    self.cursor_on_move += 1
                    self.cursor_rect.y = self.cursor_rect.y + (8 * self.game.SCALE)
            if actions['up']:
                if self.index > 0:
                    self.index -= 1
                    self.cursor_on_move -= 1
                    self.cursor_rect.y = self.cursor_rect.y - (8 * self.game.SCALE)
