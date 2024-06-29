import duel
import QoL
import ASCII_text
import card_library
import card
import rogue

version_ID = 'v0.2.0a-alpha'

def reset_oro() :
    '''
    resets Ouroboros to level 1 if the player chooses to
    '''
    # set up variables
    [oro_level] = QoL.read_data([['ouroboros', 'attack']])

    # print the menu
    QoL.clear()
    print(version_ID)
    print('\n'*2)
    ASCII_text.print_title()
    print('\n'*6)
    print(QoL.center_justified('Orouboros level: ' + str(oro_level)))
    print('\n'*2)

    # get the user's choice
    reset_choice = input(QoL.center_justified('Are you sure you want to reset Ouroboros? y/n').rstrip() + ' ')

    # reset Ouroboros if the user chooses to
    if reset_choice == 'y' :
        QoL.write_data([(['ouroboros', 'attack'], 1), (['ouroboros', 'life'], 1)])
    
def reset_death_card() :
    '''
    resets the death card to "the dev's death card" if the player chooses to
    '''
    # set up variables
    current_death_cards_unfiltered = [card_library.PlyrDeathCard1(), card_library.PlyrDeathCard2(), card_library.PlyrDeathCard3()]
    current_death_cards = [death_card if not death_card.easter else card.BlankCard() for death_card in current_death_cards_unfiltered]
    
    # print the menu
    QoL.clear()
    print(version_ID)
    print('\n'*2)
    ASCII_text.print_title()
    print('\n'*4)
    print(QoL.center_justified('Current death cards: '))
    QoL.print_deck(current_death_cards, centered=True)
    print('\n'*2)

    # get the user's choice
    reset_choice = input(QoL.center_justified('Are you sure you want to delete your death cards? y/n').rstrip() + ' ')

    # reset the death card if the user chooses to
    if reset_choice == 'y' :
        data_to_write = [
                    (['death cards', 'first', 'name'], "Nebby"), # my death card
                    (['death cards', 'first', 'attack'], 2),
                    (['death cards', 'first', 'life'], 1),
                    (['death cards', 'first', 'cost'], 2),
                    (['death cards', 'first', 'sigils'], ["waterborne", ""]),
                    (['death cards', 'first', 'easter'], True),
                    (['death cards', 'second', 'name'], "Glaucus"), # Jacob's death card
                    (['death cards', 'second', 'attack'], 4),
                    (['death cards', 'second', 'life'], 1),
                    (['death cards', 'second', 'cost'], 3),
                    (['death cards', 'second', 'sigils'], ["airborne", "unkillable"]),
                    (['death cards', 'second', 'easter'], True),
                    (['death cards', 'third', 'name'], "A Possum"), # Raina's death card
                    (['death cards', 'third', 'attack'], 2),
                    (['death cards', 'third', 'life'], 3),
                    (['death cards', 'third', 'cost'], 3),
                    (['death cards', 'third', 'sigils'], ["corpse eater", "bees within"]),
                    (['death cards', 'third', 'easter'], True)
                ]
        QoL.write_data(data_to_write)

def set_deck_size() :
    '''
    sets the deck size to the player's choice between the current hand size and 101
    '''
    # set up variables
    invalid_choice = False
    out_of_range = False
    data_to_read = [
        ['settings', 'deck size'],
        ['settings', 'hand size']
    ]
    [deck_size, hand_size] = QoL.read_data(data_to_read)

    while True :
        # print the menu
        QoL.clear()
        print(version_ID)
        print('\n'*2)
        ASCII_text.print_title()
        print('\n'*6)
        deck_size_str = 'Current deck size: ' + str(deck_size)
        hand_size_str = 'Current hand size: ' + str(hand_size)
        hand_size_str += ' '*(len(deck_size_str) - len(hand_size_str))
        print(QoL.center_justified(deck_size_str))
        print()
        print(QoL.center_justified(hand_size_str))
        print()

        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            print()
            invalid_choice = False
        elif out_of_range :
            print(QoL.center_justified('Deck size must be greater than hand size and at most 100'))
            print()
            out_of_range = False
        else :
            print('\n')

        # get the user's choice
        choice = input(QoL.center_justified('Enter the new deck size: (press enter to cancel)').rstrip() + ' ')

        if choice == '' :
            return
        
        (is_int, choice) = QoL.reps_int(choice)
        match is_int :
            case False :
                invalid_choice = True
            
            case True if choice not in range(hand_size + 1, 101) :
                out_of_range = True

            case True :
                QoL.write_data([(['settings', 'deck size'], choice)])
                return

