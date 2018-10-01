import libtcodpy as libtcod

from enum import Enum

from game_states import GameStates

from menus import character_screen, inventory_menu, character_creation_menu, gender_selection_menu, job_selection_menu, skill_selection_menu


class RenderOrder(Enum):
    STAIRS = 1
    UPSTAIRS = 2
    CORPSE = 3
    ITEM = 4
    ACTOR = 5


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, game_state):
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors['light_wall'], libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors['light_ground'], libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors['dark_wall'], libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors['dark_ground'], libtcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))

    if player.fighter.race == 1:
        libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Race: Mern'.format(player.fighter.race))

    if player.fighter.race == 2:
        libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Race: Avis'.format(player.fighter.race))

    if player.fighter.race == 3:
        libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Race: Leprechaun'.format(player.fighter.race))

    if player.fighter.race == 4:
        libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Race: Giant'.format(player.fighter.race))

    if player.fighter.race == 5:
        libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Race: Changeling'.format(player.fighter.race))

    if player.fighter.race == 6:
        libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Race: Dark Fae'.format(player.fighter.race))

    if player.fighter.gender == 1:
        libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Gender: Male'.format(player.fighter.race))

    if player.fighter.gender == 2:
        libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Gender: Female'.format(player.fighter.race))

    if player.fighter.gender == 3:
        libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Gender: Agender'.format(player.fighter.race))

    if player.fighter.job == 1:
        libtcod.console_print_ex(panel, 98, 5, libtcod.BKGND_NONE, libtcod.RIGHT,
                                 'Job: Priest'.format(player.fighter.job))

    if player.fighter.job == 2:
        libtcod.console_print_ex(panel, 98, 5, libtcod.BKGND_NONE, libtcod.RIGHT,
                                 'Job: Fighter'.format(player.fighter.job))

    if player.fighter.job == 3:
        libtcod.console_print_ex(panel, 98, 5, libtcod.BKGND_NONE, libtcod.RIGHT,
                                 'Job: Thief'.format(player.fighter.job))

    if player.fighter.job == 0:
        libtcod.console_print_ex(panel, 98, 5, libtcod.BKGND_NONE, libtcod.RIGHT,
                                 'Job: Peasant'.format(player.fighter.job))


    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_CREATION:
        character_creation_menu(con, 'Brave peasant! What is your race!:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.GENDER_SELECTION:
        gender_selection_menu(con, 'Brave peasant! What is your gender!:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.JOB_SELECTION:
        job_selection_menu(con, 'Congratulations! You have gained a level! Pick a job!:', player, 40, screen_width, screen_height)

    if game_state == GameStates.SHOW_INVENTORY:
        skill_selection_title = 'Press the key next to the skill you want to use. Use Esc to quit\n'

        inventory_menu(con, skill_selection_title, player, 50, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored) or (entity.upstairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
