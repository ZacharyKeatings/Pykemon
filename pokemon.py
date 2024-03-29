from settings import load_json
import random
from cmath import sqrt
import pygame
from move import Move

pkmn_dict = load_json("pokemonDB")
type_dict = load_json("typeDB")
move_dict = load_json("moveDB")

class Pokemon:
    def __init__(self, name):
        self.name = name
        self.moves = None
        self.type = pkmn_dict[self.name]["Type"]
        self.gender = Pokemon.set_gender(self)
        self.pokedex_number = pkmn_dict[self.name]["Pokedex-Number"]

        #Base stats of selected Pokemon
        self.base_hp = pkmn_dict[self.name]["Base-Stats"]["HP"]
        self.base_attack = pkmn_dict[self.name]["Base-Stats"]["Attack"]
        self.base_defense = pkmn_dict[self.name]["Base-Stats"]["Defense"]
        self.base_spatk = pkmn_dict[self.name]["Base-Stats"]["SpAtk"]
        self.base_spdef = pkmn_dict[self.name]["Base-Stats"]["SpDef"]
        self.base_speed = pkmn_dict[self.name]["Base-Stats"]["Speed"]
        self.ivs = Pokemon.random_ivs(self)
        Pokemon.hp_iv(self)
        self.shiny = Pokemon.is_shiny(self)

        #Stat exp
        self.hp_xp = 0
        self.attack_xp = 0
        self.defense_xp = 0
        self.spatk_xp = 0
        self.spdef_xp = 0
        self.speed_xp = 0

        #Current stats
        self.curr_xp = 0
        self.transition_xp = self.curr_xp
        self.level = 1
        self.current_level_xp = 0
        self.next_level_xp = 0
        Pokemon.set_level(self)
        self.attack = Pokemon.calc_stats(self, self.base_attack, self.ivs['Attack'], Pokemon.stat_point(self, self.attack_xp))
        self.defense = Pokemon.calc_stats(self, self.base_defense, self.ivs['Defense'], Pokemon.stat_point(self, self.defense_xp))
        self.spatk = Pokemon.calc_stats(self, self.base_spatk, self.ivs['Special-Attack'], Pokemon.stat_point(self, self.spatk_xp))
        self.spdef = Pokemon.calc_stats(self, self.base_spdef, self.ivs['Special-Defense'], Pokemon.stat_point(self, self.spdef_xp))
        self.speed = Pokemon.calc_stats(self, self.base_speed, self.ivs['Speed'], Pokemon.stat_point(self, self.speed_xp))
        self.maxHP = Pokemon.calc_hp(self, self.base_hp, self.ivs['HP'], Pokemon.stat_point(self, self.hp_xp))
        self.currentHP = self.maxHP
        self.transitionHP = self.currentHP
        self.wild = False
        self.traded = False
        self.held_item = None

        #Status effects
        self.status_counter = 0
        self.status_effect = False # Set to True if any other status effect is True
        self.paralyzed = False
        self.poisoned = False
        self.badly_poisoned = False
        self.burned = False
        self.frozen = False
        self.flinch = False
        self.confused = False # Only status that can be True while self.status_effect is True
        self.infatuation = False
        self.leech_seed = False
        self.asleep = False

        #Stat stages in battle
        self.attack_stage = 0
        self.defense_stage = 0
        self.speed_stage = 0
        self.crit_stage = 0
        self.spatk_stage = 0
        self.spdef_stage = 0
        self.evasion_stage = 0

        #!Images
        #back
        back = pygame.image.load(f'assets/images/pokemon/back-{"shiny" if self.shiny else "normal"}/{self.pokedex_number}{self.name.lower()}.png').convert_alpha()
        self.battle_back = pygame.transform.scale(back, (288, 288))
        self.back_rect = self.battle_back.get_rect()
        self.back_rect.center = (160, 288)
        #front
        front = pygame.image.load(f'assets/images/pokemon/front-{"shiny" if self.shiny else "normal"}/{self.pokedex_number}{self.name.lower()}.png').convert_alpha()
        self.battle_front = pygame.transform.scale(front, (224, 224))
        self.front_rect = self.battle_front.get_rect()
        self.front_rect.center = (496, 112)

    def set_gender(self):
        '''
        Sets gender based on gender rate frequency in pokemon stats
        '''
        if random.randint(0, 1001) < (pkmn_dict[self.name]["Gender-Rate"]["Male"] * 10):
            return "Male"
        else:
            return "Female"

    def random_ivs(self):
        '''
        Sets random iv for each stat between 0-15
        '''
        stats = ('Attack', 'Defense', 'Speed', 'Special-Attack', 'Special-Defense')
        ivs = {stat: random.randint(0, 15) for stat in stats}
        return ivs

    def hp_iv(self):
        '''
        Calculates HP iv based on other stat ivs
        '''
        dv = 0
        special = 0
        for index, value in enumerate(self.ivs.values()):
            if (value % 2) == 0:
                if index == 0: #attack
                    dv += 8
                if index == 1: #defense
                    dv += 4
                if index == 2: #speed
                    dv += 2
                if index == 3: #spatk
                    special += 1
                if index == 4: #spdef
                    special += 1
        hp_iv = dv + special
        self.ivs['HP'] = hp_iv

    def stat_point(self, stat_xp):
        '''
        Calculates stat points for use in stat and hp formulas
        '''
        #This is a lvl 100 limiter. remove if uncapping lvl
        if stat_xp >= 65535:
            stat_xp = 65535
        point = sqrt(stat_xp - 1) + 1 / 4
        return int(point.real)

    def calc_stats(self, base_stat, iv, stat_point):
        '''
        Calculates all stats
        '''
        stat = (((base_stat + iv) * 2 + stat_point) * self.level / 100) + 5
        return int(stat)

    def calc_hp(self, base_stat, iv, stat_point):
        '''
        Calculates maxHP
        '''
        hp = (((base_stat + iv) * 2 + stat_point) * self.level / 100) + (self.level + 10)
        return int(hp)

    def set_level(self):
        '''
        Compares current xp and pokemon growth type and returns current level
        '''

        def erratic(level):
            if level < 50:
                gain = level**3 * (100 - level) / 50
            if 50 <= level < 68:
                gain = level**3 * (150 - level) / 100
            if 68 <= level < 98:
                gain = level**3 * ((1911-(10*level)) / 3) / 500
            if 98 <= level <= 100:
                gain = level**3 * (160 - level) / 100
            return int(gain)

        def fast(level):
            gain = 4 * level**3 / 5
            return int(gain)

        def medium_fast(level):
            gain = level**3
            return int(gain)

        def medium_slow(level):
            gain = (6/5 * level**3) - (15 * level**2) + (100 * level) - 140
            if gain < 0:
                gain = 0
            return int(gain)

        def slow(level):
            gain = 5 * level**3 / 4
            return int(gain)

        def fluctuating(level):
            if level < 15: #After lvl 5, gives slightly higher output
                gain = level**3 * ((((level + 1) / 3) + 24) / 50)
            if 15 <= level < 36:
                gain = level**3 * ((level + 14) / 50)
            if 36 <= level <= 100: #After lvl 74, gives slightly higher output
                gain = level**3 * (((level / 2) + 32) / 50)
            return int(gain)
        
        level_matching = True
        possible_level = 1
        if pkmn_dict[self.name]["Growth-Type"] == "Erratic":
            while level_matching:
                if erratic(possible_level) < self.curr_xp >= erratic(possible_level+1): #curr_xp is more than current and next level
                    possible_level += 1
                if erratic(possible_level) <= self.curr_xp < erratic(possible_level+1): #curr_xp 
                    self.level = possible_level
                    self.current_level_xp = erratic(possible_level)
                    self.next_level_xp = erratic(possible_level + 1)
                    level_matching = False
        if pkmn_dict[self.name]["Growth-Type"] == "Fast":
            while level_matching:
                if fast(possible_level) < self.curr_xp >= fast(possible_level+1): #curr_xp is more than current and next level
                    possible_level += 1
                if fast(possible_level) <= self.curr_xp < fast(possible_level+1): #curr_xp 
                    self.level = possible_level
                    self.current_level_xp = fast(possible_level)
                    self.next_level_xp = fast(possible_level + 1)
                    level_matching = False
        if pkmn_dict[self.name]["Growth-Type"] == "Medium-Fast":
            while level_matching:
                if medium_fast(possible_level) < self.curr_xp >= medium_fast(possible_level+1): #curr_xp is more than current and next level
                    possible_level += 1
                if medium_fast(possible_level) <= self.curr_xp < medium_fast(possible_level+1): #curr_xp 
                    self.level = possible_level
                    self.current_level_xp = medium_fast(possible_level)
                    self.next_level_xp = medium_fast(possible_level + 1)
                    level_matching = False
        if pkmn_dict[self.name]["Growth-Type"] == "Medium-Slow":
            while level_matching:
                if medium_slow(possible_level) < self.curr_xp >= medium_slow(possible_level+1): #curr_xp is more than current and next level
                    possible_level += 1
                if medium_slow(possible_level) <= self.curr_xp < medium_slow(possible_level+1): #curr_xp 
                    self.level = possible_level
                    self.current_level_xp = medium_slow(possible_level)
                    self.next_level_xp = medium_slow(possible_level + 1)
                    level_matching = False
        if pkmn_dict[self.name]["Growth-Type"] == "Slow":
            while level_matching:
                if slow(possible_level) < self.curr_xp >= slow(possible_level+1): #curr_xp is more than current and next level
                    possible_level += 1
                if slow(possible_level) <= self.curr_xp < slow(possible_level+1): #curr_xp 
                    self.level = possible_level
                    self.current_level_xp = slow(possible_level)
                    self.next_level_xp = slow(possible_level + 1)
                    level_matching = False
        if pkmn_dict[self.name]["Growth-Type"] == "Fluctuating":
            while level_matching:
                if fluctuating(possible_level) < self.curr_xp >= fluctuating(possible_level+1): #curr_xp is more than current and next level
                    possible_level += 1
                if fluctuating(possible_level) <= self.curr_xp < fluctuating(possible_level+1): #curr_xp 
                    self.level = possible_level
                    self.current_level_xp = fluctuating(possible_level)
                    self.next_level_xp = fluctuating(possible_level + 1)
                    level_matching = False

    #! Add xp. all calc once items are introduced
    def exp_gained(self, enemy):
        '''
        After pokemon is defeated, calculates xp gained for each pkmn
        flat_formula = (a*t*b*e*L) / (7 * s)
        a - 1 if pkmn is wild, 1.5 if owned by trainer
        t - 1 if winning pokemon owned by original trainer, 1.5 if traded
        b - base xp yield of fainted pkmn
        e - 1.5 if winner is holding lucky egg, else 1
        L - level of fainted pokemon
        s - w/o xp.all: the num of pkmn took part in battle w/o fainting.
            with xp.all: ~pkmn that participated: pkmn that battled * 2
                         ~pkmn in party: pkmn that battled * 2 * num of pkmn in party 
        '''

        self.hp_xp += enemy.base_hp
        self.attack_xp += enemy.base_attack
        self.defense_xp += enemy.base_defense
        self.spatk_xp += enemy.base_spatk
        self.spdef_xp += enemy.base_spdef
        self.speed_xp += enemy.base_speed

        a = 1 if enemy.wild else 1.5
        t = 1.5 if self.traded else 1
        b = sum(pkmn_dict[enemy.name]["Base-Stats"].values()) * 4 / 20
        e = 1.5 if self.held_item == "Lucky-Egg" else 1
        L = enemy.level
        xp_gained = (a*t*b*e*L) / (7 * 1)

        return int(xp_gained)

    def is_shiny(self):
        '''
        If pokemon stats are specific numbers, make them shiny. shiny is just a visual perk.
        '''

        shiny = False
        if self.ivs['Attack'] in (2, 3, 6, 7, 10, 11, 14, 15):
            if self.ivs['Defense'] == 10:
                if self.ivs['Speed'] == 10:
                    if self.ivs['Special-Attack'] == 10 or self.ivs['Special-Defense'] == 10:
                        shiny = True
        return shiny

    def is_fainted(self):
        '''
        Checks if pokemon is fainted. returns True if fainted.
        '''
        if self.currentHP <= 0:
            return True
        else:
            return False

    def level_up(self):
        '''
        recalculate stats based on new level
        '''

        self.attack = Pokemon.calc_stats(self, self.base_attack, self.ivs['Attack'], Pokemon.stat_point(self, self.attack_xp))
        self.defense = Pokemon.calc_stats(self, self.base_defense, self.ivs['Defense'], Pokemon.stat_point(self, self.defense_xp))
        self.spatk = Pokemon.calc_stats(self, self.base_spatk, self.ivs['Special-Attack'], Pokemon.stat_point(self, self.spatk_xp))
        self.spdef = Pokemon.calc_stats(self, self.base_spdef, self.ivs['Special-Defense'], Pokemon.stat_point(self, self.spdef_xp))
        self.speed = Pokemon.calc_stats(self, self.base_speed, self.ivs['Speed'], Pokemon.stat_point(self, self.speed_xp))
        self.maxHP = Pokemon.calc_hp(self, self.base_hp, self.ivs['HP'], Pokemon.stat_point(self, self.hp_xp))

    def evolve(self):
        '''
        recalculates base stats based on new species
        '''
        self.name = pkmn_dict[self.name]["Evolves-Into"]
        self.type = pkmn_dict[self.name]["Type"]
        self.pokedex_number = pkmn_dict[self.name]["Pokedex-Number"]
        self.base_hp = pkmn_dict[self.name]["Base-Stats"]["HP"]
        self.base_attack = pkmn_dict[self.name]["Base-Stats"]["Attack"]
        self.base_defense = pkmn_dict[self.name]["Base-Stats"]["Defense"]
        self.base_spatk = pkmn_dict[self.name]["Base-Stats"]["SpAtk"]
        self.base_spdef = pkmn_dict[self.name]["Base-Stats"]["SpDef"]
        self.base_speed = pkmn_dict[self.name]["Base-Stats"]["Speed"]
        Pokemon.level_up(self)
        
    def set_moves(self):
        '''
        assigns move set for wild pokemon based on level. 4 most recent moves are assigned
        '''

        possible_moves = []
        move_set = []

        #fill possible_moves with all moves available at pokemon current level:
        for index, move in enumerate(pkmn_dict[self.name]['Moves']):
            if pkmn_dict[self.name]['Moves'][move] <= self.level:
                possible_moves.append(Move(move))

        #Create list no longer than 4:
        for move in range(0, len(possible_moves)):
            if move == 4:
                break
            else:
                move_set.append(possible_moves[-abs(move+1)])

        #set pokemon moves with move_set:
        self.moves = move_set

    def apply_poison(self):
        if self.poisoned:
            damage = self.maxHP // 16
            self.currentHP -= damage

        elif self.badly_poisoned:
            self.status_counter += 1
            if self.status_counter > 15:
                self.status_counter = 15
            damage = self.maxHP // (16 // self.status_counter)
            if damage < 1:
                damage = 1
                self.currentHP -= damage
            else:
                self.currentHP -= damage

    def apply_burn(self):
        if self.burned:
            damage = self.maxHP // 8
            self.currentHP -= damage

    def apply_confusion(self):
        if self.confused:
            damage = ((((2 * (self.level) / 5 + 2) * self.attack * 40 / self.defense) / 50) + 2) * random.randint(85, 100) / 100
            self.currentHP -= damage
            print(int(damage))
