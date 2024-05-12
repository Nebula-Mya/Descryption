import card
import card_library
import deck
import field
import sigils
import os
import ASCII_text
# file for core gameplay

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