import libtcodpy as libtcod
import math

from game_messages import Message
from item_functions import heal

class Job:
    def __init__(self,psychic_levels=0):
        self.psychic_levels = psychic_levels

class Fighter:
    def __init__(self, hp, defense, power, agility,mana,base_psyche,starvation_bonus = 0,nutrition=0, gender=0,stealthed=0, race=0, xp=0, job=1, priest_level=0, fighter_level=0, thief_level=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.base_agility = agility
        self.xp = xp
        self.race = race
        self.gender = gender
        self.job = job
        self.priest_level = priest_level
        self.fighter_level = fighter_level
        self.thief_level = thief_level
        self.base_max_mana = mana
        self.mana = mana
        self.nutrition = nutrition
        self.stealthed = stealthed
        self.base_psyche = base_psyche
        self.starvation_bonus = starvation_bonus

    @property
    def max_mana(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_mana_bonus
        else:
            bonus = 0

        return self.base_max_mana + bonus

    @property
    def agility(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.agility_bonus
        else:
            bonus = 0

        return self.base_agility + bonus

    @property
    def psyche(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.psyche_bonus
        else:
            bonus = 0

        return self.base_psyche + bonus
        
    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return (self.base_defense + self.agility) / 2 + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def take_psychic_damage(self, amount):
        results = []

        self.hp -= (amount + self.starvation_bonus)

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def take_mana_damage(self, mana_cost):

        self.mana -= mana_cost

    def take_hunger_damage(self, hunger_cost):

        self.nutrition -= hunger_cost

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def eat(self, amount):
        self.nutrition += amount
    
    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        elif damage > 2:
            results.append({'message': Message('{0} attacks {1} for {2} hit points. Its a critical strike!'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results
