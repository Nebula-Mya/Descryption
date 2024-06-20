import card
import card_library
import QoL
import ASCII_text
import copy
import random
import os
import duel
import sigils

def ai_category_checking(categories, player_field, card_to_play, bushes, score, strat_change_threshold) :
    '''
    checks the categories and current game state to determine which zones Leshy should play to

    Arguments:
        categories: the categories to check (list)
        player_field: the player's field (dict)
        card_to_play: the card Leshy is considering playing (card)
        bushes: the bushes on the field (dict)
        score: the score of the game (dict)
        strat_change_threshold: the score difference in Leshy's favor that will trigger a change in his strategy (int)

    Returns:
        in_strategy: the zones in strategy (list)
        out_of_strategy: the zones out of strategy (list)
    '''
    # set up variables
    in_strategy = []
    out_of_strategy = []
    influenced = False

    # steps of the strategy:
    # 1. Check if Leshy is winning enough to go on the offensive, regardless of card category
    # 2. Check for categories/strategies in order of priority
    # 3. For those not in a category or whose category did not apply (defensive)
    # 4. Remove zones that are countered by player's cards from the strategy

    # Leshy winning enough to go on the offensive, regardless of card category
    if (score['opponent'] - score['player'] >= strat_change_threshold) and (card_to_play.base_attack > 0): 
        in_strategy += [zone for zone in range(1, 6) if bushes[zone].species == '' and player_field[zone].species == '']

        out_of_strategy += [zone for zone in range(1, 6) if bushes[zone].species == '' and zone not in in_strategy]

        influenced = bool(in_strategy) # only influence if strat applies to at least 1 zone, otherwise allow it to continue to the next strat

    # check for categories/strategies in order of priority
    for category in (category for category in categories if not influenced and card_to_play.species in category['cards']) : # generator to prevent checking categories if already influenced and reduce memory usage
        out_of_strategy = [] # reset incase previous category didn't apply to any zones

        in_strategy += [zone for zone in range(1, 6) if bushes[zone].species == '' and player_field[zone].sigil in category['deals_with']]

        out_of_strategy += [zone for zone in range(1, 6) if bushes[zone].species == '' and zone not in in_strategy]

        influenced = bool(in_strategy) # only influence if strat applies to at least 1 zone, otherwise allow it to continue to the next strat

    # for those not in a category or whose category did not apply (defensive)
    if not influenced :
        out_of_strategy = [] # reset incase previous category didn't apply to any zones

        in_strategy += [zone for zone in range(1, 6) if bushes[zone].species == '' and player_field[zone].species != '']

        out_of_strategy += [zone for zone in range(1, 6) if bushes[zone].species == '' and zone not in in_strategy]
    
    # check for cards that counter Leshy's cards
    for zone in [zone for category in categories if card_to_play.sigil in category['deals_with'] for zone in range(1, 6)] :
        both_right = 'right' in player_field[zone].sigil and 'right' in card_to_play.sigil
        both_left = 'left' in player_field[zone].sigil and 'left' in card_to_play.sigil
        if both_right or both_left : # guard clause for opposing shifting cards, which counter eachother
            continue

        if card_to_play.species in category['cards'] and zone in in_strategy :
            out_of_strategy.append(zone)
            in_strategy.remove(zone)

    return in_strategy, out_of_strategy

def get_corpse_eaters(hand) :
    '''
    gets the indexes of all corpse eaters in the hand

    Arguments:
        hand: the player's hand (list)

    Returns:
        corpse_eaters: the corpse eaters in the hand (list)
    '''
    corpse_eaters = []
    for card in [card for card in range(len(hand)) if hand[card].species == 'Corpse Eater'] :
        corpse_eaters.append(card)
    return corpse_eaters

