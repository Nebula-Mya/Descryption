import card_library
import deck
import field
import QoL
import ASCII_text
import random
import math
import copy
import os
import sys

def choose_and_play(field) :
    '''
    the whole process of choosing a card to play and playing it
    player can choose to go back at any time, and if so nothing will happen

    Arguments:
        field: the field object to play the card on (field object)
    '''
    # get terminal size
    term_cols = os.get_terminal_size().columns
    card_gaps = (term_cols*55 // 100) // 5 - 15

    # set variables
    invalid_index = False
    invalid_zone = False

    while True :
        field.print_full_field()
        if invalid_index : # need to print this after the field is printed so it's not cleared
            print('Invalid index.')
            invalid_index = False

        play_index = input('Card to play: (press enter to go back) ')

        if play_index == '' : # go back
            break

        try : # adjust down for indexing and check if it's a number
            play_index = int(play_index) - 1
        except ValueError :
            play_index = len(field.hand)
        
        if play_index not in range(len(field.hand)) : # guard clause for invalid index
            invalid_index = True
            continue
        # if valid index
        while True :
            QoL.clear()
            field.print_field()
            print(' '*card_gaps + 'Card to play:')
            field.hand[play_index].explain()
            if invalid_zone :
                print('Invalid zone.')
                invalid_zone = False
            zone_to_play = input('Zone to play: (press enter to go back) ')

            if zone_to_play == '' : # go back
                break

            try : # check if it's a number
                zone_to_play = int(zone_to_play)
            except ValueError :
                zone_to_play = 0

            if zone_to_play not in range(1, 6) : # guard clause for invalid zone
                invalid_zone = True
            elif not field.play_card(play_index, zone_to_play) :
                continue
            else :
                return

def choose_draw(field) :
    '''
    the whole process of choosing a card to draw and drawing it

    Arguments:
        field: the field object to draw the card to (field object)
    '''
    # set up variables
    main_empty_alert = False
    resource_empty_alert = False
    invalid_choice = False

    while True :
        if main_empty_alert :
            print('Main deck is empty.')
            main_empty_alert = False
        if resource_empty_alert :  
            print('Resource deck is empty.')
            resource_empty_alert = False
        if invalid_choice :
            print('Invalid choice.')
            invalid_choice = False
        
        deck_number = input('Draw from resource deck (1) or main deck (2): ')

        try : # check if it's a number
            deck_number = int(deck_number)
        except ValueError :
            deck_number = 0
        
        match deck_number :
            case 1 :
                try :
                    field.draw('resource')
                    break
                except ValueError :
                    resource_empty_alert = True
            case 2 :
                try :
                    field.draw('main')
                    break
                except ValueError :
                    main_empty_alert = True
            case _ :
                invalid_choice = True

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
        QoL.clear()
        if winner == 'player' :
            ASCII_text.print_win(overkill)
        elif winner == 'opponent' :
            if abs(field.score['player'] - field.score['opponent']) < 8 :
                deck_out = True
            else :
                deck_out = False
            ASCII_text.print_lose(deck_out)
        return True
    return False

def view_remaining(field) : 
    '''
    displays the remaining cards in the player's deck (sorted so as to not allow cheating), and allows the player to view a card
    
    Arguments:
        field: the field object to view (field object)
    '''
    invalid_index = False
    while True :
        field.print_remaining()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        card_choice = input('Choose a card to view: (press enter to go back) ')
        if card_choice == '' :
            break
        try :
            card_choice = int(card_choice) - 1
        except :
            card_choice = len(field.player_deck)
        if card_choice in range(len(field.player_deck)) :
            field.print_remaining()
            sorted_main_deck = sorted(field.player_deck, key=lambda x: x.name)
            sorted_main_deck = sorted(sorted_main_deck, key=lambda x: x.cost)
            sorted_main_deck[card_choice].explain()
            input('Press enter to continue.')
        else :
            invalid_index = True

def view_graveyard(field) :
    '''
    displays the cards in the graveyard and allows the player to view a card
    
    Arguments:
        field: the field object to view (field object)'''
    invalid_index = False
    while True :
        field.print_graveyard()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        card_choice = input('Choose a card to view: (press enter to go back) ')
        if card_choice == '' :
            break
        try :
            card_choice = int(card_choice) - 1
        except :
            card_choice = len(field.graveyard)
        if card_choice in range(len(field.graveyard)) :
            field.print_graveyard()
            field.graveyard[card_choice].explain()
            input('Press enter to continue.')
        else :
            invalid_index = True

def view_cards(field) :
    '''
    menu for player to choose to view bushes, leshy's field, or player's field, all of which are executed by this function

    Arguments:
        field: the field object to view (field object)
    '''
    invalid_choice = False
    while True :
        field.print_field()
        if invalid_choice :
            print('Invalid choice.')
            invalid_choice = False
        print('1. Player field')
        print("2. Leshy's field")
        if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')):
            print('3. Bushes (PLACEHOLDER)')
        else :
            print('3. Bushes')
        row_choice = input('Choose a row to view: (press enter to go back) ')
        if row_choice == '' :
            break
        elif row_choice == '3' : # bushes
            invalid_index = False
            while True :
                field.print_field()
                if invalid_index :
                    print('Invalid index.')
                    invalid_index = False
                col_choice = input('Choose a card to view: (press enter to go back) ')
                if col_choice == '' :
                    break
                try :
                    col_choice = int(col_choice)
                except :
                    col_choice = 0
                if col_choice in range(1, 6) and field.bushes[col_choice].species != '':
                    field.print_field()
                    field.bushes[col_choice].explain()
                    input('Press enter to continue.')
                else :
                    invalid_index = True
        elif row_choice == '2' : # leshy's field
            invalid_index = False
            while True :
                field.print_field()
                if invalid_index :
                    print('Invalid index.')
                    invalid_index = False
                col_choice = input('Choose a card to view: (press enter to go back) ')
                if col_choice == '' :
                    break
                try :
                    col_choice = int(col_choice)
                except :
                    col_choice = 0
                if col_choice in range(1, 6) and field.opponent_field[col_choice].species != '':
                    field.print_field()
                    field.opponent_field[col_choice].explain()
                    input('Press enter to continue.')
                else :
                    invalid_index = True
        elif row_choice == '1' : # player's field
            invalid_index = False
            while True :
                field.print_field()
                if invalid_index :
                    print('Invalid index.')
                    invalid_index = False
                col_choice = input('Choose a card to view: (press enter to go back) ')
                if col_choice == '' :
                    break
                try :
                    col_choice = int(col_choice)
                except :
                    col_choice = 0
                if col_choice in range(1, 6) and field.player_field[col_choice].species != '':
                    field.print_field()
                    field.player_field[col_choice].explain()
                    input('Press enter to continue.')
                else :
                    invalid_index = True
        else :
            invalid_choice = True

def view_play_attack(field) :
    '''
    menu for player to choose to view deck (will happen), view graveyard (will happen), play a card (will happen), or attack and end turn (won't happen, will be in main loop)

    Arguments:
        field: the field object to view (field object)
    '''
    not_attack = True
    invalid_choice = False
    while not_attack :
        field.print_field()
        print('1. Play a card')
        print('2. View a card')
        print('3. View deck')
        print('4. View graveyard')
        print('5. Attack and end turn')
        if invalid_choice :
            print('Invalid choice.')
            invalid_choice = False
        choice = input('Choose an option: ')
        if choice == '3' :
            view_remaining(field)
        elif choice == '4' :
            view_graveyard(field)
        elif choice == '2' :
            view_cards(field)
        elif choice == '1' :
            choose_and_play(field)
        elif choice == '5' :
            not_attack = False
        else :
            invalid_choice = True

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
    # weighting of cost is done with a beta distribution
    # mult that by max_cost+1, use floor to get ints
    for i in range(size) :
        cost = math.floor((max_cost + 1) * random.betavariate(2.2, 3.3))
        card = copy.deepcopy(random.choice(possible_cards[cost]))
        deck_list.append(card)
    return deck.Deck(deck_list)

def resource_gen(size=20) :
    '''
    generates a resource deck

    Arguments:
        size: size of deck, defaults to 20 (int)

    Returns:
        a resource deck (deck object)
    '''
    squirrels = [card_library.Squirrel()]
    for n in range(size - 1) :
        squirrels.append(card_library.Squirrel())
    return deck.Deck(squirrels)

def main(deck_size, hand_size, Leshy_play_count_median=2, Leshy_play_count_variance=1, Leshy_in_strategy_chance=75, Leshy_strat_change_threshold=3) :
    # game setup
    opponent_deck = deck_gen(card_library.Poss_Leshy, deck_size*2 + 20)
    opponent_decklist = opponent_deck.shuffle()
    player_deck = deck_gen(card_library.Poss_Playr, deck_size)
    player_decklist = player_deck.shuffle()
    squirrels_deck = [card_library.Squirrel()]
    for n in range(19) :
        squirrels_deck.append(card_library.Squirrel())
    playfield = field.Playmat(deck=player_decklist, squirrels=squirrels_deck, opponent_deck=opponent_decklist, Leshy_play_count_median=Leshy_play_count_median, Leshy_play_count_variance=Leshy_play_count_variance, Leshy_in_strategy_chance=Leshy_in_strategy_chance, Leshy_strat_change_threshold=Leshy_strat_change_threshold)
    # advance from bushes
    playfield.advance()
    # draw squirrel and hand_size - 1 card
    playfield.draw('resource')
    for n in range(hand_size - 1) :
        playfield.draw('main')
    playfield.print_full_field()

    # game loop
    ongoing = True
    while ongoing :
        if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) :
            quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
            if quit_game == 'y' :
                return
        # gameplay loop
        # player turn
        if playfield.active == 'player' :
            choose_draw(playfield)
            view_play_attack(playfield)
        # leshy turn
        else :
            playfield.advance()
            playfield.print_field()
            input('Press enter to continue.')
        # attack
        playfield.attack()
        playfield.check_states()
        playfield.print_field()
        input('Press enter to continue.')

        # switch active player
        playfield.switch()

        # if winner_check, ongoing = False
        has_ended = winner_check(playfield)
        ongoing = not has_ended
        if has_ended :
            input('Press enter to return to menu.')

if __name__ == '__main__' :
    QoL.clear()
    deck_size = 20
    hand_size = 5
    main(deck_size, hand_size)