def set_hand_size() :
    '''
    sets the hand size to the player's choice between 1 and the current deck size
    '''
    # set up variables
    invalid_choice = False
    out_of_range = False
    data_to_read = [
        ['settings', 'deck size'],
        ['settings', 'hand size']
    ]
    [deck_size, hand_size] = QoL.read_data(data_to_read)

    while True :
        # print the menu
        QoL.clear()
        print(version_ID)
        print('\n'*2)
        ASCII_text.print_title()
        print('\n'*6)
        deck_size_str = 'Current deck size: ' + str(deck_size)
        hand_size_str = 'Current hand size: ' + str(hand_size)
        hand_size_str += ' '*(len(deck_size_str) - len(hand_size_str))
        print(QoL.center_justified(deck_size_str))
        print()
        print(QoL.center_justified(hand_size_str))
        print()

        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            print()
            invalid_choice = False
        elif out_of_range :
            print(QoL.center_justified('Hand size must be greater than 1 and less than the deck size'))
            print()
            out_of_range = False
        else :
            print('\n')

        # get the user's choice
        choice = input(QoL.center_justified('Enter the new hand size: (press enter to cancel)').rstrip() + ' ')

        if choice == '' :
            return
        
        (is_int, choice) = QoL.reps_int(choice)
        match is_int :
            case False :
                invalid_choice = True
            
            case True if choice not in range(2, deck_size) :
                out_of_range = True

            case True :
                QoL.write_data([(['settings', 'hand size'], choice)])
                return

def set_difficulty() :
    '''
    sets the difficulty to the player's choice, chosen from a list of difficulties
    '''
    def change_difficulty_data(difficulty_index) :
        '''
        sets the difficulty

        Arguments:
            difficulty_index: the new difficulty's index (int)
        '''
        def write_difficulty(name, number, median, var, strat, threshold) :
            data_to_write = [
                (['settings', 'difficulty', 'leshy median plays'], median),
                (['settings', 'difficulty', 'leshy plays variance'], var),
                (['settings', 'difficulty', 'leshy strat chance'], strat),
                (['settings', 'difficulty', 'leshy offense threshold'], threshold),
                (['settings', 'difficulty', 'current difficulty index'], number),
                (['settings', 'difficulty', 'current difficulty name'], name)
            ]

            QoL.write_data(data_to_write)
        
        match difficulty_index :
            case 0 :
                write_difficulty('Very Easy', 0, 1, 0, 40, 10)
            case 1 :
                write_difficulty('Easy', 1, 2, 0, 60, 5)
            case 2 :
                write_difficulty('Normal', 2, 2, 1, 75, 3)
            case 3 :
                write_difficulty('Hard', 3, 3, 2, 90, 3)
            case 4 :
                write_difficulty('Very Hard', 4, 4, 1, 100, 2)

    # set up variables
    invalid_choice = False
    [current_difficulty_index] = QoL.read_data([['settings', 'difficulty', 'current difficulty index']])
    difficulty_key = [' (CURRENT)' if i == current_difficulty_index else ' '*10 for i in range(5)]

    while True :
        # print the menu
        QoL.clear()
        print(version_ID)
        print('\n'*2)
        ASCII_text.print_title()
        print('\n'*5)
        print(QoL.center_justified('1. Very Easy' + difficulty_key[0]))
        print(QoL.center_justified('2.   Easy' + difficulty_key[1] + ' '*3))
        print(QoL.center_justified('3.  Normal' + difficulty_key[2] + ' '*2))
        print(QoL.center_justified('4.   Hard' + difficulty_key[3] + ' '*3))
        print(QoL.center_justified('5. Very Hard' + difficulty_key[4]))
        print()

        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            print()
            invalid_choice = False
        else :
            print('\n')
        
        # get the user's choice
        choice = input(QoL.center_justified('Enter the new difficulty: (press enter to cancel)').rstrip() + ' ')

        if choice == '' :
            return
        
        (is_int, choice) = QoL.reps_int(choice, -1)
        match is_int :
            case False :
                invalid_choice = True
            case True if choice not in range(5) :
                invalid_choice = True
            case True :
                change_difficulty_data(choice)
                return
        