class Playmat :
    '''
    The field of play, including the bushes, the cards in play, the player's hand, and the score.

    Arguments:
        deck: the player's main deck (list)
        squirrels: the player's resource deck (list)
        opponent_deck: Leshy's deck (list)
        Leshy_play_count_median: the number of cards Leshy will play each turn, defaults to 2 (int)
        Leshy_play_count_variance: the variance of the number of cards Leshy will play each turn, defaults to 1 (int)
        Leshy_in_strategy_chance: the percent chance that Leshy will play a card in strategy (as opposed to out of strategy), defaults to 75 (int)
        Leshy_strat_change_threshold: the score difference in Leshy's favor that will trigger a change in his strategy, defaults to 3 (int)
    
    Other Attributes:
        bushes: the bushes on the field (dict)
        player_field: the cards in play (dict)
        opponent_field: Leshy's cards in play (dict)
        hand: the cards in the player's hand (list)
        graveyard: the cards in the graveyard (list)
        score: the score of the game (dict)
        active: the active player (str)

    Methods:
        draw(deck) : draws a card from the deck to the hand
        play_card(index, zone) : plays a card to the field (first opens card explanation and has player select saccs, then plays card to zone)
        attack() : attacks with all of the active player's cards in play and updates score
        check_states() : checks for dead cards and removes them, plus returns unkillables if player's turn
        advance() : advances cards from bushes to field
        switch() : switches the active player
        check_win() : checks for a win condition
        print_remaining() : prints the remaining cards in the deck (sorted) and the squirrels (sorted)
        print_graveyard() : prints the cards in the graveyard (in order)
        print_hand() : prints the cards in the player's hand
        print_field() : prints the field and score scales
        print_full_field() : prints the field and player's hand
    '''
    def __init__(self, deck, squirrels, opponent_deck, Leshy_play_count_median=2, Leshy_play_count_variance=1, Leshy_in_strategy_chance=75, Leshy_strat_change_threshold=3) :
        # basic variables
        self.hand = []
        self.graveyard = []
        self.score = {'player': 0, 'opponent': 0}
        self.active = 'player'
        self.player_deck = deck
        self.player_squirrels = squirrels
        self.opponent_deck = opponent_deck
        self.Leshy_play_count_median = Leshy_play_count_median
        self.Leshy_play_count_variance = Leshy_play_count_variance
        self.Leshy_in_strategy_chance = Leshy_in_strategy_chance
        self.Leshy_strat_change_threshold = Leshy_strat_change_threshold

        # create the rows of the field
        gen_blank_row = lambda: {column: card.BlankCard() for column in range(7)}
        self.bushes = gen_blank_row()
        self.player_field = gen_blank_row()
        self.opponent_field = gen_blank_row()
    
    def draw(self, deck) :
        '''
        draws a card from a deck to the hand
        
        Arguments:
            deck: the deck to draw from (str) (main or resource)
        '''
        match deck :
            case 'main' :
                if self.player_deck == [] :
                    raise ValueError('Deck is empty.')
                self.hand.append(self.player_deck[0])
                self.player_deck.pop(0)

                # show card explanation
                self.print_field()
                self.hand[-1].explain()
                input('Press enter to continue.')

            case 'resource' :
                if self.player_squirrels == [] :
                    raise ValueError('Deck is empty.')
                self.hand.append(self.player_squirrels[0])
                self.player_squirrels.pop(0)

    def play_card(self, index, zone) :
        '''
        plays a card to the field from the hand (first opens card explanation and has player select saccs, then plays card to zone)

        Arguments:
            index: the index of the card in the hand (int)
            zone: the zone to play the card to (int)
        
        Returns:
            played: if the card was played (bool)
        '''
        # set up variables
        cost = self.hand[index].saccs
        og_cost = cost
        sacc_list = []

        # update display
        self.print_field()
        self.hand[index].explain()
        print('Sacrifices required:', cost)
        print('Select sacrifices: (press enter to go back)', end=' ')

        def fail_saccs() :
                sacc_list = []
                cost = og_cost # to prevent goat cheesing
                return [sacc_list, cost]

        # get sacrifices
        while not (len(sacc_list) == cost) :
            sacc_index_list = input('')

            if sacc_index_list == '' : # go back if user presses enter
                return False
            
            sacc_indexes = [int(sacc) for sacc in sacc_index_list if sacc in [str(n) for n in range(1, 6)]] # get valid saccs

            for goat in [sacc for sacc in sacc_indexes if self.player_field[sacc].sigil == 'worthy sacrifice'] : # decrease cost for cards with worthy sacrifice
                cost -= 2

            if len(sacc_indexes) > cost - len(sacc_list) : # too many saccs, serves as guard clause
                print('Too many sacrifices.')
                [sacc_list, cost] = fail_saccs() # reset saccs and cost to prevent player confusion, may change if alternate behavior is desired
                continue

            for sacc_index in sacc_indexes :
                if sacc_index not in range(1, 6) or sacc_index in sacc_list or self.player_field[sacc_index].species == '' : # invalid zone
                    print(str(sacc_index), 'is an invalid zone.')
                    break # do not reset, just don't add the sacc, may change if alternate behavior is desired
                else :
                    sacc_list.append(sacc_index)

            if self.player_field[zone].species == '' or len(sacc_list) != cost : # guard clause for playing on top of a card
                continue
            if zone not in sacc_list : # playing on top of a card that wasn't sacrificed
                print('Cannot play on top of a non sacrificed card.')
                [sacc_list, cost] = fail_saccs()
            elif self.player_field[zone].sigil == 'many lives' : # playing on top of a card with many lives
                print('Cannot play on top of a card with many lives.')
                [sacc_list, cost] = fail_saccs()
        
        # remove saccs
        for ind in sacc_list :
            QoL.exec_sigil_code(self.player_field[ind], sigils.on_sacrifices, None, locals())

            if self.player_field[ind].species == 'Cat' and self.player_field[ind].sigil == 'many lives' : # make sure cat still has many lives
                self.player_field[ind].spent_lives += 1
                if self.player_field[ind].spent_lives >= 9 :
                    self.player_field[ind] = card_library.UndeadCat()
            else :
                self.player_field[ind].die()

            if self.player_field[ind].sigil not in sigils.on_sacrifices :
                self.graveyard.insert(0, self.player_field[ind])
                self.player_field[ind] = card.BlankCard()
        else : 
            # play card to zone
            self.player_field[zone] = self.hand[index]
            self.player_field[zone].play(zone=zone)
            self.hand.pop(index)
            
            # handle sigils
            QoL.exec_sigil_code(self.player_field[zone], sigils.on_plays, None, locals())

            self.print_field()
            return True
    
    def attack(self) :
        '''
        attacks with all of the active player's cards in play and updates score
        '''
        did_shift = False
        if self.active == 'player' :
            attacking_field = self.player_field
            defending_field = self.opponent_field
            is_players = True
        else :
            attacking_field = self.opponent_field
            defending_field = self.player_field
            is_players = False

        # attacking
        for zone in attacking_field :
            if attacking_field[zone].species != '' and attacking_field[zone].zone != 0 and attacking_field[zone].zone != 6 :
                attacker_points = attacking_field[zone].attack(defending_field[zone-1],defending_field[zone],defending_field[zone+1], self.hand, is_players=is_players, bushes=self.bushes)

                # score update
                self.score[self.active] += attacker_points

        # moving sigils
        for zone in attacking_field :
            if did_shift :
                did_shift = False
            else :
                [did_shift] = QoL.exec_sigil_code(attacking_field[zone], sigils.movers, None, locals(), ['did_shift'] )

    def check_states(self) :
        '''
        checks for dead cards and removes them, plus returns unkillables if player's turn. Also summons corpse eaters if necessary.
        '''
        # set up variables
        corpses = []
        open_corpses = []

        # check for dead cards in each field
        for current_field in [self.player_field, self.opponent_field, self.bushes] :
            for zone in current_field :

                # if a sigil applies
                [corpses] = QoL.exec_sigil_code(current_field[zone], sigils.on_deaths, None, locals(), ['corpses'])

                # if a normal card dies
                if current_field[zone].status == 'dead' and (current_field[zone].sigil not in sigils.on_deaths) :
                    current_field[zone].die()
                    current_field[zone] = card.BlankCard()
                    current_field[zone].play(zone)
                    corpses.append(zone)

        # check for corpse eaters
        for zone in corpses :
            if self.player_field[zone].species == '' :
                open_corpses.append(zone)
        corpse_eaters = get_corpse_eaters(self.hand)
        exhausted = False
        while not exhausted :
            if open_corpses != [] and corpse_eaters !=[] :
                zone_choice = random.choice(open_corpses)
                self.player_field[zone_choice] = self.hand[corpse_eaters[0]]
                self.player_field[zone_choice].play(zone_choice)
                self.hand.pop(corpse_eaters[0])
                open_corpses.remove(zone_choice)
                corpse_eaters = get_corpse_eaters(self.hand)
            else :
                exhausted = True

    def advance(self) : 
        '''
        advances cards from bushes to field, utilizing rudimentary decision making for Leshy
        '''
        #region constant variables and random gen
        # play count is the number of cards that leshy will play that turn
        play_count_median = self.Leshy_play_count_median

        # shift range slightly to match amount of cards on player's field
        player_card_count = 0
        for zone in range(1, 6) :
            if self.player_field[zone].species != '' :
                player_card_count += 1
        if player_card_count > 3 :
            play_count_median += 1
        elif player_card_count < 2 :
            play_count_median -= 1

        play_count_variance = self.Leshy_play_count_variance
        play_count = random.randint(play_count_median - play_count_variance, play_count_median + play_count_variance)
        if play_count < 1 :
            play_count = 1
        elif play_count > 5 :
            play_count = 5

        # in_strategy_chance is the percent chance that leshy will play a card in strategy (as opposed to out of strategy)
        in_strategy_chance = self.Leshy_in_strategy_chance

        # strat_change_threshold is the score difference in Leshy's favor that will trigger a change in his strategy
        strat_change_threshold = self.Leshy_strat_change_threshold
        #endregion

        #region advance from bushes to field
        for zone in self.opponent_field :
            if self.opponent_field[zone].species == '' and zone != 0 and zone != 6 :
                self.opponent_field[zone] = self.bushes[zone]
                self.opponent_field[zone].play(zone=zone)
                # always replace with BlankCard, new cards will be played (and replace the BlankCard) in the new section
                self.bushes[zone] = card.BlankCard()
        #endregion

        # prevent crash if opponent deck is empty
        if self.opponent_deck == [] :
            return
        
        played = 0
        while played < play_count :
            
            # intelligent choosing of zones to prioritize
            in_strategy, out_of_strategy = ai_category_checking(card_library.AI_categories, self.player_field, self.opponent_deck[0], self.bushes, self.score, strat_change_threshold)

            # ensure that the loop will not run if there are no zones to play to, preventing infinite loop
            if len(in_strategy) + len(out_of_strategy) == 0 :
                open_zone = False
                for zone in range(1, 6) :
                    if self.bushes[zone].species == '' :
                        open_zone = True
                if open_zone == False : # if all zones are full, stop here
                    break
                # move top card to bottom
                garnet = self.opponent_deck[0]
                self.opponent_deck.pop(0)
                self.opponent_deck.append(garnet)
                # continue to next loop
                continue

            #region playing cards to zones
            # play cards in strategy
            if (random.randint(1,100) <= in_strategy_chance and in_strategy != []) or out_of_strategy == [] :
                zone = random.choice(in_strategy)
                self.bushes[zone] = self.opponent_deck[0]
                self.opponent_deck.pop(0)
            
            else :
                zone = random.choice(out_of_strategy)
                self.bushes[zone] = self.opponent_deck[0]
                self.opponent_deck.pop(0)

            played += 1
            #endregion

    def switch(self) :
        '''
        switches the active player
        '''
        if self.active == 'player' :
            self.active = 'opponent'
        elif self.active == 'opponent' :
            self.active = 'player'

    def check_win(self) :
        '''
        checks for a win condition

        Returns:
            win: if a win condition has been met (bool)
            winner: the winner of the game (str)
            overkill: how much the player overkilled by (int)
        '''
        win = False
        winner = ''
        overkill = 0
        if self.score['player'] - self.score['opponent'] >= 8 :
            win = True
            winner = 'player'
            overkill = self.score['player'] - self.score['opponent'] - 8
        elif self.score['opponent'] - self.score['player'] >= 8 :
            win = True
            winner = 'opponent'
        elif self.player_deck == [] and self.player_squirrels == [] and self.active == 'player' :
            win = True
            winner = 'opponent'
        return (win, winner, overkill)

    def print_remaining(self) :
        '''
        prints the remaining cards in the deck (sorted) and the squirrels (sorted) (clears screen first)
        '''
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        sorted_main_deck = sorted(self.player_deck, key=lambda x: x.name)
        sorted_main_deck = sorted(sorted_main_deck, key=lambda x: x.cost)
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8 
        chunked = QoL.chunk(sorted_main_deck, cards_per_row)  
        deck_string = ''
        for chunk in chunked :
            for n in range(11) :
                deck_string += ' '*card_gaps
                for card in chunk :
                    deck_string += card.text_by_line() + ' '*card_gaps
                deck_string += '\n'
            deck_string += '\n'
        QoL.clear()
        print(' '*card_gaps + 'Remaining cards in deck:')
        print(deck_string, end='')
        print(' '*card_gaps + 'Remaining squirrels: ' + str(len(self.player_squirrels)))

    def print_graveyard(self) :
        '''
        prints the cards in the graveyard (in order) (clears screen first)
        '''
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8 
        chunked = QoL.chunk(self.graveyard, cards_per_row)  
        graveyard_string = ''
        for chunk in chunked :
            for n in range(11) :
                graveyard_string += ' '*card_gaps
                for card in chunk :
                    graveyard_string += card.text_by_line() + ' '*card_gaps
                graveyard_string += '\n'
            graveyard_string += '\n'
        QoL.clear()
        print(' '*card_gaps + 'Graveyard:')
        print(graveyard_string, end='')
    
    def print_hand(self) : 
        '''
        prints the cards in the player's hand (does NOT clear screen first)
        '''
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8 
        chunked = QoL.chunk(self.hand, cards_per_row) 
        hand_string = ''
        for chunk in chunked :
            for n in range(11) :
                hand_string += ' '*card_gaps
                for card in chunk :
                    hand_string += card.text_by_line() + ' '*card_gaps
                hand_string += '\n'
        print(' '*card_gaps + 'Hand:')
        print(hand_string, end='')

    def print_field(self) :
        '''
        prints the field and score scales (clears screen first)
        '''
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        QoL.clear()
        vis_bushes = [self.bushes[1], self.bushes[2], self.bushes[3], self.bushes[4], self.bushes[5]]
        vis_opponent_field = [self.opponent_field[1], self.opponent_field[2], self.opponent_field[3], self.opponent_field[4], self.opponent_field[5]]
        vis_player_field = [self.player_field[1], self.player_field[2], self.player_field[3], self.player_field[4], self.player_field[5]]
        field_list = [vis_bushes, vis_opponent_field, vis_player_field]
        field_string = ''
        for row in field_list :
            for n in range(11) :
                field_string += ' '*card_gaps*3
                for card in row :
                    field_string += card.text_by_line() + ' '*card_gaps*3
                field_string += '\n'
            if row == vis_opponent_field :
                if card_gaps <= 0 :
                    field_string += '-'*75 + '\n'
                else :
                    field_string += ' '*card_gaps + '-'*(card_gaps*16 + 75) + '\n'
        print(field_string, end='')
        # print scales
        if self.score['player'] > self.score['opponent'] :
            if self.score['player'] - self.score['opponent'] >= 8 :
                player_weight = 'O'*8
                opponent_weight = ' '*8
            else :
                player_weight = 'O' * (self.score['player'] - self.score['opponent'])
                player_weight += ' ' * (8 - (self.score['player'] - self.score['opponent']))
                opponent_weight = ' '*8
        elif self.score['opponent'] > self.score['player'] :
            if self.score['opponent'] - self.score['player'] >= 8 :
                opponent_weight = 'O'*8
                player_weight = ' '*8
            else :
                opponent_weight = ' ' * (8 - (self.score['opponent'] - self.score['player']))
                opponent_weight += 'O' * (self.score['opponent'] - self.score['player'])
                player_weight = ' '*8
        else :
            player_weight = ' '*8
            opponent_weight = ' '*8
        ASCII_text.print_scales(player_weight, opponent_weight)

    def print_full_field(self) :
        '''
        prints the field and player's hand (clears screen first)
        '''
        self.print_field()
        self.print_hand()

