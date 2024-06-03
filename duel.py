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
    term_cols = os.get_terminal_size().columns
    card_gaps = (term_cols*55 // 100) // 5 - 15
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
            play_index = len(field.hand)
        if play_index in range(len(field.hand)) :
            bad_input = False
            QoL.clear()
            field.print_field()
            print(' '*card_gaps + 'Card to play:')
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
        field.print_full_field()
        deck_number = input('Draw from main deck (1) or resource deck (2): ')
        try :
            deck_number = int(deck_number)
        except :
            deck_number = 0
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
        QoL.clear()
        if winner == 'player' :
            print(ASCII_text.win)
        elif winner == 'opponent' :
            print(ASCII_text.lose)
            if abs(field.score['player'] - field.score['opponent']) < 8 :
                print(' '*40 + 'You have been decked out.')
        if overkill :
            print('Overkill: ' + str(overkill))
        return True
    return False

def view_remaining(field) : 
    '''
    displays the remaining cards in the player's deck (sorted so as to not allow cheating), and allows the player to view a card
    
    Arguments:
        field: the field object to view (field object)
    '''
    bad_input = True
    invalid_index = False
    while bad_input :
        field.print_remaining()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        card_choice = input('Choose a card to view: (press enter to go back) ')
        if card_choice == '' :
            return
        try :
            card_choice = int(card_choice) - 1
        except :
            card_choice = len(field.player_deck)
        if card_choice in range(len(field.player_deck)) :
            bad_input = False
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
    bad_input = True
    invalid_index = False
    while bad_input :
        field.print_graveyard()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        card_choice = input('Choose a card to view: (press enter to go back) ')
        if card_choice == '' :
            return
        try :
            card_choice = int(card_choice) - 1
        except :
            card_choice = len(field.graveyard)
        if card_choice in range(len(field.graveyard)) :
            bad_input = False
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
    bad_input = True
    invalid_choice = False
    while bad_input :
        field.print_field()
        if invalid_choice :
            print('Invalid choice.')
            invalid_choice = False
        if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')):
            print('1. Bushes (PLACEHOLDER)')
        else :
            print('1. Bushes')
        print("2. Leshy's field")
        print('3. Player field')
        row_choice = input('Choose a row to view: (press enter to go back) ')
        if row_choice == '' :
            break
        elif row_choice == '1' : # bushes
            invalid_index = False
            while bad_input :
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
                    bad_input = False
                    input('Press enter to continue.')
                else :
                    invalid_index = True
        elif row_choice == '2' : # leshy's field
            invalid_index = False
            while bad_input :
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
                    bad_input = False
                    input('Press enter to continue.')
                else :
                    invalid_index = True
        elif row_choice == '3' : # player's field
            invalid_index = False
            while bad_input :
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
                    bad_input = False
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
    while not_attack :
        field.print_field()
        print('1. View deck')
        print('2. View graveyard')
        print('3. View a card')
        print('4. Play a card')
        print('5. Attack and end turn')
        choice = input('Choose an option: ')
        if choice == '1' :
            view_remaining(field)
        elif choice == '2' :
            view_graveyard(field)
        elif choice == '3' :
            view_cards(field)
        elif choice == '4' :
            choose_and_play(field)
        elif choice == '5' :
            not_attack = False
        else :
            print('Invalid choice.')

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
    # bad_input = True
    # while bad_input :
    #     deck_size = input('(PLAYTEST FEATURE) Deck size: ')
    #     try :
    #         deck_size = int(deck_size)
    #         bad_input = False
    #     except :
    #         print('Invalid deck size.')
    # bad_input = True
    # while bad_input :
    #     hand_size = input('(PLAYTEST FEATURE) Hand size: ')
    #     try :
    #         hand_size = int(hand_size)
    #         bad_input = False
    #     except :
    #         print('Invalid hand size.')
    # quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
    # if quit_game == 'y' :
    #     exit()

    deck_size = 20
    hand_size = 5
    main(deck_size, hand_size)

    ## deck generation testing
    # print(deck_gen(card_library.Poss_Playr, 32))

    ## win check testing
    # opponent_deck = deck_gen(card_library.Poss_Leshy, 15*2 + 20)
    # opponent_decklist = opponent_deck.shuffle()
    # player_deck = deck_gen(card_library.Poss_Playr, 15)
    # player_decklist = player_deck.shuffle()
    # squirrels_deck = [card_library.Squirrel()]
    # for n in range(19) :
    #     squirrels_deck.append(card_library.Squirrel())
    # playfield = field.Playmat(deck=player_decklist, squirrels=squirrels_deck, opponent_deck=opponent_decklist)
    # playfield.print_field()
    # playfield.score['player'] = 10
    # playfield.score['opponent'] = 3
    # playfield.print_field()
    # playfield.score['opponent'] = 2
    # input('Press enter to continue.')
    # playfield.print_field()
    # input('Press enter to continue. (player wins)')
    # winner_check(playfield)
    # input('Press enter to continue.')

    # playfield.score['player'] = 3
    # playfield.score['opponent'] = 10
    # playfield.print_field()
    # playfield.score['player'] = 2
    # input('Press enter to continue.')
    # playfield.print_field()
    # input('Press enter to continue. (opponent wins)')
    # winner_check(playfield)
    # input('Press enter to continue.')

    # playfield.score['player'] = 0
    # playfield.score['opponent'] = 2
    # playfield.print_field()
    # playfield.player_squirrels = []
    # playfield.player_deck = []
    # input('Press enter to continue. (decked out)')
    # winner_check(playfield)

    ## attack testing
    # import card
    # opponent_deck = deck_gen(card_library.Poss_Leshy, 15*2 + 20)
    # opponent_decklist = opponent_deck.shuffle()
    # player_deck = deck_gen(card_library.Poss_Playr, 15)
    # player_decklist = player_deck.shuffle()
    # squirrels_deck = [card_library.Squirrel()]
    # for n in range(19) :
    #     squirrels_deck.append(card_library.Squirrel())
    # playfield = field.Playmat(deck=player_decklist, squirrels=squirrels_deck, opponent_deck=opponent_decklist)
    # playfield.player_field = {0: card.BlankCard(), 1: card_library.Stoat(), 2: card_library.Wolf(), 3: card_library.Grizzly(), 4: card_library.Urayuli(), 5: card_library.Raven(), 6: card.BlankCard()}
    # playfield.player_field[0].play(0)
    # playfield.player_field[1].play(1)
    # playfield.player_field[2].play(2)
    # playfield.player_field[3].play(3)
    # playfield.player_field[4].play(4)
    # playfield.player_field[5].play(5)
    # playfield.player_field[6].play(6)
    # playfield.opponent_field = {0: card.BlankCard(), 1: card_library.Stoat(), 2: card_library.Wolf(), 3: card_library.Grizzly(), 4: card_library.Urayuli(), 5: card_library.Raven(), 6: card.BlankCard()}
    # playfield.opponent_field[0].play(0)
    # playfield.opponent_field[1].play(1)
    # playfield.opponent_field[2].play(2)
    # playfield.opponent_field[3].play(3)
    # playfield.opponent_field[4].play(4)
    # playfield.opponent_field[5].play(5)
    # playfield.opponent_field[6].play(6)
    # playfield.bushes = {0: card.BlankCard(), 1: card_library.Stoat(), 2: card.BlankCard(), 3: card_library.Grizzly(), 4: card_library.Urayuli(), 5: card_library.Raven(), 6: card.BlankCard()}
    # playfield.bushes[0].play(0)
    # playfield.bushes[1].play(1)
    # playfield.bushes[2].play(2)
    # playfield.bushes[3].play(3)
    # playfield.bushes[4].play(4)
    # playfield.bushes[5].play(5)
    # playfield.bushes[6].play(6)
    # playfield.print_field()
    # input('Press enter to continue.')
    # playfield.attack()
    # playfield.print_field()
    # input('Press enter to continue.')
    # playfield.check_states()
    # playfield.print_field()