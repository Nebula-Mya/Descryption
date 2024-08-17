import card_library
import card
import field
import QoL
import ASCII_text
import sys
import duel
import random
import deck
import time
import sigils

def card_battle(campaign, Poss_Leshy=None) : 
    '''
    starts a card battle between the player and Leshy, with the player's deck being campaign.player_deck
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
        Poss_Leshy: the possible cards for Leshy's deck, defaults to all allowed Leshy cards with costs <= to player's max cost (list)

    Returns:
        bool: True if the player wins, False if the player loses
    '''
    def gameplay(campaign, Poss_Leshy) :
        import duel

        data_to_read = [
            ['settings', 'difficulty', 'leshy median plays'],
            ['settings', 'difficulty', 'leshy plays variance'],
            ['settings', 'difficulty', 'leshy strat chance'],
            ['settings', 'difficulty', 'leshy offense threshold']
        ]
        [play_median, play_var, opp_strat, opp_threshold] = QoL.read_data(data_to_read)

        deck_size = len(campaign.player_deck)

        if Poss_Leshy :
            leshy_deck = duel.deck_gen(Poss_Leshy, int(deck_size * 1.5))
        else :
            player_max_cost = max([card.saccs for card in campaign.player_deck.cards])
            fair_poss_leshy = {cost: [card for card in card_library.Poss_Leshy[cost]] for cost in range(0, max(3, player_max_cost+1))} # may be changed later for balancing
            leshy_deck = duel.deck_gen(fair_poss_leshy, int(deck_size * 1.5))
        
        QoL.clear()
        print('\n')
        wick_states = [2] + [3] * (campaign.lives - 1)
        wick_states += [0] * (3 - len(wick_states))
        ASCII_text.print_candelabra(wick_states)
        print(QoL.center_justified('As you approach the figure, Leshy blows out all but one of your candles.').rstrip())
        print(QoL.center_justified('"Beat this boss and I\'ll relight your candles."').rstrip())
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

        (_, winner, overkill, _) = duel.main(deck_size, 4, play_median, play_var, opp_strat, opp_threshold, player_deck_obj=campaign.player_deck, opponent_deck_obj=leshy_deck, squirrels_deck_obj=campaign.squirrel_deck, print_results=False)

        if winner == 'opponent' :
            campaign.lives = 0
            QoL.clear()
            print('\n'*3)
            ASCII_text.print_candelabra([3, 0, 0])
            print()
            input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
            return False
        
        campaign.add_teeth(overkill)
        QoL.clear()
        print('\n'*3)
        wick_states = (campaign.lives) * [2]
        wick_states += [0] * (3 - len(wick_states))
        ASCII_text.print_candelabra(wick_states)
        print()
        return True
    
    return gameplay(campaign, Poss_Leshy) # add flavor text, context, etc.

##### bosses will use the basic AI, but with higher difficulty settings and have their unique mechanics (pickaxe, ship, extra sigils, moon)

##### bosses essentially work as two duels, but winning the first duel triggers a special event (the bosses unique mechanic) and the second duel starts from where the first left off

##### before boss fights, all but one candle will be extinguished, and a smoke card will be added to the deck for each candle extinguished 

##### after a boss fight, remove all smoke cards from the deck

##### if the player loses to a boss, set campaign.has_lost = True, as lives arent updated during the previous thing

##### if the player wins, relight candles and update config file

