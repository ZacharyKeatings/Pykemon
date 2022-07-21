import pygame, os
from states.state import State
import random
#!---Debugging - can remove
from pokemon import Pokemon
#!-------------------------

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
        # current cursor position
        self.index = 0
        #Which move did each Pokemon select
        self.selected_friend_move = None
        self.selected_foe_move = None
        #Who goes first, who goes second
        self.first_move = None
        self.second_move = None
        #Who already made a move?
        self.friend_moved = False
        self.foe_moved = False

        #!------
        # When a move is used with a status effect, pokemon status flag set to true
        #! set self.status_counter to num of turns status is active
        #! at beginning of each new turn, if status counter is > 0, do something
        #! then reduce counter by 1 and proceed with battle

        #Cursor Data
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "cursor-filled.png"))
        self.scaled_cursor_img = pygame.transform.scale(self.cursor_img, (self.cursor_img.get_width() * self.game.SCALE, self.cursor_img.get_height() * self.game.SCALE))
        self.cursor_rect = self.scaled_cursor_img.get_rect()
        self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

        #!Test Pokemon--------
        self.friend = Pokemon("Bulbasaur")
        self.friend.curr_xp = 30000
        self.friend.transition_xp = 30000
        self.friend.set_level()
        self.friend.level_up()
        self.friend.set_moves()
        self.friend.currentHP = self.friend.maxHP

        self.foe = Pokemon("Ivysaur")
        self.foe.curr_xp = 3000
        self.foe.set_level()
        self.foe.level_up()
        self.foe.set_moves()
        self.foe.maxHP = 200
        self.foe.currentHP = self.foe.maxHP

        # self.venusaur = Pokemon("Venusaur")
        # self.venusaur.curr_xp = 1600
        # self.venusaur.set_level()
        # self.venusaur.level_up()
        # self.venusaur.set_moves()
        # self.venusaur.currentHP = self.venusaur.maxHP
        #!-------------------

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions['select']:
            if self.menu_state == 'main':
                if self.index == 0: #fight
                    if self.friend.is_fainted():
                        self.menu_state = 'friend fainted'
                    elif self.foe.is_fainted():
                        self.menu_state = 'foe fainted'
                    else:
                        self.menu_state = 'fight'
                        self.cursor_rect.x, self.cursor_rect.y = self.scaled_battle_move_menu_rect.x + (40 * self.game.SCALE), self.scaled_battle_move_menu_rect.y + (38 * self.game.SCALE)
                if self.index == 1: #pack
                    pass
                if self.index == 2: #pkmn
                    pass
                if self.index == 3: #run
                    self.menu_state = 'escape'

            elif self.menu_state == 'fight':
                self.new_turn()
                self.set_moves()

                if self.selected_friend_move.curr_pp <= 0:
                    self.menu_state = 'no pp left'
                else:
                    self.move_order()

                    if self.first_move == self.friend:
                        if self.friend.status_effect:
                            if self.friend.flinch:
                                self.friend.flinch = False
                                self.foe.status_effect = False
                                self.friend_moved = True
                                self.menu_state = 'foe used move'
                            elif self.friend.paralyzed:
                                rand_num = random.randint(0, 3)
                                if rand_num == 0:
                                    self.friend_moved = True
                                    self.menu_state = 'friend paralyzed'
                                else:
                                    self.menu_state = 'friend used move'
                            elif self.friend.burned:
                                self.menu_state = 'friend used move'
                            elif self.friend.poisoned:
                                self.menu_state = 'friend used move'
                            elif self.friend.badly_poisoned:
                                self.menu_state = 'friend used move'
                        else:
                            self.menu_state = 'friend used move'

                    if self.first_move == self.foe:
                        if self.foe.status_effect:
                            if self.foe.flinch:
                                self.foe.flinch = False
                                self.foe.status_effect = False
                                self.foe_moved = True
                                self.menu_state = 'friend used move'
                            elif self.foe.paralyzed:
                                rand_num = random.randint(0, 3)
                                if rand_num == 0:
                                    self.foe_moved = True
                                    self.menu_state = 'foe paralyzed'
                                else:
                                    self.menu_state = 'foe used move'
                            elif self.foe.burned:
                                self.menu_state = 'foe used move'
                            elif self.foe.poisoned:
                                self.menu_state = 'foe used move'
                            elif self.foe.badly_poisoned:
                                self.menu_state = 'foe used move'
                        else:
                            self.menu_state = 'foe used move'

            elif self.menu_state == 'friend used move':
                # switch to critical hit, effectiveness, foe move or move menu
                self.selected_friend_move.use(self.friend, self.foe)
                self.selected_friend_move.curr_pp -= 1
                self.friend_moved = True

                if self.selected_friend_move.move_missed == True:
                    self.menu_state = 'friend missed'
                else:
                    if self.selected_friend_move.landed_crit:
                        self.menu_state = 'friend critical hit'
                    elif self.selected_friend_move.effectiveness(self.foe) != 1:
                        self.menu_state = 'friend effectiveness'
                    elif self.foe.is_fainted():
                        self.menu_state = 'foe fainted'
                    elif self.foe.flinch:
                        if self.foe_moved is False:
                            self.foe.flinch = False
                            self.foe.status_effect = False
                            self.foe_moved = True
                            self.menu_state = "foe flinched"
                        else:
                            self.menu_state = "foe flinched"
                    elif self.selected_friend_move.applied_poison:
                        self.menu_state = 'foe poisoned'
                    elif self.selected_friend_move.applied_burn:
                        self.menu_state = 'foe burned'
                    elif self.friend.status_effect:
                        if self.friend.poisoned:
                            self.menu_state = 'friend hurt by poison'
                        elif self.friend.badly_poisoned:
                            self.menu_state = 'friend hurt by poison'
                        elif self.friend.burned:
                            self.menu_state = 'friend hurt by burn'
                    elif self.foe_moved is False:
                        if self.foe.paralyzed:
                            rand_num = random.randint(0, 3)
                            if rand_num == 0:
                                self.foe_moved = True
                                self.menu_state = 'foe paralyzed'
                            else:
                                self.menu_state = 'foe used move'
                        else:
                            self.menu_state = 'foe used move'
                    else:
                        self.menu_state = 'main'
                        self.index = 0
                        self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'foe used move':
                # switch to critical hit, effectiveness, friend move or move menu
                self.selected_foe_move.use(self.foe, self.friend)
                self.foe_moved = True

                if self.selected_foe_move.move_missed == True:
                    self.menu_state = 'foe missed'
                else:
                    if self.selected_foe_move.landed_crit:
                        self.menu_state = 'foe critical hit'
                    elif self.selected_foe_move.effectiveness(self.friend) != 1:
                        self.menu_state = 'foe effectiveness'
                    elif self.friend.is_fainted():
                        self.menu_state = 'friend fainted'
                    elif self.friend.flinch:
                        if self.friend_moved is False:
                            self.friend.flinch = False
                            self.friend.status_effect = False
                            self.friend_moved = True
                            self.menu_state = "friend flinched"
                        else:
                            self.menu_state = "friend flinched"
                    elif self.selected_foe_move.applied_poison:
                        self.menu_state = 'friend poisoned'
                    elif self.selected_foe_move.applied_burn:
                        self.menu_state = 'friend burned'
                    elif self.foe.status_effect:
                        if self.foe.poisoned:
                            self.menu_state = 'foe hurt by poison'
                        elif self.foe.badly_poisoned:
                            self.menu_state = 'foe hurt by poison'
                        elif self.foe.burned:
                            self.menu_state = 'foe hurt by burn'
                    elif self.friend_moved is False:
                        if self.friend.paralyzed:
                            rand_num = random.randint(0, 3)
                            if rand_num == 0:
                                self.friend_moved = True
                                self.menu_state = 'friend paralyzed'
                            else:
                                self.menu_state = 'friend used move'
                        else:
                            self.menu_state = 'friend used move'
                    else:
                        self.menu_state = 'main'
                        self.index = 0
                        self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'friend critical hit':
                # switch to move effectiveness, opponent move, or move menu
                if self.selected_friend_move.effectiveness(self.foe) != 1:
                    self.menu_state = 'friend effectiveness'
                elif self.foe.is_fainted():
                    self.menu_state = 'foe fainted'
                elif self.foe.status_effect:
                    if self.foe.flinch:
                        if self.foe_moved is False:
                            self.foe.flinch = False
                            self.foe.status_effect = False
                            self.foe_moved = True
                            self.menu_state = "foe flinched"
                        else:
                            self.menu_state = "foe flinched"
                elif self.foe_moved is False:
                    self.menu_state = 'foe used move'
                else:
                    self.menu_state = 'fight'

            elif self.menu_state == 'foe critical hit':
                # switch to move effectiveness, opponent move, or move menu
                if self.selected_foe_move.effectiveness(self.friend) != 1:
                    self.menu_state = 'foe effectiveness'
                elif self.friend.is_fainted():
                    self.menu_state = 'friend fainted'
                elif self.friend.status_effect:
                    if self.friend.flinch:
                        if self.friend_moved is False:
                            self.friend.flinch = False
                            self.friend.status_effect = False
                            self.friend_moved = True
                            self.menu_state = "friend flinched"
                        else:
                            self.menu_state = "friend flinched"
                elif self.friend_moved is False:
                    self.menu_state = 'friend used move'
                else:
                    self.menu_state = 'fight'

            elif self.menu_state == 'friend effectiveness':
                # switch to  opponent move or move menu
                if self.foe.is_fainted():
                    self.menu_state = 'foe fainted'
                elif self.foe.status_effect:
                    if self.foe.flinch:
                        if self.foe_moved is False:
                            self.foe.flinch = False
                            self.foe.status_effect = False
                            self.foe_moved = True
                            self.menu_state = "foe flinched"
                        else:
                            self.menu_state = "foe flinched"
                elif self.foe_moved is False:
                    self.menu_state = 'foe used move'
                else:
                    self.menu_state = 'fight'

            elif self.menu_state == 'foe effectiveness':
                # switch to  opponent move or move menu
                if self.friend.is_fainted():
                    self.menu_state = 'friend fainted'
                elif self.friend.status_effect:
                    if self.friend.flinch:
                        if self.friend_moved is False:
                            self.friend.flinch = False
                            self.friend.status_effect = False
                            self.friend_moved = True
                            self.menu_state = "friend flinched"
                        else:
                            self.menu_state = "friend flinched"
                elif self.friend_moved is False:
                    self.menu_state = 'friend used move'
                else:
                    self.menu_state = 'fight'

            elif self.menu_state == 'friend flinched':
                # switch to  opponent move or move menu
                if self.friend.is_fainted():
                    self.menu_state = 'friend fainted'
                else:
                    self.menu_state = 'fight'

            elif self.menu_state == 'foe flinched':
                # switch to  opponent move or move menu
                if self.foe.is_fainted():
                    self.menu_state = 'foe fainted'
                else:
                    self.menu_state = 'main'
                    self.index = 0
                    self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'friend paralyzed':
                # switch to  opponent move or move menu
                if self.friend.is_fainted():
                    self.menu_state = 'friend fainted'
                else:
                    self.menu_state = 'fight'

            elif self.menu_state == 'foe paralyzed':
                # switch to  opponent move or move menu
                if self.foe.is_fainted():
                    self.menu_state = 'foe fainted'
                else:
                    self.menu_state = 'main'
                    self.index = 0
                    self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'friend poisoned':
                self.menu_state = 'main'
                self.index = 0
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'foe poisoned':
                self.menu_state = 'main'
                self.index = 0
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'foe hurt by poison':
                self.foe.apply_poison()
                if self.foe.is_fainted():
                    self.menu_state = 'foe fainted'
                elif self.friend_moved is False:
                    self.menu_state = 'friend used move'
                else:
                    self.menu_state = 'main'
                    self.index = 0
                    self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'friend hurt by poison':
                self.friend.apply_poison()
                # switch to  opponent move or move menu
                if self.friend.is_fainted():
                    self.menu_state = 'friend fainted'
                elif self.foe_moved is False:
                    self.menu_state = 'foe used move'
                else:
                    self.menu_state = 'main'
                    self.index = 0
                    self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'friend burned':
                self.menu_state = 'main'
                self.index = 0
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'foe burned':
                self.menu_state = 'main'
                self.index = 0
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'foe hurt by burn':
                self.foe.apply_burn()
                if self.foe.is_fainted():
                    self.menu_state = 'foe fainted'
                elif self.friend_moved is False:
                    self.menu_state = 'friend used move'
                else:
                    self.menu_state = 'main'
                    self.index = 0
                    self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'friend hurt by burn':
                self.friend.apply_burn()
                # switch to  opponent move or move menu
                if self.friend.is_fainted():
                    self.menu_state = 'friend fainted'
                elif self.foe_moved is False:
                    self.menu_state = 'foe used move'
                else:
                    self.menu_state = 'main'
                    self.index = 0
                    self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'friend fainted':
                self.menu_state = 'main'
                self.index = 0
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'foe fainted':
                self.menu_state = 'main'
                self.index = 0
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)

            elif self.menu_state == 'no pp left':
                self.menu_state = 'fight'

            elif self.menu_state == 'friend missed':
                self.menu_state = 'fight'

            elif self.menu_state == 'foe missed':
                self.menu_state = 'fight'

            elif self.menu_state == 'escape':
                self.game.playing = False
                self.game.running = False

        if actions['back']:
            if self.menu_state == 'fight':
                self.menu_state = 'main'
                self.index = 0
                self.cursor_rect.x, self.cursor_rect.y = self.scaled_main_battle_menu_rect.x + (8 * self.game.SCALE), self.scaled_main_battle_menu_rect.y + (14 * self.game.SCALE)
        self.game.reset_keys()

    def render(self, display):
        display.blit(self.scaled_background_img, (0,0))
        if self.menu_state == 'main':
            display.blit(self.scaled_main_battle_menu, self.scaled_main_battle_menu_rect)

        elif self.menu_state == 'friend fainted':
            self.game.draw_text(display, f"{self.friend.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"fainted!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'foe fainted':
            self.game.draw_text(display, f"Enemy {self.foe.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"fainted!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'friend hurt by poison':
            self.game.draw_text(display, f"{self.friend.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was hurt by poison!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'foe hurt by poison':
            self.game.draw_text(display, f"Enemy {self.foe.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was hurt by poison!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'friend poisoned':
            self.game.draw_text(display, f"{self.friend.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was poisoned!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'foe poisoned':
            self.game.draw_text(display, f"Enemy {self.foe.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was poisoned!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'friend hurt by burn':
            self.game.draw_text(display, f"{self.friend.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was hurt by it's burn!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'foe hurt by burn':
            self.game.draw_text(display, f"Enemy {self.foe.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was hurt by it's burn!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'friend burned':
            self.game.draw_text(display, f"{self.friend.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was burned!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'foe burned':
            self.game.draw_text(display, f"Enemy {self.foe.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"was burned!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))
        
        elif self.menu_state == 'friend used move':
            self.game.draw_text(display, f"{self.friend.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"used {self.selected_friend_move.name.upper()}!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))
        
        elif self.menu_state == 'foe used move':
            self.game.draw_text(display, f"Enemy {self.foe.name.upper()}", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
            self.game.draw_text(display, f"used {self.selected_foe_move.name.upper()}!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))
        
        elif self.menu_state == 'friend critical hit' or self.menu_state == 'foe critical hit':
            self.game.draw_text(display, "A critical hit!", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))

        elif self.menu_state == 'friend effectiveness':
            if self.selected_friend_move.effectiveness(self.foe) > 1:
                self.game.draw_text(display, "It's super", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
                self.game.draw_text(display, "effective!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))
            elif self.selected_friend_move.effectiveness(self.foe) < 1:
                self.game.draw_text(display, "It's not very", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
                self.game.draw_text(display, "effective...", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))

        elif self.menu_state == 'foe effectiveness':
            if self.selected_foe_move.effectiveness(self.friend) > 1:
                self.game.draw_text(display, "It's super", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
                self.game.draw_text(display, "effective!", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))
            elif self.selected_foe_move.effectiveness(self.friend) < 1:
                self.game.draw_text(display, "It's not very", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
                self.game.draw_text(display, "effective...", self.game.BLACK, (9*self.game.SCALE),  (128*self.game.SCALE))
        
        elif self.menu_state == 'friend flinched':
            self.game.draw_text(display, f"{self.friend.name.upper()} flinched!", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))
        
        elif self.menu_state == 'foe flinched':
            self.game.draw_text(display, f"{self.foe.name.upper()} flinched!", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))

        elif self.menu_state == 'no pp left':
            self.game.draw_text(display, "No pp left!", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))

        elif self.menu_state == 'friend missed':
            self.game.draw_text(display, f"{self.friend.name.upper()} missed!", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))

        elif self.menu_state == 'foe missed':
            self.game.draw_text(display, f"{self.foe.name.upper()} missed!", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))

        elif self.menu_state == 'escape':
            self.escape(display)

        self.draw_foe(display)
        self.draw_friend(display)

    def draw_hp_bar(self, display, pokemon, x, y):
        def hp_bar_colour(pokemon):
            ratio = pokemon.transitionHP / pokemon.maxHP
            if ratio > 0.5625:
                return self.game.GREEN
            elif 0.5625 >= ratio > 0.29167:
                return self.game.YELLOW
            elif ratio <= 0.29167:
                return self.game.RED

        def hp_bar_length(pokemon):
            if pokemon.currentHP < pokemon.transitionHP:
                pokemon.transitionHP -= 1
                ratio = pokemon.transitionHP / pokemon.maxHP
            if pokemon.currentHP > pokemon.transitionHP:
                pokemon.transitionHP += 1
                ratio = pokemon.transitionHP / pokemon.maxHP
            if pokemon.currentHP == pokemon.transitionHP:
                ratio = pokemon.currentHP / pokemon.maxHP

            length = ratio * (48 * self.game.SCALE)
            return int(length)
        
        pygame.draw.rect(display, hp_bar_colour(pokemon), (x, y, hp_bar_length(pokemon), 2 * self.game.SCALE))

    def draw_xp_bar(self, display, pokemon, x, y):
        def xp_bar_length(pokemon):
            if pokemon.curr_xp > pokemon.transition_xp:
                pokemon.transition_xp += 5
                ratio = (pokemon.transition_xp - pokemon.current_level_xp) / (pokemon.next_level_xp - pokemon.current_level_xp)
            if pokemon.curr_xp == pokemon.transition_xp:
                ratio = (pokemon.curr_xp - pokemon.current_level_xp) / (pokemon.next_level_xp - pokemon.current_level_xp)
            length = ratio * (64 * self.game.SCALE)
            if int(length) > (64 * self.game.SCALE):
                length = (64 * self.game.SCALE)
            return int(length)

        pygame.draw.rect(display, self.game.BLUE, (x, y, xp_bar_length(pokemon), 2 * self.game.SCALE))

    def draw_gender(self, display, pokemon, x, y):
        gender = "@" if pokemon.gender == "Male" else "#"
        self.game.draw_text(display, gender, self.game.BLACK, x, y)

    def draw_status(self, display, pokemon, x, y):
        if pokemon.poisoned or pokemon.badly_poisoned:
            status = "PSN"
        elif pokemon.burned:
            status = "BRN"
        else:
            status = ""
        self.game.draw_text(display, status, self.game.BLACK, x, y)

    def draw_foe(self, display):
        display.blit(self.foe.battle_front, self.foe.front_rect)
        self.draw_gender(display, self.foe, 320, 32)
        self.draw_hp_bar(display, self.foe, 128, 76)
        self.game.draw_text(display, self.foe.name.upper(), self.game.BLACK, 36, 0)
        self.game.draw_text(display, str(self.foe.level), self.game.BLACK, 228, 28)
        self.draw_status(display, self.foe, 92, 29)

    def draw_friend(self, display):
        display.blit(self.friend.battle_back, self.friend.back_rect)
        self.draw_hp_bar(display, self.friend, 384, 300)
        self.draw_xp_bar(display, self.friend, 320, 365)
        self.draw_gender(display, self.friend, 580, 256)
        self.game.draw_text(display, self.friend.name.upper(), self.game.BLACK, 320, 224)
        self.game.draw_text(display, str(self.friend.level), self.game.BLACK, 484, 252)
        self.draw_status(display, self.friend, 352, 253)
        self.game.draw_text(display, f"{self.friend.transitionHP}/{self.friend.maxHP}", self.game.BLACK, 576, 320, alignment='right')

        if self.menu_state == 'main':
            display.blit(self.scaled_cursor_img, self.cursor_rect)
        if self.menu_state == 'fight':
            display.blit(self.scaled_battle_move_menu, self.scaled_battle_move_menu_rect)
            display.blit(self.scaled_cursor_img, self.cursor_rect)

            # Move list
            num_moves = len(self.friend.moves)
            for index, move in enumerate(self.friend.moves):
                self.game.draw_text(display, move.name.upper(), self.game.BLACK, self.scaled_battle_move_menu_rect.x + (48*self.game.SCALE), self.scaled_battle_move_menu_rect.y + (37*self.game.SCALE) + (32*index))
            for blank_move in range(len(self.friend.moves), 4):
                self.game.draw_text(display, "-", self.game.BLACK, self.scaled_battle_move_menu_rect.x + (48*self.game.SCALE), self.scaled_battle_move_menu_rect.y + (37*self.game.SCALE) + (32*blank_move))

            # Move type
            self.game.draw_text(display, self.friend.moves[self.index].type.upper(), self.game.BLACK, self.scaled_battle_move_menu_rect.x + (16*self.game.SCALE), self.scaled_battle_move_menu_rect.y + (13*self.game.SCALE))
            self.game.draw_text(display, f"{self.friend.moves[self.index].curr_pp}/{self.friend.moves[self.index].pp}", self.game.BLACK, self.scaled_battle_move_menu_rect.x + (80*self.game.SCALE), self.scaled_battle_move_menu_rect.y + (21*self.game.SCALE), alignment='right')

    def escape(self, display):
        self.game.draw_text(display, f"Got away safely!", self.game.BLACK, (9*self.game.SCALE),  (112*self.game.SCALE))

    def new_turn(self):
        if self.friend_moved is True and self.foe_moved is True:
            self.friend_moved = False
            self.foe_moved = False

    def set_moves(self):
        self.selected_friend_move = self.friend.moves[self.index]
        if self.selected_friend_move.curr_pp <= 0:
            self.menu_state = 'no pp left'
        self.selected_foe_move = self.foe.moves[random.randint(0, len(self.foe.moves)-1)]

    def move_order(self):
        if self.selected_friend_move.priority > self.selected_foe_move.priority:
            self.first_move = self.friend
            self.second_move = self.foe

        if self.selected_friend_move.priority < self.selected_foe_move.priority:
            self.first_move = self.foe
            self.second_move = self.friend

        if self.selected_friend_move.priority == self.selected_foe_move.priority:
            if self.friend.speed >= self.foe.speed:
                self.first_move = self.friend
                self.second_move = self.foe
            else:
                self.first_move = self.foe
                self.second_move = self.friend

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
                if self.index < len(self.friend.moves)-1:
                    self.index += 1
                    self.cursor_rect.y = self.cursor_rect.y + (8 * self.game.SCALE)
            if actions['up']:
                if self.index > 0:
                    self.index -= 1
                    self.cursor_rect.y = self.cursor_rect.y - (8 * self.game.SCALE)        
