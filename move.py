from settings import load_json
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
        self.curr_pp = self.pp
        self.max_pp = move_dict[self.name]["Max-PP"]
        self.power = move_dict[self.name]["Power"]
        self.accuracy = move_dict[self.name]["Accuracy"]
        self.priority = move_dict[self.name]["Priority"]
        self.description = move_dict[self.name]["Description"]
        self.effect = move_dict[self.name]["Effect"]
        self.effect_rate = move_dict[self.name]["Effect-Rate"]
        self.stat_stage = move_dict[self.name]["Stat-Stage"]
        self.crit_threshold = None
        self.landed_crit = False
        self.move_missed = False

        self.applied_poison = False
        self.applied_bad_poison = False
        self.applied_burn = False
        self.applied_paralyzed = False
        self.applied_frozen = False


    def flinch(self, defender):
        '''
        Pokemon cannot use move on their next turn.
        '''
        defender.flinch = True
        defender.status_effect = True

    def poisoned(self, defender):
        '''
        Pokemon loses 1/16 of maxHP each turn.
        Remains after battle ends. Pokemon loses 1 HP every 4 steps until (Pokemon has 1HP/Pokemon faints)
        '''
        defender.poisoned = True
        defender.status_effect = True

    def badly_poisoned(self, defender):
        '''
        Pokemon loses 1/16 of maxHP on first turn. Each sequential turn, add 1/16 of maxHP to damage.
        Becomes regular poison after battle ends. Pokemon loses 1 HP every 4 steps until (Pokemon has 1HP/Pokemon faints)
        '''
        defender.badly_poisoned = True
        defender.status_effect = True

    def burned(self, defender):
        '''
        Pokemon loses 1/8 of maxHP at the end of each turn.
        Pokemon attack reduced by 50%.
        '''
        defender.burned = True
        defender.status_effect = True

    def paralyzed(self, defender):
        '''
        pokemon has 25% chance of not being able to attack.
        Remains after battle ends.
        '''
        defender.paralyzed = True

    def frozen(self, defender):
        '''
        Pokemon cannot attack, but has 20% chance each turn to remove effect.
        If pokemon attacked with Fire-type move, will remove effect.
        '''
        defender.frozen = True

#!
    def confused(self, defender):
        '''
        Pokemon has 50% chance of hurting themselves between 2-5 turns.
        Pokemon can be confused along with other effects.
        '''
        defender.status_counter = random.randint(2, 5)
        defender.confused = True

#!
    def infatuation(self, defender):
        '''
        Pokemon has 50% chance of becoming infatuated.
        While infatuated, Pokemon will not attack between 5-6 turns.
        '''
        pass

#!
    def leech_seed(self, defender):
        '''
        Pokemon loses 1/16 of maxHP each turn, and the active Pokemon heals HP for damage amount.
        '''
        pass

#!
    def sleep(self, defender):
        '''
        Pokemon is asleep and cannot use any move between 1 - 7 turns.
        '''
        pass

#!
    def raise_stat(self, attacker):
        '''
        Increases stat of Pokemon
        '''
        pass

#!
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

    def crit_hit(self, attacker):
        '''
        This calculation uses the gen III-V formula
        '''

        if attacker.crit_stage == 0:
            self.crit_threshold = 16
        elif attacker.crit_stage == 1:
            self.crit_threshold = 8
        elif attacker.crit_stage == 2:
            self.crit_threshold = 4
        elif attacker.crit_stage == 3:
            self.crit_threshold = 3
        elif attacker.crit_stage <= 4:
            self.crit_threshold = 2
        rand_num = random.randint(1, self.crit_threshold)

        if rand_num == self.crit_threshold:
            self.landed_crit = True
        else:
            self.landed_crit = False

    def miss_check(self):
        rand_num = random.randint(0, 101)
        if rand_num > self.accuracy:
            self.move_missed = True
        else:
            self.move_missed = False

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
            self.crit_hit(attacker)
            crit_modifier = 2 if self.landed_crit else 1
            damage = ((((2 * (attacker.level * crit_modifier) / 5 + 2) * attackstat * self.power / defensestat) / 50) + 2) * Move.calc_stab(self, attacker) * Move.effectiveness(self, defender) * random.randint(85, 100) / 100
        else:
            damage = 0

        return int(damage)

#!
    def apply_effects(self, defender):
        '''
        Checks if move applies any status effect to defending pokemon
        '''
        chance = random.randint(0, 101)
        if chance < self.effect_rate:
            if self.effect == "Paralyzed":
                self.applied_paralyzed = True
                self.paralyzed(defender)
            if self.effect == "Poisoned":
                self.applied_poison = True
                self.poisoned(defender)
            if self.effect == "Badly Poisoned":
                self.applied_bad_poison = True
                self.badly_poisoned(defender)
            if self.effect == "Burn":
                self.applied_burn = True
                self.burned(defender)
            if self.effect == "Freeze":
                self.applied_frozen = True
                self.frozen(defender)
            if self.effect == "Flinch":
                self.flinch(defender)

            if self.effect == "Confused":
                self.confused(defender)
            if self.effect == "Infatuation":
                self.infatuation(defender)
            if self.effect == "Leech Seed":
                self.leech_seed(defender)
            if self.effect == "Sleep":
                self.sleep(defender)

    def use(self, attacker, defender):
        '''
        calls a move.
        runs status effect check, if applicable. then applies damage, if applicable
        '''
        #Chance to miss:
        self.move_missed = False
        self.miss_check()
        if not self.move_missed:
            if self.effect != "":
                self.apply_effects(defender)
            if attacker.burned:
                original_attack = attacker.attack
                attacker.attack /= 2
            damage = self.calc_damage(attacker, defender)
            if attacker.burned:
                attacker.attack = original_attack
            defender.currentHP -= damage
            if defender.currentHP < 0:
                defender.currentHP = 0

#! should be in pokemon class
    def learn(self, pokemon):
        '''
        If Pokemon levels up and can learn a new move, add move to move_list if len < 4. if >= 4, ask to forget one move.
        '''
        pass

#! should be in pokemon class
    def forget(self, pokemon):
        '''
        If a Pokemon is trying to learn a new move but has 4 moves in move_list, forget a move first
        '''
        pass
