import duel
import QoL
import ASCII_text

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
    [junk, hand_size] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
    QoL.write_file('config.txt', 'Descryption_Data/config.txt', [str(size), hand_size])

def set_hand_size(size) :
    '''
    sets the hand size

    Arguments:
        size: the new hand size (int)
    '''
    [deck_size, junk] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
    QoL.write_file('config.txt', 'Descryption_Data/config.txt', [deck_size, str(size)])

def settings() :
    '''
    allows the player to change the deck size and hand size as well as reset Ouroboros
    '''
    bad_input = True
    invalid_choice = False
    while bad_input :
        QoL.clear()
        print('\n'*3)
        print(ASCII_text.title)
        [deck_size, hand_size] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
        print('\n'*5)
        print(QoL.center_justified('Settings   '))
        print(QoL.center_justified('==========   '))
        print(QoL.center_justified('1.  Change deck size      '))
        print(QoL.center_justified('2.  Change hand size      '))
        print(QoL.center_justified('3.   Reset Ouroboros     '))
        print(QoL.center_justified('4. Return to main menu   '))
        print('\n'*3)
        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            invalid_choice = False
        choice = input(QoL.center_justified('Choose a menu to view:   ').rstrip() + ' ')
        if choice == '1' :
            bad_choice = True
            invalid_deck_size = False
            while bad_choice :
                QoL.clear()
                print(ASCII_text.title)
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
        elif choice == '2' :
            bad_choice = True
            invalid_hand_size = False
            while bad_choice :
                QoL.clear()
                print(ASCII_text.title)
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
        elif choice == '3' :
            QoL.clear()
            print(ASCII_text.title)
            [deck_size, hand_size] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
            print('\n'*5)
            print(QoL.center_justified('Settings   '))
            print(QoL.center_justified('==========   '))
            print(QoL.center_justified('1.  Change deck size      '))
            print(QoL.center_justified('2.  Change hand size      '))
            print(QoL.center_justified('3.   Reset Ouroboros     '))
            print(QoL.center_justified('4. Return to main menu   '))
            print('\n'*3)
            reset_choice = input(QoL.center_justified('Are you sure you want to reset Ouroboros? y/n').rstrip() + ' ')
            if reset_choice == 'y' :
                reset_oro()
            else :
                continue
        elif choice == '4' :
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
        print('\n'*3)
        print(ASCII_text.title)
        print('\n'*5)
        print(QoL.center_justified('Main Menu   '))
        print(QoL.center_justified('==========   '))
        print(QoL.center_justified('1.  Start a game      '))
        print(QoL.center_justified('2.    Settings        '))
        print(QoL.center_justified('3.      Quit          '))
        print('\n'*3)
        if invalid_choice :
            print(QoL.center_justified('Invalid choice'))
            invalid_choice = False
        choice = input(QoL.center_justified('Choose a menu to view:   ').rstrip() + ' ')
        if choice == '1' :
            [deck_size, hand_size] = QoL.read_file('config.txt', 'Descryption_Data/config.txt')
            duel.main(int(deck_size), int(hand_size))
        elif choice == '2' :
            settings()
        elif choice == '3' :
            exit()
        else :
            invalid_choice = True

if __name__ == '__main__' :
    main_menu()