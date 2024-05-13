import card
import card_library
import deck
import field
import sigils
import os
import ASCII_text
import random
import math
import copy

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
# choose_and_play is good

def choose_draw(field) :
    '''
    the whole process of choosing a card to draw and drawing it

    Arguments:
        field: the field object to draw the card to (field object)
    '''
    bad_input = True
    while bad_input :
        field.print_full_field()
        deck_number = int(input('Draw from main deck (1) or resource deck (2): '))
        if deck_number == 1 :
            card = field.draw('main')
            bad_input = False
        elif deck_number == 2 :
            card = field.draw('resource')
            bad_input = False
        else :
            print('Invalid deck number.')
# choose_draw is good

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
# untested

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
# untested

def deck_gen(possible_cards, size) :
    '''
    generates a deck from a list of possible cards
    
    Arguments:
        possible_cards: list of cards to choose from (dict)
        size: size of deck (int)

    Returns:
        deck: deck of cards (deck object)
    '''
    deck_list = []
    max_cost = max(possible_cards.keys())
    # weighting of cost is done with a beta distribution (alpha = 1.4, beta = 3)
    # mult that by max_cost, use ceil to get ints
    for i in range(size) :
        cost = math.ceil(max_cost * random.betavariate(1.4, 3))
        card = copy.deepcopy(random.choice(possible_cards[cost]))
        deck_list.append(card)
    return deck.Deck(deck_list)
# deck_gen is good

if __name__ == '__main__' :
    # region ### testing setup ###
    os.system('clear')
    leshy_deck = deck.Deck([card_library.Asp(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF()])
    player_deck = deck.Deck([card_library.DumpyTF(), card_library.Lobster(), card_library.BoppitW(), card_library.Ouroboros(), card_library.Turtle(), card_library.Asp(), card_library.Falcon(), card_library.DumpyTF(), card_library.Turtle(), card_library.BoppitW()])
    squirrels = [card_library.Squirrel()]
    for n in range(19) :
        squirrels.append(card_library.Squirrel())
    player_squirrels = deck.Deck(squirrels)
    testmat = field.Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
    testmat.player_field[1] = card_library.Rabbit()
    testmat.player_field[2] = card_library.Falcon()
    testmat.player_field[3] = card_library.DumpyTF()
    testmat.player_field[4] = card_library.Rabbit()
    testmat.player_field[1].play(zone=1)
    testmat.player_field[2].play(zone=2)
    testmat.player_field[3].play(zone=3)
    testmat.player_field[4].play(zone=4)
    testmat.draw('resource')
    testmat.draw('main')
    testmat.draw('resource')
    testmat.draw('resource')
    testmat.draw('main')
    testmat.print_field()
    # endregion

    # testing stuff: 