def get_higher_difficulty() :
    '''
    gets the higher difficulty settings for bosses
    
    Returns:
        tuple: the higher difficulty settings for bosses
    '''
    difficulty_number = QoL.read_data([['settings', 'difficulty', 'current difficulty index']])[0]
    difficulty_settings = [
        { # very easy
            'leshy median plays' : 1,
            'leshy plays variance' : 0,
            'leshy strat chance' : 40,
            'leshy offense threshold' : 5
            },
        { # easy
            'leshy median plays' : 2,
            'leshy plays variance' : 0,
            'leshy strat chance' : 60,
            'leshy offense threshold' : 4
            },
        { # normal
            'leshy median plays' : 2,
            'leshy plays variance' : 1,
            'leshy strat chance' : 75,
            'leshy offense threshold' : 3
            },
        { # hard
            'leshy median plays' : 3,
            'leshy plays variance' : 2,
            'leshy strat chance' : 90,
            'leshy offense threshold' : 3
            },
        { # very hard
            'leshy median plays' : 4,
            'leshy plays variance' : 1,
            'leshy strat chance' : 100,
            'leshy offense threshold' : 2
            }
    ]
    match difficulty_number :
        case 4 : # already max difficulty
            return (difficulty_settings[4]['leshy median plays'], difficulty_settings[4]['leshy plays variance'], difficulty_settings[4]['leshy strat chance'], difficulty_settings[4]['leshy offense threshold'])
        case value if value in range(0, 4) :
            return (difficulty_settings[value]['leshy median plays'], difficulty_settings[value]['leshy plays variance'], difficulty_settings[value + 1]['leshy strat chance'], difficulty_settings[value + 1]['leshy offense threshold'])
        case _ :
            raise ValueError(f"invalid difficulty number: {difficulty_number}")

def error_checks(deck_size, hand_size, Leshy_play_count_median, Leshy_play_count_variance, Leshy_in_strategy_chance, Leshy_strat_change_threshold) :
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

