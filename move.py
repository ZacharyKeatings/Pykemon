from settings import load_json
import pokemon
import random

type_dict = load_json("typeDB")
move_dict = load_json("moveDB")

#! Add never miss method
#! Add way to increase move chance to crit

class Move:
    def __init__(self, name):
        self.name = name
        self.type = move_dict[self.name]["Type"]
        self.damage_class = move_dict[self.name]["Damage-Class"]
        self.pp = move_dict[self.name]["PP"]
        self.max_pp = move_dict[self.name]["Max-PP"]
        self.power = move_dict[self.name]["Power"]
        self.accuracy = move_dict[self.name]["Accuracy"]
        self.priority = move_dict[self.name]["Priority"]
        self.description = move_dict[self.name]["Description"]
        self.effect = move_dict[self.name]["Effect"]
        self.effect_rate = move_dict[self.name]["Effect-Rate"]
        self.stat_stage = move_dict[self.name]["Stat-Stage"]
        self.landed_crit = False

    def get_priority(self):
        return self.priority

    def get_type(self):
        return self.type

    def paralyzed(self, defender):
        '''
        pokemon has 25% chance of not being able to attack.
        Remains after battle ends.
        '''
        pass

    def poisoned(self, defender):
        '''
        Pokemon loses 1/16 of maxHP each turn.
        Remains after battle ends. Pokemon loses 1 HP every 4 steps until (Pokemon has 1HP/Pokemon faints)
        '''
        pass

    def badly_poisoned(self, defender):
        '''
        Pokemon loses 1/16 of maxHP on first turn. Each sequential turn, add 1/16 of maxHP to damage.
        Becomes regular poison after battle ends. Pokemon loses 1 HP every 4 steps until (Pokemon has 1HP/Pokemon faints)
        '''
        pass

    def burned(self, defender):
        '''
        Pokemon loses 1/8 of maxHP at the end of each turn.
        Pokemon attack reduced by 50%.
        '''
        pass

    def frozen(self, defender):
        '''
        Pokemon cannot attack, but has 20% chance each turn to remove effect.
        If pokemon attacked with Fire-type move, will remove effect.
        '''
        pass

    def flinch(self, defender):
        '''
        Pokemon cannot use move on their next turn.
        '''
        print(f"{defender.name} Flinched!")#!------------------------------

    def confused(self, defender):
        '''
        Pokemon has 50% chance of hurting themselves between 1-4 turns.
        Pokemon can be confused along with other effects.
        '''
        pass

    def infatuation(self, defender):
        '''
        Pokemon has 50% chance of becoming infatuated.
        While infatuated, Pokemon will not attack between 5-6 turns.
        '''
        pass

    def leech_seed(self, defender):
        '''
        Pokemon loses 1/16 of maxHP each turn, and the active Pokemon heals HP for damage amount.
        '''
        pass

    def sleep(self, defender):
        '''
        Pokemon is asleep and cannot use any move between 1 - 7 turns.
        '''
        pass

    def raise_stat(self, defender):
        '''
        Increases stat of Pokemon
        '''
        pass

    def lower_stat(self, defender):
        '''
        Decreases stat of Pokemon
        '''
        pass

    def effectiveness(self, defender):
        '''
        calculates move effectiveness based on type.
        '''
        effectiveness_modifier = 1
        for index, type in enumerate(defender.type):
            for i, type2 in enumerate(type_dict[self.type]["Double_Damage_To"]):
                if type in type2:
                    effectiveness_modifier *= 2
            for i, type2 in enumerate(type_dict[self.type]["Half_Damage_To"]):
                if type in type2:
                    effectiveness_modifier *= 0.5
            for i, type2 in enumerate(type_dict[self.type]["No_Damage_To"]):
                if type in type2:
                    effectiveness_modifier = 0

        return effectiveness_modifier

    def calc_stab(self, attacker):
        '''If attacking Pokemon uses a move with a type that matches own type, return 1.5 multiplier, else return 1'''
        stab = 1
        if self.type in enumerate(attacker.type):
            stab = 1.5

        return stab

#! Update Crit to calculate based on pokemon stat crit stage to work with stat modifier moves
    def crit_hit(self, attacker):
        is_crit = random.randint(0, attacker.speed)
        if is_crit > (attacker.speed/2):
            self.landed_crit = True
            return 1.5
        else:
            self.landed_crit = False
            return 1

    def calc_damage(self, attacker, defender):
        '''
        ((((2 * Level / 5 + 2) * AttackStat * AttackPower / DefenseStat) / 50) + 2) * STAB * Weakness/Resistance * Random(85-100) / 100
        level = pokemon level
        attackStat = attacking pokemon's attack/special attack
        attackPower = move power
        defenseStat = defending pokemon's defense/special defense
        STAB = Pokemon.calc_stab
        weakness/resistence = Pokemon.effectiveness
        random(85-100) = returns a random number between 85 and 100
        '''
        if self.damage_class == "Physical":
            attackstat = attacker.attack
            defensestat = defender.defense
        elif self.damage_class == "Special":
            attackstat = attacker.spatk
            defensestat = defender.spdef
        
        if self.power > 0:
            damage = ((((2 * attacker.level / 5 + 2) * attackstat * self.power / defensestat) / 50) + 2) * Move.calc_stab(self, attacker) * Move.crit_hit(self, attacker) * Move.effectiveness(self, defender) * random.randint(85, 100) / 100
        else:
            damage = 0

        return int(damage)

    def apply_effects(self, defender):
        '''
        Checks if move applies any status effect to defending pokemon
        '''
        chance = random.randint(0, 101)
        if chance < move_dict[self.name]["Effect-Rate"]:
            if move_dict[self.name]["Effect"] == "Paralyzed":
                Move.paralyzed(self, defender)
            if move_dict[self.name]["Effect"] == "Poisoned":
                Move.poisoned(self, defender)
            if move_dict[self.name]["Effect"] == "Badly_Poisoned":
                Move.badly_poisoned(self, defender)
            if move_dict[self.name]["Effect"] == "Burned":
                Move.burned(self, defender)
            if move_dict[self.name]["Effect"] == "Frozen":
                Move.frozen(self, defender)
            if move_dict[self.name]["Effect"] == "Flinch":
                Move.flinch(self, defender)
            if move_dict[self.name]["Effect"] == "Confused":
                Move.confused(self, defender)
            if move_dict[self.name]["Effect"] == "Infatuation":
                Move.infatuation(self, defender)
            if move_dict[self.name]["Effect"] == "Leech_Seed":
                Move.leech_seed(self, defender)
            if move_dict[self.name]["Effect"] == "Sleep":
                Move.sleep(self, defender)

    def use(self, attacker, defender):
        '''
        calls a move.
        runs status effect check, if applicable. then applies damage, if applicable
        '''
        if self.effect != "":
            Move.apply_effects(self, defender)
        damage = Move.calc_damage(self, attacker, defender)
        # defender.transitionHP = defender.currentHP
        defender.currentHP -= damage
        if defender.currentHP < 0:
            defender.currentHP = 0

    def learn(self, pokemon):
        '''
        If Pokemon levels up and can learn a new move, add move to move_list if len < 4. if >= 4, ask to forget one move.
        '''
        pass