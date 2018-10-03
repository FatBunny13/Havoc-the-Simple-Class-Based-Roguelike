import libtcodpy as libtcod
from random import randint

from components.ai import BasicMonster, SlimeMonster, ShrubMonster,CharmedMonster
from components.equipment import EquipmentSlots, Equipment
from components.equippable import Equippable
from fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from components.upstair import Upstairs

from entity import Entity

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal, throw_shurikin, eat

from map_objects.rectangle import Rect
from map_objects.tile import Tile

from random_utils import from_dungeon_level, random_choice_from_dict

from render_functions import RenderOrder


class GameMap:

    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size,max_maze_rooms,maze_min_size, maze_max_size, map_width, map_height, player, entities):
        if self.dungeon_level == 0:
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_maze_rooms):
            # random width and height
                w = randint(maze_min_size, maze_max_size)
                h = randint(maze_min_size, maze_max_size)
            # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                    self.create_room(new_room)

                # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                    # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                        # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_entities(new_room, entities)

                # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

        else:
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
            # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                    self.create_room(new_room)

                # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                    # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                        # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_entities(new_room, entities)

                # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

        upstairs_component = Upstairs(self.dungeon_level + 1)
        up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Stairs',
                             render_order=RenderOrder.UPSTAIRS, stairs=upstairs_component)
        entities.append(up_stairs)

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([ [1, 0],[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[0, 0], [3, 1]], self.dungeon_level)
        min_items_per_room = from_dungeon_level([[1, 0]], self.dungeon_level)

        # Get a random number of monsters
        number_of_monsters = randint(1, max_monsters_per_room)

        # Get a random number of items
        number_of_items = randint(0, max_items_per_room)
        monster_chances = {
                'orc': 80,
                'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level),
                'fairy': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level),
                'slime': from_dungeon_level([[20, 3], [30, 5], [60, 7]], self.dungeon_level),
                'shrub': from_dungeon_level([[15, 0],[0, 1]], self.dungeon_level),
                'stone': from_dungeon_level([[5, 2], [10, 4]], self.dungeon_level)}



        item_chances = {
            'healing_potion': 35,
            'ration': 10,
            'sword': from_dungeon_level([[10, 1]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lance': from_dungeon_level([[15, 3]], self.dungeon_level),
            'rbrace': from_dungeon_level([[15, 3]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=2, power=5, xp=5000, agility=1,mana = 0,base_psyche = 0)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                elif monster_choice == 'troll':
                    fighter_component = Fighter(hp=50, defense=3, power=6, xp=100, agility=1,mana = 0,base_psyche = 0)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Cave Troll', blocks=True, fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                elif monster_choice == 'stone':
                    fighter_component = Fighter(hp=10, defense=25, power=8, xp=160, agility= -1,mana = 0,base_psyche = 0)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'G', libtcod.gray, 'Stone Golem', blocks=True, fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                elif monster_choice == 'slime':
                    fighter_component = Fighter(hp=10, defense=25, power=8, xp=160, agility= 2,mana = 0,base_psyche = 0)
                    ai_component = SlimeMonster()

                    monster = Entity(x, y, 's', libtcod.green, 'Slime', blocks=True, fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                elif monster_choice == 'shrub':
                    fighter_component = Fighter(hp=1, defense=0, power=5, xp=160, agility= 3,mana = 0,base_psyche = 0)
                    ai_component = ShrubMonster()

                    monster = Entity(x, y, '"', libtcod.desaturated_green, 'Thorn-Shrub', blocks=True, fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=10, defense=1, power=2, xp=100, agility=4,mana = 0,base_psyche = 0)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'f', libtcod.black, 'Fairy', blocks=True,fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)


                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1, room.x2)
            y = randint(room.y1, room.y2)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'ration':
                    item_component = Item(use_function=eat, amount=40)
                    item = Entity(x, y, '%', libtcod.brown, 'Ration', render_order=RenderOrder.ITEM,
                              item=item_component)
                elif item_choice == 'sword':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND and EquipmentSlots.OFF_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.white, 'Sword', equippable=equippable_component,item=item_component)
                elif item_choice == 'lance':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6, defense_bonus=-5)
                    item_component = Item(use_function=None)
                    item = Entity(x, y, '/', libtcod.white, 'Lance', equippable=equippable_component,item=item_component)
                elif item_choice == 'shield':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component,item=item_component)
                elif item_choice == 'rbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.black, 'Right Bracelet of Defense', equippable=equippable_component,item=item_component)
                elif item_choice == 'rlightbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=1, agility_bonus=-1,)
                    item = Entity(x, y, '[', libtcod.black, 'Rotten Right Bracelet',
                                  equippable=equippable_component,item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '?', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '?', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '?', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(use_function=throw_shurikin, damage=20, maximum_range=10)
                    item = Entity(x, y, '+', libtcod.gray, 'Shuriken', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def scrolling_map(p, hs, s, m):
    #Get the position of the camera in a scrolling map    
        
        if p < hs:
            return 0
        elif p >= m - hs:
            return m - s
        else:
            return p - hs

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities

    def previous_floor(self, player, message_log, constants):
        self.dungeon_level -= 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'],player, entities,)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities
