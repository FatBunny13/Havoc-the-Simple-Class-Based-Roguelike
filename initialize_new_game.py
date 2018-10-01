import libtcodpy as libtcod
import random

from components.equipment import Equipment
from components.equippable import Equippable
from components.item import Item
from fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.skills import Skills
from components.skill import Skill


from entity import Entity

from equipment_slots import EquipmentSlots

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap
from character import Gender




from render_functions import RenderOrder


def get_constants():
    window_title = 'Caves of Havoc'

    screen_width = 100
    screen_height = 60

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 78
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    maze_max_size = 2
    maze_min_size = 2
    max_maze_rooms = 20

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 4

    min_monsters_per_room = 1
    min_items_per_room = 1


    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(101, 101, 101),
        'light_ground': libtcod.Color(148, 158, 148)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'maze_max_size': maze_max_size,
        'maze_min_size': maze_min_size,
        'max_maze_rooms': max_maze_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'min_monsters_per_room': min_monsters_per_room,
        'min_items_per_room': min_items_per_room,
        'colors': colors
    }

    return constants


def get_game_variables(constants):
    fighter_component = Fighter(hp=100, defense=1, power=5, agility=1, job = 0, mana = 10, nutrition=500, base_psyche = 2, starvation_bonus = 0)
    inventory_component = Inventory(26)
    skills_component = Skills(15)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component, skills=skills_component)
    entities = [player]

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4)
    item_component = Item(use_function=None)
    dagger = Entity(0, 0, '/', libtcod.sky, 'Carving Knife', equippable=equippable_component,item=item_component)
    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1, agility_bonus=-1)
    item_component = Item(use_function=None)
    buckler = Entity(0, 0, '{', libtcod.sky, 'Buckler', equippable=equippable_component,item=item_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)
    player.inventory.add_item(buckler)
    player.equipment.toggle_equip(buckler)
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.CHARACTER_CREATION
    ggender = Gender.male

    return player, entities, game_map, message_log, game_state, ggender
