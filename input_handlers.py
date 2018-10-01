import libtcodpy as libtcod


from game_states import GameStates
from fighter import Fighter
from initialize_new_game import get_constants, get_game_variables
def handle_keys(player,key, game_state):

    print("---> key: %s    state: %s" % (key,game_state))

    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)
    elif game_state == GameStates.CHARACTER_CREATION:
        return handle_character_creation(key)
    elif game_state == GameStates.GENDER_SELECTION:
        return handle_gender_selection(key)
    elif game_state == GameStates.JOB_SELECTION:
        return handle_job_selection(key,player)
    elif game_state == GameStates.SHOW_SKILL_MENU:
        return handle_skill_keys(key)
    elif game_state == GameStates.SKILL_TARGETING:
        return handle_targeting_keys(key)

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # Movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'z':
        return {'wait': True}

    if key_char == 'g':
        return {'pickup': True}
    if key_char == 's':
        return {'use_skills': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    elif key.vk == libtcod.KEY_ENTER:
        return {'take_stairs': True}

    elif key.text == '<':
        return {'take_upstairs': True}

    elif key_char == 'c':
        return {'show_character_screen': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}
    if key_char == 's':
        return {'use_skills': True}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_main_menu(key, player,):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key_char == 'd':
        return {'new_game': True}
    return {}


def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}

def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_skill_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'skill_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_character_creation(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'character_creation': 'mern'}
        elif key_char == 'b':
            return {'character_creation': 'avis'}
        elif key_char == 'c':
            return {'character_creation': 'lepra'}
        elif key_char == 'd':
            return {'character_creation': 'giant'}
        elif key_char == 'e':
            return {'character_creation': 'change'}
        elif key_char == 'f':
            return {'character_creation': 'fae'}

    return {}


def handle_job_selection(key, player):

    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'job': 'pri'}
        elif key_char == 'b':
            return {'job': 'fig'}
        elif key_char == 'c':
            return {'job': 'thi'}
        elif key_char == 'd':
            return {'job': 'wiz'}
        if player.fighter.thief_level >= 1 and key_char == 'e':
            return {'job': 'psy'}

    return {}

def handle_gender_selection(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'gender': 'm'}
        elif key_char == 'b':
            return {'gender': 'f'}
        elif key_char == 'c':
            return {'gender': 'a'}

    return {}


def handle_character_screen(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
