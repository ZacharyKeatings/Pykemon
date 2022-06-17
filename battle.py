from move import Move
import pokemon
import pygame

class Battle:
    def __init__(self, attacker, defender):
        self.turn = 0
        self.weather = None
        self.attacker = attacker
        self.defender = defender


    def attack(self):
        move_list = self.attacker.moves
        move_choice = input(f"Choose a move: {move_list}\n")
        Move(move_choice).use(self.attacker, self.defender)
        Battle.next_turn(self)

    def use_item(self):
        pass

    def switch_pokemon(self):
        pass

    def escape(self):
        print("You got away safely!")
        self.turn = 0

    def next_turn(self):
        self.attacker, self.defender = self.defender, self.attacker
        self.turn += 1

    def battle_loop(self):
        #!1 - attack, 2 - change pkmn, 3 - item, 4 - run
        curr_battle = True
        while curr_battle:
            if self.attacker.currentHP == 0 or self.defender.currentHP == 0:
                curr_battle = False
            print(f"{self.attacker.name}'s HP: {self.attacker.currentHP}/{self.attacker.maxHP}")
            print(f"{self.defender.name}'s HP: {self.defender.currentHP}/{self.defender.maxHP}")
            player_choice = int(input("Make a choice\n"))
            if player_choice == 1:
                Battle.attack(self)
            elif player_choice == 2:
                pass
            elif player_choice == 3:
                pass
            elif player_choice == 4:
                Battle.escape(self)
                curr_battle = False

    def end_fight(self, attacker, defender):
        print(f"{defender.name} fainted!") #!----------------------------------
        print(f"previous xp: {attacker.curr_xp}") #!----------------------------
        xp = pokemon.Pokemon.exp_gained(self, defender)
        attacker.curr_xp += xp
        print(f"current xp: {attacker.curr_xp}") #!----------------------------

