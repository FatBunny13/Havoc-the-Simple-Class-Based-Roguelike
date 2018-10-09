import libtcodpy as libtcod
from dataclasses import dataclass, field
from typing import List
from game_messages import Message
from entity import Entity, SkillEntity
from components.skill import Skill




class Skills:

    def __init__(self, capacity):

        self.capacity = int(capacity)
        self.skill_list = list()

    def __eq__(self, other):
        equivalent = True
        if self.skill != other.skill:
            equivalent = False
        return equivalent

    def add_skill(self, skill):
        results = list()
        if( len(self.skill_list) >= self.capacity):
            results.append({
                'item_added': None,
                'message': Message('You cannot learn anymore skills.', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': skill,
                'message': Message('You have learned the skill {0}!'.format(skill.name), libtcod.blue)
            })

            self.skill_list.append(skill)

        return results

    