def settings() :
    '''
    allows the player to change the difficulty, deck size, hand size, and reset Ouroboros
    '''
    def print_settings_options() :
        '''
        prints the settings options
        '''
        print(QoL.center_justified('Settings   '))
        print(QoL.center_justified('='*25 + ' '*4))
        print(QoL.center_justified('1.  Change difficulty     '))
        print(QoL.center_justified('2.  Change deck size      '))
        print(QoL.center_justified('3.  Change hand size      '))
        print(QoL.center_justified('4.  Reset Ouroboros      '))
        print(QoL.center_justified('5.  Delete death card    '))

    # set up variables
    invalid_choice = False

    while True :
        # print the menu
        QoL.clear()
        print(version_ID)
        print('\n'*2)
        ASCII_text.print_title()
        print('\n'*5)
        print_settings_options()
        print()

        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            print()
            invalid_choice = False
        else :
            print('\n')
        
        # get the user's choice
        choice = input(QoL.center_justified('Choose an option: (press enter to cancel)').rstrip() + ' ')

        match choice :
            case '' : # quit to main menu
                return
            case '1' :
                set_difficulty()
            case '2' :
                set_deck_size()
            case '3' :
                set_hand_size()
            case '4' :
                reset_oro()
            case '5' :
                reset_death_card()
            case _ :
                invalid_choice = True

def main_menu() :
    '''
    displays the main menu and allows the player to start a game, change settings, or exit the game
    '''
    # set up variables
    invalid_choice = False

    while True :
        # print the menu
        QoL.clear()
        print(version_ID)
        print('\n'*2)
        ASCII_text.print_title()
        print('\n'*6)
        print(QoL.center_justified('1.  Start a game      '))
        print()
        print(QoL.center_justified('2.  Play a round      '))
        print()
        print(QoL.center_justified('3.    Settings        '))
        print()
        print(QoL.center_justified('4.      Quit          '))
        print()

        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            print()
            invalid_choice = False
        else :
            print('\n')

        # get the user's choice
        choice = input(QoL.center_justified('Choose an option:' + ' '*3).rstrip() + ' ')

        match choice :
            case '1' :
                rogue.main()
            case '2' :
                data_to_read = [
                    ['settings', 'deck size'],
                    ['settings', 'hand size'],
                    ['settings', 'difficulty', 'leshy median plays'],
                    ['settings', 'difficulty', 'leshy plays variance'],
                    ['settings', 'difficulty', 'leshy strat chance'],
                    ['settings', 'difficulty', 'leshy offense threshold']
                ]
                [deck_size, hand_size, play_median, play_var, opp_strat, opp_threshold] = QoL.read_data(data_to_read)

                duel.main(deck_size, hand_size, play_median, play_var, opp_strat, opp_threshold)
            case '3' :
                settings()
            case '4' :
                exit()
            case _ :
                invalid_choice = True

if __name__ == '__main__' :
    main_menu()