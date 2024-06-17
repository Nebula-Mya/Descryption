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

    # set up variables
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

            (is_int, zone_to_play) = QoL.reps_int(zone_to_play)

            if not is_int or zone_to_play not in range(1, 6) : # guard clause for invalid zone
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
        field.print_full_field()
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

        (_, deck_number) = QoL.reps_int(deck_number)
        
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
    checks if the game is over and prints the appropriate message

    Arguments:
        field: the field object to check (field object)

    Returns:
        True if the game is over, False if not (bool)
    '''
    # get variables from field
    (win, winner, overkill) = field.check_win()
    
    if not win : # guard clause for game not being over
        return False
    
    # game is over
    QoL.clear()
    match winner :
        case 'player' :
            ASCII_text.print_win(overkill)
        case 'opponent' :
            deck_out = False
            if abs(field.score['player'] - field.score['opponent']) < 8 : # if Leshy isn't winning by at least 8 points, it's a deck out
                deck_out = True
            ASCII_text.print_lose(deck_out)
    return True

def view_remaining(field) : 
    '''
    displays the remaining cards in the player's deck (sorted so as to not allow cheating), and allows the player to view a card
    
    Arguments:
        field: the field object to view (field object)
    '''
    # set up variables
    invalid_index = False

    while True :
        field.print_remaining()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        card_choice = input('Choose a card to view: (press enter to go back) ')
        if card_choice == '' :
            break

        (is_int, card_choice) = QoL.reps_int(card_choice, -1)
        if is_int and card_choice in range(len(field.player_deck)) :
            field.print_remaining()
            QoL.sort_deck(field.player_deck)[card_choice].explain()
            input('Press enter to continue.')
        else :
            invalid_index = True

def view_graveyard(field) :
    '''
    displays the cards in the graveyard and allows the player to view a card
    
    Arguments:
        field: the field object to view (field object)
    '''
    # set up variables
    invalid_index = False

    while True :
        field.print_graveyard()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        card_choice = input('Choose a card to view: (press enter to go back) ')
        if card_choice == '' :
            break

        (is_int, card_choice) = QoL.reps_int(card_choice, -1)
        if is_int and card_choice in range(len(field.graveyard)) :
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
    def pick_from_row(row) :
        '''
        allows player to choose a card from a row to view
        
        Arguments:
            row: the row to choose from (list of card objects)
        '''
        # set up variables
        invalid_index = False

        while True :
            field.print_field()
            if invalid_index :
                print('Invalid index.')
                invalid_index = False
            col_choice = input('Choose a card to view: (press enter to go back) ')
            if col_choice == '' :
                break

            (is_int, col_choice) = QoL.reps_int(col_choice)
            if is_int and col_choice in range(1, 6) and row[col_choice].species != '' :
                field.print_field()
                row[col_choice].explain()
                input('Press enter to continue.')
            else :
                invalid_index = True

    # set up variables
    invalid_choice = False

    while True :
        field.print_field()
        print('1. Player field')
        print("2. Leshy's field")
        print('3. Bushes')
        if invalid_choice :
            print('Invalid choice.')
            invalid_choice = False
        row_choice = input('Choose a row to view: (press enter to go back) ')
        match row_choice :
            case '' :
                break
            case '1' :
                pick_from_row(field.player_field)
            case '2' :
                pick_from_row(field.opponent_field)
            case '3' :
                pick_from_row(field.bushes)
            case _ :
                invalid_choice = True

def view_play_attack(field) :
    '''
    menu for player to choose to view deck (will happen), view graveyard (will happen), play a card (will happen), or attack and end turn (won't happen, will be in main loop)

    Arguments:
        field: the field object to view (field object)
    '''
    # set up variables
    invalid_choice = False

    while True :
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
        match choice :
            case '1' :
                choose_and_play(field)
            case '2' :
                view_cards(field)
            case '3' :
                view_remaining(field)
            case '4' :
                view_graveyard(field)
            case '5' :
                affirm = input('Are you sure you want to end your turn? (type anything to continue) ').lower() # might change this prompt
                if affirm != '' :
                    break
            case _ :
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
    # set up variables
    deck_list = []
    max_cost = max(possible_cards.keys())

    # weighting of cost is done via beta distribution, multiplied and rounding up to nearest cost
    for _ in range(size) :
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
    # set up variables
    squirrels = []

    for _ in range(size) : 
        squirrels.append(card_library.Squirrel())

    return deck.Deck(squirrels)

def main(deck_size, hand_size, Leshy_play_count_median=2, Leshy_play_count_variance=1, Leshy_in_strategy_chance=75, Leshy_strat_change_threshold=3) :
    # game setup
    opponent_deck = deck_gen(card_library.Poss_Leshy, deck_size*2)
    player_deck = deck_gen(card_library.Poss_Playr, deck_size)
    squirrels_deck = resource_gen(deck_size)

    playfield = field.Playmat(deck=player_deck.shuffle(), squirrels=squirrels_deck.shuffle(), opponent_deck=opponent_deck.shuffle(), Leshy_play_count_median=Leshy_play_count_median, Leshy_play_count_variance=Leshy_play_count_variance, Leshy_in_strategy_chance=Leshy_in_strategy_chance, Leshy_strat_change_threshold=Leshy_strat_change_threshold)

    # advance from bushes
    playfield.advance()

    # draw squirrel and hand_size - 1 card
    playfield.draw('resource')
    for _ in range(hand_size - 1) :
        playfield.draw('main')
    playfield.print_field()

    # game loop
    while True :
        # playtest feature to quick quit
        if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) :
            if playfield.active == 'player' :
                playfield.print_full_field()
            quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
            if quit_game == 'y' :
                QoL.clear()
                if playfield.score['player'] > playfield.score['opponent'] :
                    ASCII_text.print_win()
                else :
                    ASCII_text.print_lose()
                break
            
        # player turn
        if playfield.active == 'player' :
            choose_draw(playfield)
            view_play_attack(playfield)

        # leshy turn
        else :
            playfield.advance()
            playfield.print_field()
            input('Press enter to continue.')

        # attack (both turns)
        playfield.attack()
        playfield.check_states()
        playfield.print_field()
        input('Press enter to continue.')

        # switch turns
        playfield.switch()
        if winner_check(playfield) :
            break
            
    input('Press enter to return to menu.')

if __name__ == '__main__' :
    QoL.clear()
    deck_size = 20
    hand_size = 5
    main(deck_size, hand_size)