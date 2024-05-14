import card_library
import deck
import field
import QoL
import ASCII_text
import random
import math
import copy
import os

def choose_and_play(field) :
    '''
    the whole process of choosing a card to play and playing it
    player can choose to go back at any time, and if so nothing will happen

    Arguments:
        field: the field object to play the card on (field object)
    '''
    (term_cols, term_rows) = os.get_terminal_size()
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
            play_index = len(field.hand) + 1
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

def main(deck_size, hand_size) :
    # game setup
    opponent_deck = deck_gen(card_library.Poss_Leshy, deck_size*2 + 20)
    opponent_decklist = opponent_deck.shuffle()
    player_deck = deck_gen(card_library.Poss_Playr, deck_size)
    player_decklist = player_deck.shuffle()
    squirrels_deck = [card_library.Squirrel()]
    for n in range(19) :
        squirrels_deck.append(card_library.Squirrel())
    playfield = field.Playmat(deck=player_decklist, squirrels=squirrels_deck, opponent_deck=opponent_decklist)
    # advance from bushes
    playfield.advance()
    # draw squirrel and hand_size - 1 card
    playfield.draw('resource')
    for n in range(hand_size - 1) :
        playfield.draw('main')
    playfield.print_full_field()
    input('Press enter to start.')

    # game loop
    ongoing = True
    while ongoing :
        quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
        if quit_game == 'y' :
            exit()
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
        ongoing = not winner_check(playfield)

if __name__ == '__main__' :
    QoL.clear()
    bad_input = True
    while bad_input :
        deck_size = input('(PLAYTEST FEATURE) Deck size: ')
        try :
            deck_size = int(deck_size)
            bad_input = False
        except :
            print('Invalid deck size.')
    bad_input = True
    while bad_input :
        hand_size = input('(PLAYTEST FEATURE) Hand size: ')
        try :
            hand_size = int(hand_size)
            bad_input = False
        except :
            print('Invalid hand size.')
    quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
    if quit_game == 'y' :
        exit()
    main(deck_size, hand_size)

    ## deck generation testing
    # print(deck_gen(card_library.Poss_Playr, 32))