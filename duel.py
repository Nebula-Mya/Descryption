import card
import card_library
import deck
import field
import sigils
import os
import ASCII_text

def choose_and_play(field) :
    '''
    the whole process of choosing a card to play and playing it
    player can choose to go back at any time, and if so nothing will happen

    Arguments:
        field: the field object to play the card on (field object)
    '''
    bad_input = True
    second_bad_input = False
    invalid_index = False
    while bad_input :
        field.print_full_field()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        play_index = input('Card to play: (press enter to go back) ')
        if play_index == '' :
            break
        try :
            play_index = int(play_index) - 1
        except :
            play_index = len(field.hand) + 1
        if play_index in range(len(field.hand)) :
            bad_input = False
            os.system('clear')
            field.print_field()
            print(' '*5 + 'Card to play:')
            field.hand[play_index].explain()
            second_bad_input = True
        else :
            invalid_index = True
        while second_bad_input and not bad_input:
            zone_to_play = input('Zone to play: (press enter to go back) ')
            if zone_to_play == '' :
                bad_input = True
                break
            try :
                zone_to_play = int(zone_to_play)
            except :
                zone_to_play = 0
            if zone_to_play in range(1, 6) :
                second_bad_input = False
                if not field.play_card(play_index, zone_to_play) :
                    bad_input = True
                    second_bad_input = False
            else :
                print('Invalid zone.')

def choose_draw(field) :
    '''
    the whole process of choosing a card to draw and drawing it

    Arguments:
        field: the field object to draw the card to (field object)
    '''
    bad_input = True
    while bad_input :
        field.print_field()
        deck_number = int(input('Draw from main deck (1) or resource deck (2): '))
        if deck_number == 1 :
            card = field.draw('main')
            bad_input = False
        elif deck_number == 2 :
            card = field.draw('resource')
            bad_input = False
        else :
            print('Invalid deck number.')

def winner_check(field) :
    '''
    checks if the game is over

    Arguments:
        field: the field object to check (field object)

    Returns:
        True if the game is over, False if not (bool)
    '''
    (win, winner, overkill) = field.check_win()
    if win :
        os.system('clear')
        if winner == 'player' :
            print(ASCII_text.win)
        elif winner == 'opponent' :
            print(ASCII_text.lose)
        if overkill :
            print('Overkill: ' + str(overkill))
        return True
    return False

def view_play_attack(field) :
    '''
    menu for player to choose to view deck (will happen), view graveyard (will happen), play a card (will happen), or attack and end turn (won't happen, will be in main loop)

    Arguments:
        field: the field object to view (field object)
    '''
    not_attack = True
    while not_attack :
        field.print_field()
        print('1. View deck')
        print('2. View graveyard')
        print('3. Play a card')
        print('4. Attack and end turn')
        choice = input('Choose an option: ')
        if choice == '1' :
            field.print_remaining()
            input('Press enter to continue.')
        elif choice == '2' :
            field.print_graveyard()
            input('Press enter to continue.')
        elif choice == '3' :
            choose_and_play(field)
        elif choice == '4' :
            not_attack = False
        else :
            print('Invalid choice.')