if __name__ == '__main__' :
    def test_advancing() :
            QoL.clear()

            # create decks
            leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
            player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
            player_squirrels = duel.resource_gen()

            # Create a sample playmat with cards on the field
            playmat = Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
            card_list = []
            for cost in card_library.Poss_Playr :
                for species in card_library.Poss_Playr[cost] :
                    card_list.append(species)
                    card_list.append(card.BlankCard())
            for zone in range(1, 6) :
                playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))

            # Call the advance method
            playmat.advance()

            # Print the field after advancing
            playmat.print_field()

    def test_split_dam() :
        QoL.clear()

        # create decks
        leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
        player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
        player_squirrels = duel.resource_gen()

        # Create a sample playmat with cards on the field
        playmat = Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 6) :
            if zone == 3 :
                playmat.player_field[zone] = card.BlankCard()
                continue
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))
        
        # place a split card in the middle of leshy's field and advance twice
        playmat.opponent_field[3] = card_library.BoppitW(True)
        playmat.advance()
        playmat.advance()

        # print the field
        playmat.print_field()

        # get user input before advancing
        input("Press enter to advance. (summoning a dam builder to zone 3)")

        # place a dam builder in the middle of player's field
        playmat.hand.append(card_library.Beaver())
        playmat.hand[0].saccs = 0
        playmat.play_card(0, 3)

        # print the field
        playmat.print_field()

        # get user input before advancing
        input("Press enter to advance. (kill the split card)")

        # kill the split card
        playmat.opponent_field[3].status = 'dead'
        playmat.check_states()

        # print the field
        playmat.print_field()

    def test_corpse_eaters() :
        QoL.clear()

        # create decks
        leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
        player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
        player_squirrels = duel.resource_gen()

        # Create a sample playmat with cards on the field
        playmat = Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 6) :
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))
        
        # populate hand
        for n in range(6) :
            if random.randint(1, 2) == 1 :
                playmat.hand.append(card.BlankCard(species='Corpse Eater', cost=1, attack=1, life=1, sigil='corpse eater', status='alive', blank_cost=True))
            else :
                playmat.hand.append(card_library.Squirrel())
        
        # print the field
        playmat.print_full_field()

        # get user input
        input("Press enter to advance. (kill 2 cards)")

        # kill 2 cards and check states
        cards_to_kill = []
        for zone in range(1, 6) :
            if playmat.player_field[zone].species != '' :
                cards_to_kill.append(zone)
        kill_count = 2
        if len(cards_to_kill) < 2 :
            kill_count = len(cards_to_kill)
        for n in range(kill_count) :
            zone_to_kill = random.choice(cards_to_kill)
            playmat.player_field[zone_to_kill].status = 'dead'
            cards_to_kill.remove(zone_to_kill)
        playmat.check_states()

        # print the field
        playmat.print_full_field()

    def test_hefty() :
        QoL.clear()

        # create decks
        leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
        player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
        player_squirrels = duel.resource_gen()

        # Create a sample playmat with cards on the field
        playmat = Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 6) :
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))
            playmat.player_field[zone].zone = zone

        # place a hefty card in the player's field
        playmat.player_field[2] = card_library.MooseBuck()
        playmat.player_field[2].play(zone=2)
        playmat.player_field[2].sigil = 'hefty (right)'
        playmat.player_field[2].update_ASCII()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        # get user input before advancing
        input("Press enter to advance. (move the hefty card to the right)")

        # advance
        playmat.attack()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        # get user input before advancing
        input("Press enter to advance. (place a card to the right)")

        # place a card to the right of the hefty card
        playmat.player_field[4] = card_library.Squirrel()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        # get user input before advancing
        input("Press enter to advance. (move the hefty card to the right)")

        # advance
        playmat.attack()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        # get user input before advancing
        input("Press enter to advance. (move the hefty card to the right)")

        # advance
        playmat.attack()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

    def test_empty_deck() :
        QoL.clear()

        # create decks
        leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
        player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
        player_squirrels = duel.resource_gen()

        # Create a sample playmat with cards on the field
        playmat = Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 6) :
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))
            playmat.player_field[zone].zone = zone
        playmat.print_full_field()

        # empty squirrels
        playmat.player_squirrels = []

        # draw with empty squirrels
        input("Press enter to draw with empty squirrels.")
        duel.choose_draw(playmat)

        # empty deck
        playmat.player_deck = []
        playmat.player_squirrels = duel.resource_gen().shuffle()

        # draw with empty deck
        input("Press enter to draw with empty deck.")
        duel.choose_draw(playmat)

        # see hand
        input("Press enter to see hand.")
        playmat.print_full_field()

    # test_advancing()
    # test_split_dam()
    # test_corpse_eaters()
    # test_hefty()
    test_empty_deck()

    pass