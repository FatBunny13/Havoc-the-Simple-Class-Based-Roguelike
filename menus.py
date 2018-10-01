import libtcodpy as libtcod

from character import Gender

def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)

def skill_use_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.skills.number_of_skills) == 0:
        options = ['You have no skills.']
    else:
        options = [skill.name for skill in player.skills.number_of_skills]




    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'Caves of Havoc')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 13) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'In the year of 1002 the village of Havoc flucuated between winter and summer.')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 12) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'The weather went from heat waves one week to blizzards the next')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 11) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'The Court Wizard discovered the problem. The temples of Spring and Autumn have dissapered!')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 10) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'The only way to recover them is by getting the Orb of Etheria located in the Caves of Havoc.')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 9) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'The Orb of Etheria is in the grasps of the Snakes. After it was stolen by their god Rukshala')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 8) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'The Duchess of Havoc sent the banshee High-Bloodmaster named Aern of the necromancers guild.')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 7) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'And the Avis Shadowlord named Purron of the thieves guild.')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 7) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'The party was lead by a human scout named Oliviere,')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 6) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'They have never returned.')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 5) + 1, libtcod.BKGND_NONE, libtcod.CENTER,
                             'You have decided to venture into the Caves of Havoc. It cant be too hard! Find the Orb and face whatever horrors you find!')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'Coding by Alfonso Abraham. Additional Coding and Bugfixing by Julie Abraham.')

    menu(con, '', ['Start a game','Continue last game', 'Quit'], 24, screen_width, screen_height)
    
def character_creation_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Mern'.format(player.fighter.max_hp),
    		   'Avis '.format(player.fighter.max_hp),
    		   'Leprachaun'.format(player.fighter.max_hp),
    		   'Giant'.format(player.fighter.max_hp),
    		   'Changeling'.format(player.fighter.max_hp),
    'Nymph'.format(player.fighter.max_hp)]



    menu(con, header, options, menu_width, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Defense (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)

def gender_selection_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Male'.format(player.fighter.max_hp),
               'Female '.format(player.fighter.max_hp),
               'Agender'.format(player.fighter.max_hp),]

    menu(con, header, options, menu_width, screen_width, screen_height)


def job_selection_menu(con, header, player, menu_width, screen_width, screen_height):

    options = ['Priest'.format(player.fighter.max_hp),
               'Fighter '.format(player.fighter.max_hp),
               'Thief'.format(player.fighter.max_hp),
               'Magician'.format(player.fighter.max_hp),]

    if player.fighter.thief_level >= 1:
        options.append('Psychic')


    menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))
    libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Race: {0}'.format(player.fighter.race))
    libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Gender: {0}'.format(Gender.male))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