def pre_boss_flavor(campaign) :
    '''
    prints pre boss fight flavor text and displays
    adds smoke cards to the player's deck
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    # pre fight flavor text, extra lives being extinguished, etc.
    QoL.clear()
    print('\n')
    wick_states = [2] + [3] * (campaign.lives - 1)
    wick_states += [0] * (3 - len(wick_states))
    for _ in range(0, campaign.lives - 1) :
        campaign.add_card(card_library.Smoke())
    ASCII_text.print_candelabra(wick_states)
    print(QoL.center_justified('As you approach the figure, Leshy blows out all but one of your candles.').rstrip())
    print(QoL.center_justified('"Beat this boss and I\'ll relight your candles."').rstrip())
    print()
    input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

def post_boss_flavor(campaign, result) :
    '''
    prints post boss fight flavor text and displays
    removes smoke cards from the player's deck

    Arguments:
        campaign: the current campaign object (rogue_campaign object)
        result: whether the player won (bool)
    '''
    # remove smoke cards
    all_smoke = [card_ for card_ in campaign.player_deck.cards if card_.species == 'The Smoke']
    for smoke in all_smoke :
        campaign.remove_card(smoke)

    if not result : # player lost
        QoL.clear()
        print('\n'*3)
        ASCII_text.print_candelabra([3, 0, 0])
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
    else : # player won
        QoL.clear()
        print('\n'*3)
        wick_states = (campaign.lives) * [2]
        wick_states += [0] * (3 - len(wick_states))
        ASCII_text.print_candelabra(wick_states)
        print()

def turn_structure(playfield) :
    '''
    the turn structure for boss fights, excluding checking for win conditions and switching turns

    Arguments:
        playfield: the current playfield object (field object)

    Returns:
        tuple: win, winner, overkill, deck_out, played (bool, str, int, bool, list)
    '''
    # set up variables
    played = []

    # playtest feature to quick quit
    if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) :
        if playfield.active == 'player' :
            playfield.print_full_field()
        quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
        if quit_game == 'y' :
            QoL.clear()
            if playfield.score['player'] > playfield.score['opponent'] :
                (win, winner, overkill, deck_out) = (True, 'player', 0, False)
            else :
                (win, winner, overkill, deck_out) = (True, 'opponent', 0, False)
            return (win, winner, overkill, deck_out, [])
        
    # player turn
    if playfield.active == 'player' :
        duel.choose_draw(playfield)
        played = duel.view_play_attack(playfield)

    # leshy turn
    else :
        if any([card_.species == 'The Moon' for card_ in playfield.opponent_field.values()]) : # tidal lock sigil if moon on the board
            for card_ in [card_ for card_ in playfield.player_field.values() if card_.species in ['Squirrel', 'Vole']] :
                playfield.graveyard.insert(0, card_)
                playfield.summon_card(card=card.BlankCard(), zone=[zone for zone, zone_card in playfield.player_field.items() if zone_card == card_][0], field=playfield.player_field)
        playfield.advance()
        playfield.print_field()
        input('Press enter to continue.')

    # attack (both turns)
    playfield.attack()
    playfield.check_states()
    playfield.print_field()
    input('Press enter to continue.')

    return (False, '', 0, False, played)

def init_boss_playfield(campaign, Poss_Leshy=None, first_cards=None, advance=True) :
    '''
    creates the playfield for a boss fight

    Arguments:
        campaign: the current campaign object (rogue_campaign object)
        Poss_Leshy: the possible cards for Leshy's deck, defaults to all allowed Leshy cards with costs <= to player's max cost (list)
        first_cards: the first cards to be drawn by Leshy, from first to last (list)
        advance: whether to advance from bushes (bool)
    '''
    # set variables
    (play_median, play_var, opp_strat, opp_threshold) = get_higher_difficulty()

    deck_size = len(campaign.player_deck)

    if Poss_Leshy :
        leshy_deck = duel.deck_gen(Poss_Leshy, int(deck_size * 1.5))
    else :
        player_max_cost = max([card.saccs for card in campaign.player_deck.cards])
        leshy_max_cost = max(cost for cost in card_library.Poss_Leshy.keys())
        fair_poss_leshy = {cost: [card for card in card_library.Poss_Leshy[cost]] for cost in range(0, min(leshy_max_cost, player_max_cost+1))} # may be changed later for balancing
        leshy_deck = duel.deck_gen(fair_poss_leshy, int(deck_size * 1.5))

    playfield = field.Playmat(campaign.player_deck.shuffle(fair_hand=True), campaign.squirrel_deck.shuffle(), leshy_deck.shuffle(), play_median, play_var, opp_strat, opp_threshold)

    # add first cards to top of deck
    if first_cards :
        first_cards.reverse()
        for _ in range(len(first_cards)) :
            playfield.opponent_deck.pop()
        for card_ in first_cards :
            playfield.opponent_deck.insert(0, card_)

    # advance from bushes
    if advance : playfield.advance()

    # draw squirrel and hand_size - 1 card
    playfield.draw('resource')
    for _ in range(3) :
        playfield.draw('main')
    playfield.print_field()

    return playfield

def random_extra_sigil(possibles) :
    '''
    selects a card from possibles and adds a random sigil to it

    Arguments:
        possibles: the possible cards to choose from (list)

    Returns:
        card: the chosen card with a random sigil added (card object)
    '''
    # set up functions
    def sigil_name(sigil) :
        match sigil :
            case '' : return 'No Sigil'
            case _ if 'hefty' in sigil : return 'Hefty'
            case _ if 'lane shift' in sigil : return 'Sprinter'
            case _ : return QoL.title_case(sigil)

    same_sigil = lambda sigil_1, sigil_2 : sigil_1 != '' and sigil_name(sigil_1) == sigil_name(sigil_2) # check if two sigils are the same or variations of the same sigil
    good_sigil = lambda reciever, sigil : sigil not in ['', '???'] and not same_sigil(reciever.sigils[0], sigil) and not same_sigil(reciever.sigils[1], sigil) # check if a sigil can be added
    
    # choose card
    chosen_card = QoL.random_card(possibles)

    # get sigil slot
    if chosen_card.has_sigil('') :
        sigil_slot = chosen_card.sigils.index('')
    else :
        sigil_slot = random.choice([0, 1])

    # while not good_sigil(hidden_reward, selected_sigil) : selected_sigil = random.choice(list(sigils.Dict.keys()))
    while not good_sigil(chosen_card, sigil := random.choice(list(sigils.Dict.keys()))) : pass
    else : chosen_card.sigils[sigil_slot] = sigil

    chosen_card.update_ASCII()

    return chosen_card

def trading(playfield) :
    '''
    allows the player to trade wolf pelts from their hand for the trader's cards on the board

    Arguments:
        playfield: the current playfield object (field object)
    '''
    def player_vers(traded_card) :
        '''
        switches the player's card to its opposite version if necessary

        Arguments:
            traded_card: the card being traded (card object)
        '''
        if any([traded_card.has_sigil(mover) for mover in sigils.movers]) :
            for (sigil, index) in [(sigil, traded_card.sigils.index(sigil)) for sigil in traded_card.sigils if sigil in sigils.movers] : 
                match (sigil, index) :
                    case ('lane shift left', index) : traded_card.sigils[index] = 'lane shift right'
                    case ('lane shift right', index) : traded_card.sigils[index] = 'lane shift left'
                    case ('hefty (left)', index) : traded_card.sigils[index] = 'hefty (right)'
                    case ('hefty (right)', index) : traded_card.sigils[index] = 'hefty (left)'
            traded_card.update_ASCII()
        
        if type(traded_card) == card_library.OppositeRabbit :
            sigils_ = getattr(traded_card, 'sigils')
            return card_library.Rabbit(sigils=sigils_)
        elif type(traded_card) == card_library.OppositeShrew :
            sigils_ = getattr(traded_card, 'sigils')
            return card_library.Shrew(sigils=sigils_)
        
        return traded_card
    
    def view_hand(playfield) :
        invalid_index = False
        while True :
            QoL.clear()
            print('\n'*5)
            QoL.print_deck(playfield.hand, numbered=True, centered=True, blocked=True)
            if invalid_index :
                print('Invalid index.')
                invalid_index = False
            card_choice = input('Choose a card to view: (press enter to go back) ')
            if card_choice == '' :
                break

            (is_int, card_choice) = QoL.reps_int(card_choice, -1)
            if is_int and card_choice in range(len(playfield.hand)) :
                QoL.clear()
                print('\n'*5)
                QoL.print_deck(playfield.hand, numbered=True, centered=True, blocked=True)
                playfield.hand[card_choice].explain()
                input('Press enter to continue.')
            else :
                invalid_index = True

    def get_card_from_row(row) :
        '''
        allows player to choose a card from a row to trade
        
        Arguments:
            row: the row to choose from (list of card objects)

        Returns:
            card: the chosen card (card object)
        '''
        # set up variables
        invalid_index = False

        while True :
            playfield.print_field(score_scale=False)
            if invalid_index :
                print('Invalid index.')
                invalid_index = False
            col_choice = input('Choose a card to trade for: (press enter to go back) ')
            if col_choice == '' :
                break

            (is_int, col_choice) = QoL.reps_int(col_choice)
            if is_int and col_choice in range(1, 5) and row[col_choice].species != '' :
                return row[col_choice]
            else :
                invalid_index = True
    
    def trade_card(playfield) :
        '''
        allows the player to trade a wolf pelt for a card
        
        Arguments:
            playfield: the current playfield object (field object)
        '''
        # set up variables
        invalid_choice = False

        while True :
            playfield.print_field(score_scale=False)
            print("1. Leshy's field")
            print('2. Bushes')
            if invalid_choice :
                print('Invalid choice.')
                invalid_choice = False
            row_choice = input('Choose a row to trade from: (press enter to go back) ')
            match row_choice :
                case '' : 
                    return
                case '1' :
                    trade_field = playfield.opponent_field
                    chosen_trade = get_card_from_row(playfield.opponent_field)
                    if chosen_trade == None :
                        continue
                    break
                case '2' :
                    trade_field = playfield.bushes
                    chosen_trade = get_card_from_row(playfield.bushes)
                    if chosen_trade == None :
                        continue
                    break
                case _ : 
                    invalid_choice = True
                    continue
        
        # trade card
        zone = [zone for zone, card_ in trade_field.items() if card_ == chosen_trade][0]
        new_card = player_vers(chosen_trade)
        playfield.hand.append(new_card)
        wolf_pelts = [card_ for card_ in playfield.hand if type(card_) == card_library.WolfPelt]
        playfield.hand.remove(wolf_pelts[0])
        playfield.summon_card(card=card.BlankCard(), zone=zone, field=trade_field)

    choices = '''1. Trade a wolf pelt for a card
