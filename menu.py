import duel
import QoL
import ASCII_text

version_ID = 'v0.1.3-alpha'

choice_text = 'Choose an option:'

def menu_center(text, width=24) :
    '''
    centers text for the menu, adding a space if the text ends with a colon, and spacing out from numbering (honestly don't quite understand this one, but it works?) 

    Arguments:
        text: the text to center (str)
        width: the width of the menu, defaults to 24 (int)
    
    Returns:
        the centered text (str)
    '''
    og_text = text
    numbered = False
    shift_left = 0
    if text[1] == '.' :
        text_start = text[:2]
        text = text[2:].lstrip()
        numbered = True
        shift_left = 1
    if len(text) < width :
        text = ' '*((width - len(text)) // 2 - shift_left) + text + ' '*(width - len(text) + shift_left)
    elif len(text) > width :
        text = ' '*((width - len(text)) - shift_left) + text + ' '*((width - len(text)) // 2 + shift_left)
    if og_text[-1] == ':' :
        return QoL.center_justified(text).rstrip() + ' '
    elif numbered :
        return QoL.center_justified(text_start + text)
    else :
        return QoL.center_justified(text)

def reset_oro() :
    '''
    resets the attack and life of Ouroboros to 1
    '''
    QoL.write_file('data.txt', 'Descryption_Data/data.txt', ['1', '1'])

def set_deck_size(size) :
    '''
    sets the deck size

    Arguments:
        size: the new deck size (int)
    '''
    [junk, hand_size, play_median, play_var, opp_strat, opp_threshold] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
    QoL.write_file('config.txt', 'Descryption_Data/config.txt', [str(size), hand_size, play_median, play_var, opp_strat, opp_threshold])

def set_hand_size(size) :
    '''
    sets the hand size

    Arguments:
        size: the new hand size (int)
    '''
    [deck_size, junk, play_median, play_var, opp_strat, opp_threshold] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')[0]
    QoL.write_file('config.txt', 'Descryption_Data/config.txt', [deck_size, str(size), play_median, play_var, opp_strat, opp_threshold])

def set_difficulty(difficulty) :
    '''
    sets the difficulty

    Arguments:
        difficulty: the new difficulty (int)
    '''
    if difficulty == 0 :
        play_median = '1'
        play_var = '0'
        opp_strat = '40'
        opp_threshold = '10'
    elif difficulty == 1 :
        play_median = '2'
        play_var = '0'
        opp_strat = '60'
        opp_threshold = '5'
    elif difficulty == 2 :
        play_median = '2'
        play_var = '1'
        opp_strat = '75'
        opp_threshold = '3'
    elif difficulty == 3 :
        play_median = '3'
        play_var = '2'
        opp_strat = '90'
        opp_threshold = '3'
    elif difficulty == 4 :
        play_median = '4'
        play_var = '1'
        opp_strat = '100'
        opp_threshold = '2'

    [deck_size, hand_size] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')[0:2]
    QoL.write_file('config.txt', 'Descryption_Data/config.txt', [deck_size, hand_size, play_median, play_var, opp_strat, opp_threshold])

def print_settings_options() :
    '''
    prints the settings options
    '''
    print(QoL.center_justified('Settings   '))
    print(QoL.center_justified('='*26 + '   '))
    print(QoL.center_justified('1.  Change difficulty     '))
    print(QoL.center_justified('2.  Change deck size      '))
    print(QoL.center_justified('3.  Change hand size      '))
    print(QoL.center_justified('4.   Reset Ouroboros     '))
    print(QoL.center_justified('5. Return to main menu   '))

def settings() :
    '''
    allows the player to change the difficulty, deck size, hand size, and reset Ouroboros
    '''
    bad_input = True
    invalid_choice = False
    while bad_input :
        QoL.clear()
        print(version_ID)
        print('\n'*2)
        ASCII_text.print_title()
        [deck_size, hand_size, play_median, play_var, opp_strat, opp_threshold] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
        print('\n'*5)
        print_settings_options()
        print('\n'*3)
        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            invalid_choice = False
        choice = input(menu_center(choice_text))
        # change difficulty
        if choice == '1' :
            bad_choice = True
            invalid_difficulty = False
            while bad_choice :
                QoL.clear()
                print(version_ID)
                print('\n'*2)
                ASCII_text.print_title()
                print('\n'*5)
                difficulty_dict = {0:40, 1:60, 2:75, 3:90, 4:100}
                current_difficulty = -1
                difficulty_key = []
                for n in difficulty_dict :
                    if difficulty_dict[n] == int(opp_strat) :
                        difficulty_key.append(' (CURRENT)')
                        current_difficulty = n
                    else :
                        difficulty_key.append(' '*10)
                print(QoL.center_justified('1. Very Easy' + difficulty_key[0]))
                print(QoL.center_justified('2.   Easy' + difficulty_key[1] + '   '))
                print(QoL.center_justified('3.  Normal' + difficulty_key[2] + '  '))
                print(QoL.center_justified('4.   Hard' + difficulty_key[3] + '   '))
                print(QoL.center_justified('5. Very Hard' + difficulty_key[4]))
                print('\n'*3)
                if invalid_difficulty :
                    print(QoL.center_justified('Invalid difficulty'))
                    invalid_difficulty = False
                difficulty = input(QoL.center_justified('Enter the new difficulty: (press enter to cancel)').rstrip() + ' ')
                if difficulty == '' :
                    break
                try :
                    difficulty = int(difficulty)
                except ValueError :
                    difficulty = -1
                if difficulty >= 1 and difficulty <= 5 :
                    if difficulty == current_difficulty + 1 :
                        bad_choice = False
                    else :
                        set_difficulty(difficulty - 1)
                        bad_choice = False
                else :
                    invalid_difficulty = True
        # change deck size
        elif choice == '2' :
            bad_choice = True
            invalid_deck_size = False
            while bad_choice :
                QoL.clear()
                print(version_ID)
                print('\n'*2)
                ASCII_text.print_title()
                print('\n'*5)
                print(QoL.center_justified('Current deck size: ' + deck_size))
                print(QoL.center_justified('Current hand size: ' + hand_size))
                print('\n'*3)
                if invalid_deck_size :
                    print(QoL.center_justified('Invalid deck size'))
                    invalid_deck_size = False
                new_size = input(QoL.center_justified('Enter the new deck size: (press enter to cancel)').rstrip() + ' ')
                if new_size == '' :
                    break
                try :
                    new_size = int(new_size)
                except ValueError :
                    new_size = -1
                if new_size > int(hand_size) and new_size <= 100 :
                    set_deck_size(new_size)
                    bad_choice = False
                else :
                    invalid_deck_size = True
        # change hand size
        elif choice == '3' :
            bad_choice = True
            invalid_hand_size = False
            while bad_choice :
                QoL.clear()
                print(version_ID)
                print('\n'*2)
                ASCII_text.print_title()
                print('\n'*5)
                print(QoL.center_justified('Current deck size: ' + deck_size))
                print(QoL.center_justified('Current hand size: ' + hand_size))
                print('\n'*3)
                if invalid_hand_size :
                    print(QoL.center_justified('Invalid hand size'))
                    invalid_hand_size = False
                new_size = input(QoL.center_justified('Enter the new hand size: (press enter to cancel)').rstrip() + ' ')
                if new_size == '' :
                    break
                try :
                    new_size = int(new_size)
                except ValueError :
                    new_size = -1
                if new_size < int(deck_size) and new_size <= 15 :
                    set_hand_size(new_size)
                    bad_choice = False
                else :
                    invalid_hand_size = True
        # reset Ouroboros
        elif choice == '4' :
            QoL.clear()
            print(version_ID)
            print('\n'*2)
            ASCII_text.print_title()
            print('\n'*5)
            print_settings_options()
            print('\n'*3)
            reset_choice = input(QoL.center_justified('Are you sure you want to reset Ouroboros? y/n').rstrip() + ' ')
            if reset_choice == 'y' :
                reset_oro()
            else :
                continue
        # quit to main menu
        elif choice == '5' :
            return
        else :
            invalid_choice = True

def main_menu() :
    '''
    displays the main menu
    '''
    bad_input = True
    invalid_choice = False
    while bad_input :
        QoL.clear()
        print(version_ID)
        print('\n'*2)
        ASCII_text.print_title()
        print('\n'*6)
        # print(QoL.center_justified('Main Menu  '))
        # print(QoL.center_justified('================  '))
        print(QoL.center_justified('1.  Start a game      '))
        print()
        print(QoL.center_justified('2.    Settings        '))
        print()
        print(QoL.center_justified('3.      Quit          '))
        print('\n'*3)
        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            invalid_choice = False
        choice = input(menu_center(choice_text))
        if choice == '1' :
            [deck_size, hand_size, play_median, play_var, opp_strat, opp_threshold] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
            duel.main(int(deck_size), int(hand_size), Leshy_play_count_median=int(play_median), Leshy_play_count_variance=int(play_var), Leshy_in_strategy_chance=int(opp_strat), Leshy_strat_change_threshold=int(opp_threshold))
        elif choice == '2' :
            settings()
        elif choice == '3' :
            exit()
        else :
            invalid_choice = True

if __name__ == '__main__' :
    main_menu()