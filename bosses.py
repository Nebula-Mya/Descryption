import card_library
import card
import field
import QoL
import ASCII_text
import random
import sys
import duel

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

def random_card(possible_cards) :
    '''
    gets a random card from a list of possible cards
    '''
    # get card type
    template_card = random.choice(possible_cards)
    card_class = type(template_card)
    if any(type(card) for card in card_library.Rare_Cards) == card_class: # lower chances of rare cards
        template_card = random.choice(possible_cards)
        card_class = type(template_card)

    return card_class(getattr(template_card, 'blank_cost', False))

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

def boss_fight_prospector(campaign) : # boss fight 1
    def gameplay(campaign) :
        pre_boss_flavor(campaign)

        playfield = init_boss_playfield(campaign, first_cards=[card_library.PackMule(True), card_library.Coyote(True)])

        # game loop
        second_phase = False
        pack_mule_killed = False
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

            # check if pack mule was killed
            if not pack_mule_killed and all([type(card_) != card_library.PackMule for card_ in playfield.opponent_field.values()] + [type(card_) != card_library.PackMule for card_ in playfield.bushes.values()]) :
                pack_mule_killed = True
                playfield.hand.append(card_library.Squirrel())
                one_cost = random_card(card_library.Poss_Playr[1])
                two_cost = random_card(card_library.Poss_Playr[2])
                bone_card = random_card(card_library.Poss_Playr[1]) # until bones are implemented
                playfield.hand.append(one_cost)
                playfield.hand.append(two_cost)
                playfield.hand.append(bone_card)

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
                print(QoL.center_justified('The cards shatter into gold nuggets.'))
                print()
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
                        print()
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
                        print()
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
                    print(QoL.center_justified('You can see the fins of sharks circling.'))
                    print()
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
                    print(QoL.center_justified('"Well, I can\'t let you beat my game that easily."'))
                    print()
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
        return card_battle(campaign) # for testing prior to implementation

    return gameplay(campaign) # add flavor text, context, etc.

def boss_fight_leshy(campaign) : # boss fight 4
    def gameplay(campaign) :
        return card_battle(campaign) # for testing prior to implementation

    return gameplay(campaign) # add flavor text, context, etc.