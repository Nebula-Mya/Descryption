from __future__ import annotations # prevent type hints needing import at runtime
from typing import TYPE_CHECKING

import card_library
import deck
import field
import QoL
import ASCII_text
import os
import card

def choose_and_play(field: field.Playmat) -> card.BlankCard | None:
    '''
    the whole process of choosing a card to play and playing it
    player can choose to go back at any time, and if so nothing will happen

    Arguments:
        field: the field object to play the card on (field object)

    Returns:
        the card played or None if no card is played (card object)
    '''
    # get terminal size
    term_cols = os.get_terminal_size().columns
    card_gaps = (term_cols*55 // 100) // 5 - 15

    # set up variables
    invalid_index = False
    invalid_zone = False
    on_occupied = False

    while True :
        field.print_full_field()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False

        play_index = input('Card to play: (press enter to go back) ')

        if play_index == '' : # go back
            break

        (is_int, play_index) = QoL.reps_int(play_index, -1)
        
        if not is_int or play_index not in range(len(field.hand)) : # guard clause for invalid index
            invalid_index = True
            continue
        # if valid index
        while True :
            QoL.clear()
            field.print_field()
            print(' '*card_gaps + 'Card to play:')
            card_to_play = field.hand[play_index] # for tracking played cards
            card_to_play.explain()
            if invalid_zone :
                print('Invalid zone.')
                invalid_zone = False
            if on_occupied :
                print('Cannot play on top of a card without sacrificing.')
                on_occupied = False
            zone_to_play = input('Zone to play: (press enter to go back) ')

            if zone_to_play == '' : # go back
                break

            (is_int, zone_to_play) = QoL.reps_int(zone_to_play)

            if not is_int or zone_to_play not in range(1, 5) : # guard clause for invalid zone
                invalid_zone = True
            elif not field.play_card(play_index, zone_to_play) :
                if field.hand[play_index].saccs == 0 :
                    on_occupied = True
                continue
            else :
                return card_to_play

def choose_draw(field: field.Playmat) -> None :
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

        deck_number = input('Draw from resource deck (1) or main deck (2) or view current deck (3): ')

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
            case 3 :
                QoL.clear()
                print('\n'*5)
                print(QoL.center_justified('Your deck:'))
                field.print_remaining()
                print()
                input(QoL.center_justified('Press Enter to go back...').rstrip() + ' ')
            case _ :
                invalid_choice = True

def winner_check(field: field.Playmat, silent: bool=False) -> tuple[bool, str, int, bool] :
    '''
    checks if the game is over and prints the appropriate message

    Arguments:
        field: the field object to check (field object)
        silent: whether to print the message or not, defaults to False (bool)

    Returns:
        (win, winner, overkill, deck_out) (tuple)
        win: whether the game is over (bool)
        winner: the winner of the game (str)
        overkill: the amount of overkill (int)
        deck_out: whether the deck ran out (bool)
    '''
    # get variables from field
    (win, winner, overkill, deck_out) = field.check_win()
    
    if not win : # guard clause for game not being over
        return (win, winner, overkill, deck_out)
    
    # game is over
    QoL.clear()
    match winner :
        case 'player' if not silent :
            ASCII_text.print_win(overkill)
        case 'opponent' if not silent :
            ASCII_text.print_lose(deck_out)
    return (win, winner, overkill, deck_out)

def view_remaining(field: field.Playmat) -> None : 
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

def view_graveyard(field: field.Playmat) -> None :
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

def view_cards(field: field.Playmat) -> None :
    '''
    menu for player to choose to view bushes, leshy's field, or player's field, all of which are executed by this function

    Arguments:
        field: the field object to view (field object)
    '''
    def pick_from_row(row: dict[int, card.BlankCard]) -> None :
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
            if is_int and col_choice in range(1, 5) and type(row[col_choice]) != card.BlankCard :
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

def view_play_attack(field: field.Playmat) -> list[card.BlankCard] :
    '''
    menu for player to choose to view deck (will happen), view graveyard (will happen), play a card (will happen), or attack and end turn (won't happen, will be in main loop)

    Arguments:
        field: the field object to view (field object)

    Returns:
        played: the cards played (list of card objects)
    '''
    # set up variables
    invalid_choice = False
    played = []

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
                played_card = choose_and_play(field)
                if played_card : played.append(played_card) # track played cards
            case '2' :
                view_cards(field)
            case '3' :
                view_remaining(field)
            case '4' :
                view_graveyard(field)
            case '5' :
                break # might add a confirmation later if it's too easy to accidentally end turn
            case _ :
                invalid_choice = True
        
    return played

def deck_gen(possible_cards: list[type[card.BlankCard]] | dict[int, list[type[card.BlankCard]]], size: int, hidden_cost: bool=False) -> deck.Deck :
    '''
    generates a deck from a list of possible cards
    
    Arguments:
        possible_cards: list of cards to choose from (dict)
        size: size of deck (int)
        hidden_cost: whether to hide the cost of the card, defaults to False (bool)

    Returns:
        deck: deck of cards (deck object)
    '''
    # error handling
    if size < 1 :
        raise ValueError('Deck size must be at least 1.')
    if not possible_cards :
        raise ValueError('Possible cards dict must not be empty.')

    deck_list = [QoL.random_card(possible_cards, hidden_cost) for _ in range(size)]

    return deck.Deck(deck_list)

def resource_gen(size: int) -> deck.Deck :
    '''
    generates a resource deck

    Arguments:
        size: size of deck (int)

    Returns:
        a resource deck (deck object)
    '''
    # error handling
    if size < 1 :
        raise ValueError('Deck size must be at least 1.')

    squirrels: list[card.BlankCard] = [card_library.Squirrel() for _ in range(size)]

    return deck.Deck(squirrels)

def main(deck_size: int, hand_size: int, Leshy_play_count_median: int, Leshy_play_count_variance: int, Leshy_in_strategy_chance: int, Leshy_strat_change_threshold: int, player_deck_obj: deck.Deck | None=None, squirrels_deck_obj: deck.Deck | None=None, opponent_deck_obj: deck.Deck | None=None, print_results: bool=True)  -> tuple[bool, str, int, bool]:
    '''
    main function for deck battles
    
    Arguments:
        deck_size: size of the deck (int)
        hand_size: size of the hand (int)
        Leshy_play_count_median: median number of plays for Leshy (int)
        Leshy_play_count_variance: variance in number of plays for Leshy (int)
        Leshy_in_strategy_chance: chance of Leshy playing in strategy (int)
        Leshy_strat_change_threshold: threshold for Leshy changing strategy (int)
        player_deck_obj: the player's deck object, defaults to None (deck object)
        squirrels_deck_obj: the squirrel deck object, defaults to None (deck object)
        opponent_deck_obj: the opponent's deck object, defaults to None (deck object
        print_results: whether to print the results of the game, defaults to True (bool)
        
    Returns:
        (win, winner, overkill, deck_out) (tuple)'''
    # error handling
    if deck_size < 1 :
        raise ValueError('Deck size must be at least 1.')
    if hand_size < 1 :
        raise ValueError('Hand size must be at least 1.')
    if hand_size > deck_size :
        raise ValueError('Hand size must be less than or equal to deck size.')
    if Leshy_play_count_median < 1 :
        raise ValueError('Leshy play count median must be at least 1.')
    if Leshy_play_count_variance < 0 :
        raise ValueError('Leshy play count variance must be at least 0.')
    if Leshy_in_strategy_chance < 0 or Leshy_in_strategy_chance > 100 :
        raise ValueError('Leshy in strategy chance must be between 0 and 100.')
    if Leshy_strat_change_threshold < -5 or Leshy_strat_change_threshold > 5 :
        raise ValueError('Leshy strategy change threshold must be between -5 and 5.')

    # game setup
    if player_deck_obj :
        player_deck = player_deck_obj
    else :
        player_deck = deck_gen(card_library.Poss_Playr, deck_size)
    if opponent_deck_obj :
        opponent_deck = opponent_deck_obj
    else :
        opponent_deck = deck_gen(card_library.Poss_Leshy, deck_size*2, hidden_cost=True)
    if squirrels_deck_obj :
        squirrels_deck = squirrels_deck_obj
    else :
        squirrels_deck = resource_gen(deck_size)

    playfield = field.Playmat(player_deck.shuffle(fair_hand=True), squirrels_deck.shuffle(), opponent_deck.shuffle(), Leshy_play_count_median, Leshy_play_count_variance, Leshy_in_strategy_chance, Leshy_strat_change_threshold)

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
        # if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) :
        #     if playfield.active == 'player' :
        #         playfield.print_full_field()
        #     quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
        #     if quit_game == 'y' :
        #         QoL.clear()
        #         if playfield.score['player'] > playfield.score['opponent'] :
        #             if print_results : ASCII_text.print_win()
        #             (win, winner, overkill, deck_out) = (True, 'player', 0, False)
        #         else :
        #             if print_results : ASCII_text.print_lose()
        #             (win, winner, overkill, deck_out) = (True, 'opponent', 0, False)
        #         break
            
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
        (win, winner, overkill, deck_out) = winner_check(playfield)
        if win :
            break
            
    if print_results : input('Press enter to continue.')
    return (win, winner, overkill, deck_out)