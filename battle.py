from move import Move
from pokemon import Pokemon
import random
from settings import load_json

move_dict = load_json("moveDB")

class Battle:
    def __init__(self, attacker, defender):
        self.weather = None
        self.attacker = attacker
        self.defender = defender


    def fight(self):
        #pick move from list
        attacker_move = random.choice(self.attacker.moves)
        #defender pkmn uses random move
        defender_move = random.choice(self.defender.moves)
        #move priority checked -> higher priority goes first
        if not self.attacker.is_fainted() and not self.defender.is_fainted():
            if Move(attacker_move).get_priority() == Move(defender_move).get_priority():
            #if priority equal, check pkmn speed -> faster goes first
                if self.attacker.speed >= self.defender.speed:
                    Move(attacker_move).use(self.attacker, self.defender)
                    if not self.defender.is_fainted():
                        Move(defender_move).use(self.defender, self.attacker)
                    else:
                        Battle.end_fight(self, self.attacker, self.defender)
                else:
                    Move(defender_move).use(self.defender, self.attacker)
                    if not self.attacker.is_fainted():
                        Move(attacker_move).use(self.attacker, self.defender)
                    else:
                        Battle.end_fight(self, self.defender, self.attacker)
            elif Move(attacker_move).get_priority() > Move(attacker_move).get_priority():
                Move(attacker_move).use(self.attacker, self.defender)
                if not self.defender.is_fainted():
                    Move(defender_move).use(self.defender, self.attacker)
                else:
                    Battle.end_fight(self, self.attacker, self.defender)
            elif Move(attacker_move).get_priority() < Move(attacker_move).get_priority():
                Move(defender_move).use(self.defender, self.attacker)
                if not self.attacker.is_fainted():
                    Move(attacker_move).use(self.attacker, self.defender)
                else:
                    Battle.end_fight(self, self.defender, self.attacker)    

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
        if self.attacker.speed > self.defender.speed:
            print("You got away safely!")
        else:
            print("Can't escape!")

    def battle_loop(self):
        #!1 - attack, 2 - change pkmn, 3 - item, 4 - run
        while True:
            if self.attacker.currentHP == 0 or self.defender.currentHP == 0:
                break
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
                break

    def end_fight(self, attacker, defender):
        print(f"{defender.name} fainted!") #!----------------------------------
        print(f"previous xp: {attacker.curr_xp}") #!----------------------------
        xp = attacker.exp_gained(defender)
        attacker.curr_xp += xp
        print(f"current xp: {attacker.curr_xp}") #!----------------------------
