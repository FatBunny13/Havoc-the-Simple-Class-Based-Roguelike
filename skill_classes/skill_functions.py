import tcod as libtcod

from entity import Entity, SkillEntity
from item_functions import cast_charm
from components.skill import Skill
from game_messages import Message
from initialize_new_game import get_constants, get_game_variables
from render_functions import clear_all, render_all

class Charm(Skill):
    skill_component = Skill(use_function=cast_charm, hunger_cost=10, skill_targeting=True,
                            targeting_message=Message(
                                'Left-click a target tile to charm them, or right-click to cancel.',
                                libtcod.light_cyan))
    charm = SkillEntity(' ', libtcod.red, 'Charm Enemy', skill=skill_component)

    def use(self, skill_entity, **kwargs):
        results = []

        skill_component = Skill(use_function=cast_charm)

        if skill_component.use_function is None:
            results.append({'message': Message('You cannot use that skill.'.format(skill_entity.name), libtcod.yellow)})
        else:
            if skill_component.skill_targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'skill_targeting': Skill})
            else:
                kwargs = {**skill_entity.function_kwargs, **kwargs}
                skill_use_results = skill_component.use_function(self.owner, **kwargs)

                for skill_use_result in skill_use_results:
                    if skill_use_result.get('used'):
                       self.remove_skill()

                    results.extend(skill_use_results)

        return results
