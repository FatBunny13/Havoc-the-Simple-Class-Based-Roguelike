import libtcodpy as libtcod

from random import randint

from game_messages import Message


class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                if target.fighter.stealthed == 0:
                    monster.move_astar(target, entities, game_map)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        else:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

        return results

class CharmedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        closest_distance = 10
        if self.number_of_turns > 0:
            for entity in entities:
                if entity.ai and entity != monster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
                    distance = monster.distance_to(entity)

                    if distance < closest_distance:
                        target = entity
                        closest_distance = distance
                        if monster.distance_to(target) >= 2:
                                monster.move_astar(target, entities, game_map)
                        elif target.fighter.hp > 0:
                            attack_results = monster.fighter.attack(target)
                            results.extend(attack_results)
                    else:
                        random_x = self.owner.x + randint(0, 2) - 1
                        random_y = self.owner.y + randint(0, 2) - 1

                        if random_x != self.owner.x and random_y != self.owner.y:
                            self.owner.move_towards(random_x, random_y, game_map, entities)
            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer charmed!'.format(self.owner.name), libtcod.red)})

        return results



class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results

class SlimeMonster:
    def take_turn(self, target, fov_map, game_map, entities,):
        results = []
        monster = self.owner

        random_x = self.owner.x + randint(0, 2) - 1
        random_y = self.owner.y + randint(0, 2) - 1
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

                if target.fighter.hp > 0 and monster.distance_to(target) == 1:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)

        return results

class ShrubMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results