2. View a card on the field
3. View a card in your hand
4. View your deck
5. Finish trading'''

    invalid_choice = False
    while True :
        playfield.print_field(score_scale=False)
        playfield.print_hand()
        print(choices)
        if invalid_choice :
            print('Invalid choice.')
            invalid_choice = False
        match input('Choose an option: ') :
            case '1' : trade_card(playfield)
            case '2' : duel.view_cards(playfield)
            case '3' : view_hand(playfield)
            case '4' : duel.view_remaining(playfield)
            case '5' : break
            case _ : invalid_choice = True

def boss_fight_prospector(campaign) : # boss fight 1
    def gameplay(campaign) :
        pre_boss_flavor(campaign)

        playfield = init_boss_playfield(campaign, first_cards=[card_library.PackMule(True), card_library.Coyote(True)])

        # game loop
        second_phase = False
        while True :
            # gameplay
            (win, winner, overkill, deck_out, _) = turn_structure(playfield)
            if win : # playtest feature to quick quit
                result = winner == 'player'
                post_boss_flavor(campaign, result)
                if result :
                    QoL.write_data([(['progress markers', 'beat prospector'], True)])
                else :
                    campaign.lives = 0
                break

            # switch turns
            playfield.switch()
            (win, winner, overkill, deck_out) = duel.winner_check(playfield, silent=True)

            if win and winner == 'opponent' :
                post_boss_flavor(campaign, False)
                campaign.lives = 0
                break

            elif win and not second_phase :
                # update variables
                win = False
                second_phase = True

                # flavor text expaining whats happening (why cards are replaced with gold nuggets, etc.)
                QoL.clear()
                print('\n'*5)
                print(QoL.center_justified('Clearly weakened, the prospector takes his pickaxe and strikes your cards.'))
                time.sleep(2)
                print(QoL.center_justified('The cards shatter into gold nuggets.'))
                time.sleep(3)
                print('\n'*2)
                input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

                # kill player's cards
                nugget_zones = [zone for zone in range(1,5) if playfield.player_field[zone].species != '']
                for card_ in playfield.player_field.values() :
                    if card_.species != '' :
                        card_.status = 'dead'
                playfield.check_states()

                # replace player's cards with gold nuggets
                for zone in nugget_zones : playfield.summon_card(card=card_library.GoldNugget(True), zone=zone, field=playfield.player_field)

                # start with bloodhound
                playfield.opponent_deck.insert(0, card_library.Bloodhound(True))

                # reset stats
                playfield.score = {'player': 0, 'opponent': 0}
                playfield.active = 'player'

            elif win and second_phase:
                post_boss_flavor(campaign, True)
                QoL.write_data([(['progress markers', 'beat prospector'], True)])
                break

        return (win, winner, overkill, deck_out)

    return gameplay(campaign) # add flavor text, context, etc.

def boss_fight_angler(campaign) : # boss fight 2
    def gameplay(campaign) :
        pre_boss_flavor(campaign)

        poss_angler_p1 = {
            1 : [card_library.Kingfisher(True), card_library.Otter(True)]
        }
        poss_angler_p2 = {
            0 : [card_library.BaitBucket(True)]
        }
        playfield = init_boss_playfield(campaign, Poss_Leshy=poss_angler_p1, advance=False)

        # game loop
        second_phase = False
        turn_count = 0
        played = []
        while True :
            # gameplay
            (win, winner, overkill, deck_out, played_new) = turn_structure(playfield)
            played += played_new
            if win : # playtest feature to quick quit
                result = winner == 'player'
                post_boss_flavor(campaign, result)
                if result :
                    QoL.write_data([(['progress markers', 'beat angler'], True)])
                else :
                    campaign.lives = 0
                break

            # hook and use hook
            if playfield.active == 'opponent' :
                if turn_count % 2 == 0 : # aim hook at most recently played card
                    if turn_count == 0 : # only explain the first time
                        # flavor text expaining whats happening (why a card is hooked, etc.)
                        QoL.clear()
                        print('\n'*5)
                        print(QoL.center_justified('The angler casts his line and hooks one of your cards.'))
                        time.sleep(3)
                        print('\n'*2)
                        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
                    
                    to_hook = None
                    while to_hook not in playfield.player_field.values() : # ensure a card is hooked
                        to_hook = played[-1]
                        played.pop()
                    to_hook.hook()

                else : # use hook
                    if turn_count == 1 : # only explain the first time
                        # flavor text expaining whats happening (why a hooked card switches sides, etc.)
                        QoL.clear()
                        print('\n'*5)
                        print(QoL.center_justified('The angler reels in his line and pulls your card to his side.'))
                        time.sleep(3)
                        print('\n'*2)
                        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
                    
                    # check if a card is hooked and pull it to the opponent's field
                    if any([card_.hooked for card_ in playfield.player_field.values()]) :
                        for zone in range(1, 5) :
                            if playfield.player_field[zone].hooked :
                                if playfield.opponent_field[zone].species != '' : # shift to bushes
                                    playfield.summon_card(card=playfield.opponent_field[zone], zone=zone, field=playfield.bushes)
                                playfield.summon_card(card=playfield.player_field[zone], zone=zone, field=playfield.opponent_field)
                                playfield.summon_card(card=card.BlankCard(), zone=zone, field=playfield.player_field)
                                break

            # switch turns
            if playfield.active == 'opponent' :
                turn_count += 1
            playfield.switch()
            (win, winner, overkill, deck_out) = duel.winner_check(playfield, silent=True)

            if win and winner == 'opponent' :
                post_boss_flavor(campaign, False)
                campaign.lives = 0
                break

            elif win and not second_phase :
                # update variables
                win = False
                second_phase = True

                has_lost_prior = QoL.read_data([['progress markers', 'losses']])[0] != 0

                if has_lost_prior : # normal behavior
                    # flavor text expaining whats happening (why cards are being replaced with bait buckets, etc.)
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('The angler clears his field and drops bait buckets into the water.'))
                    time.sleep(2)
                    print(QoL.center_justified('You can see the fins of sharks circling.'))
                    time.sleep(3)
                    print('\n'*2)
                    input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

                    # clear angler's field
                    for zone in range(1, 5) :
                        for field in [playfield.opponent_field, playfield.bushes] : playfield.summon_card(card=card.BlankCard(), zone=zone, field=field)

                    # summon bait buckets to anglers field (not bushes) infront of player's cards
                    for zone in range(1, 5) :
                        if playfield.player_field[zone].species != '' : playfield.summon_card(card=card_library.BaitBucket(True), zone=zone, field=playfield.opponent_field)

                else :
                    # flavor text expaining whats happening (why cards are being replaced with grizzly bears, etc.)
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('Leshy removes his mask to speak to you.'))
                    time.sleep(3)
                    print(QoL.center_justified('"Well, I can\'t let you beat my game that easily."'))
                    time.sleep(3)
                    print('\n'*2)
                    input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

                    # fill angler's field and bushes with grizzly bears with mighty leap
                    for zone in range(1, 5) :
                        for field in [playfield.opponent_field, playfield.bushes] : playfield.summon_card(card=card_library.Grizzly(blank_cost=True, sigils=['mighty leap', '']), zone=zone, field=field)

                # change deck to be angler's second phase deck
                playfield.opponent_deck = duel.deck_gen(poss_angler_p2, len(playfield.opponent_deck))

                # reset stats
                playfield.score = {'player': 0, 'opponent': 0}
                playfield.active = 'player'

            elif win and second_phase:
                post_boss_flavor(campaign, True)
                QoL.write_data([(['progress markers', 'beat angler'], True)])
                break

        return (win, winner, overkill, deck_out)

    return gameplay(campaign) # add flavor text, context, etc.

def boss_fight_trapper_trader(campaign) : # boss fight 3
    def gameplay(campaign) :
        pre_boss_flavor(campaign)

        poss_trapper = {
            1 : [card_library.StrangeFrog(True), card_library.DumpyTF(True), card_library.Bullfrog(True)]
        }

        # set up trader's board
        playfield = init_boss_playfield(campaign, Poss_Leshy=poss_trapper, advance=False)
        trader_board_cards = [card.BlankCard(), card_library.StrangeFrog(True), card_library.StrangeFrog(True), card_library.LeapingTrap(True)]
        random.shuffle(trader_board_cards)
        for zone in range(1, 5) :
            playfield.summon_card(card=trader_board_cards.pop(), zone=zone, field=playfield.opponent_field)

        # game loop
        second_phase = False
        played = []
        while True :
            # gameplay
            (win, winner, overkill, deck_out, played_new) = turn_structure(playfield)
            played += played_new
            if win : # playtest feature to quick quit
                result = winner == 'player'
                post_boss_flavor(campaign, result)
                if result :
                    QoL.write_data([(['progress markers', 'beat trapper'], True)])
                else :
                    campaign.lives = 0
                break

            # switch turns
            playfield.switch()
            (win, winner, overkill, deck_out) = duel.winner_check(playfield, silent=True)

            if win and winner == 'opponent' :
                post_boss_flavor(campaign, False)
                campaign.lives = 0
                break

            elif win and not second_phase :
                # update variables
                win = False
                second_phase = True

                has_lost_prior = QoL.read_data([['progress markers', 'losses']])[0] > 1

                if has_lost_prior : # normal behavior
                    # flavor text expaining whats happening (why field is being filled and trading is happening, etc.)
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('Leshy turns his mask upside down, becoming the trader.'))
                    time.sleep(3)
                    print(QoL.center_justified('"I hope you brought pelts..."'))
                    time.sleep(2)
                    print(QoL.center_justified('The trader fills her field with cards.'))
                    time.sleep(2)
                    print(QoL.center_justified('"Because these creatures are prepared to rip your throat out."'))
                    time.sleep(3)
                    print(QoL.center_justified('"Trade for what you can, but know this: the rest will stay and fight for me."'))
                    time.sleep(3)
                    print('\n'*2)
                    input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

                    # fill trader's field with random cards with additional sigils
                    allowed_cards = [card_ for cost in card_library.Poss_Leshy.keys() for card_ in card_library.Poss_Leshy[cost] if card_.has_sigil('')]
                    for zone in range(1, 5) :
                        playfield.summon_card(card=random_extra_sigil(allowed_cards), zone=zone, field=playfield.opponent_field)
                        playfield.opponent_field[zone].blank_cost = False
                        playfield.opponent_field[zone].update_ASCII()
                        playfield.summon_card(card=random_extra_sigil(allowed_cards), zone=zone, field=playfield.bushes)
                        playfield.bushes[zone].blank_cost = False
                        playfield.bushes[zone].update_ASCII()

                    # add all wolf pelts from graveyard and players field to their hand + 1 more
                    playfield.hand.append(card_library.WolfPelt(True))
                    for card_ in playfield.graveyard[:] :
                        if card_.species == 'Wolf Pelt' :
                            playfield.hand.append(card_)
                            playfield.graveyard.remove(card_)
                    for zone in range(1, 5) :
                        if playfield.player_field[zone].species == 'Wolf Pelt' :
                            playfield.hand.append(playfield.player_field[zone])
                            playfield.summon_card(card=card.BlankCard(), zone=zone, field=playfield.player_field)

                    # trade wolf pelts for trader's cards (traded cards go to player's hand)
                    trading(playfield)

                    # hide costs from opponent's cards
                    for zone in range(1, 5) :
                        playfield.opponent_field[zone].blank_cost = True
                        playfield.opponent_field[zone].update_ASCII()
                        playfield.bushes[zone].blank_cost = True
                        playfield.bushes[zone].update_ASCII()

                else :
                    # flavor text expaining whats happening (why cards are being replaced with grizzly bears, etc.)
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('Leshy removes his mask to speak to you.'))
                    time.sleep(3)
                    print(QoL.center_justified('"Well, I can\'t let you beat my game that easily."'))
                    time.sleep(3)
                    print('\n'*2)
                    input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

                    # fill trader's field and bushes with grizzly bears with mighty leap
                    for zone in range(1, 5) :
                        for field in [playfield.opponent_field, playfield.bushes] : playfield.summon_card(card=card_library.Grizzly(blank_cost=True, sigils=['mighty leap', '']), zone=zone, field=field)

                # empty trader's deck
                playfield.opponent_deck = deck.Deck([])

                # reset stats
                playfield.score = {'player': 0, 'opponent': 0}
                playfield.active = 'player'

            elif win and second_phase:
                post_boss_flavor(campaign, True)
                QoL.write_data([(['progress markers', 'beat trapper'], True)])
                break

        return (win, winner, overkill, deck_out)

    return gameplay(campaign) # add flavor text, context, etc.

def boss_fight_leshy(campaign) : # boss fight 4
    ## Leshy's reaction to the moon being destroyed will be part of field.check_states()
    def deck_trials(campaign) :
        pass

    def mining(campaign, playfield) :
        pass

    def hooking(campaign, playfield, played) :
        # hook and use hook
        if playfield.active == 'player' : return # guard clause
            
        to_hook = None
        while to_hook not in playfield.player_field.values() : # ensure a card is hooked
            to_hook = played[-1]
            played.pop()
        to_hook.hook()

        # check if a card is hooked and pull it to the opponent's field
        if any([card_.hooked for card_ in playfield.player_field.values()]) :
            for zone in range(1, 5) :
                if playfield.player_field[zone].hooked :
                    if playfield.opponent_field[zone].species != '' : # shift to bushes
                        playfield.summon_card(card=playfield.opponent_field[zone], zone=zone, field=playfield.bushes)
                    playfield.summon_card(card=playfield.player_field[zone], zone=zone, field=playfield.opponent_field)
                    playfield.summon_card(card=card.BlankCard(), zone=zone, field=playfield.player_field)
                    break

    def trading(campaign, playfield) :
        pass

    class battle_state : ## maybe add explanations for the masks the first time they are used
        '''
        the state of the final boss fight, including phase and masks
            
        Attributes:
            masks: the possible masks to choose from (list)
            index: the index of the mask
            phase: the phase of the fight (1, 2, 3)
            
        Methods:
            change: changes the mask to the next one
            use: uses the mask
        '''
        def __init__(self) :
            self.masks = ['Prospector', 'Angler', 'Trader']
            self.index = 0
            self.phase = 1

        def change(self) :
            '''
            changes the mask to the next one

            Returns:
                str: the new mask
            '''
            pass # add dialogues, etc.
            self.index = (self.index + 1) % len(self.masks)
            return self.masks[self.index]
        
        def use(self, campaign, playfield, played) :
            '''
            uses the mask

            Arguments:
                campaign: the current campaign object (rogue_campaign object)
                playfield: the current playfield object (field object)
                played: the cards played (list)
            '''
            pass

        def win(self, campaign, playfield) :
            '''
            executes the code for beating a phase, depending on the current phase, increments the phase, and returns whether the player has won the entire fight

            Arguments:
                campaign: the current campaign object (rogue_campaign object)
                playfield: the current playfield object (field object)

            Returns:
                bool: whether the player has won the entire fight
            '''
            pass

    def gameplay(campaign) :
        # pre boss events
        deck_trials(campaign)

        # pre boss flavor text
        pre_boss_flavor(campaign)

        # set up trader's board
        playfield = init_boss_playfield(campaign, Poss_Leshy=card_library.Rare_Cards, advance=False)
        duel_state = battle_state()
        start_board_cards = [card.BlankCard(), card.BlankCard(), card.BlankCard(), card_library.MoleMan(True)]
        random.shuffle(start_board_cards)
        for zone in range(1, 5) : playfield.summon_card(card=start_board_cards.pop(), zone=zone, field=playfield.opponent_field)

        # game loop
        played = []
        while True :
            # gameplay
            (win, winner, overkill, deck_out, played_new) = turn_structure(playfield)
            played += played_new
            if win : # playtest feature to quick quit
                result = winner == 'player'
                post_boss_flavor(campaign, result)
                if result :
                    QoL.write_data([(['progress markers', 'beat prospector'], True)])
                else :
                    campaign.lives = 0
                break

            # switch turns
            duel_state.use(campaign, playfield, played)
            duel_state.change()
            playfield.switch()
            (win, winner, overkill, deck_out) = duel.winner_check(playfield, silent=True)

            if win and winner == 'opponent' :
                post_boss_flavor(campaign, False)
                campaign.lives = 0
                break

            elif duel_state().win(campaign) :
                post_boss_flavor(campaign, True)
                QoL.write_data([(['progress markers', 'beat leshy'], True)])
                break

        return (win, winner, overkill, deck_out)

    return gameplay(campaign) # add flavor text, context, etc.