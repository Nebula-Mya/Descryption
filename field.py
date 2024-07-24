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
    def is_in_strat(card_to_play, opp_card, sigil_slot) :
        # set up variables
        self_attack = card_to_play.current_attack
        self_life = card_to_play.current_life
        opp_attack = opp_card.current_attack
        opp_life = opp_card.current_life

        # check for categories
        for category in [category for category in categories if opp_card.sigil_in_category(category['opp sigils'])] :
            if card_to_play.sigil_in_category(category['self sigils'], sigil_slot) or category['stats'](self_attack, self_life, opp_attack, opp_life) :
                return True
        
        # if no categories apply
        if opp_card.species != '' and (self_life > opp_attack or self_attack >= opp_life or opp_attack >= 4) :
            return True
        
        return False
    
    def is_out_strat(card_to_play, opp_card, sigil_slot) :
        # set up variables
        self_attack = card_to_play.current_attack
        self_life = card_to_play.current_life
        opp_attack = opp_card.current_attack
        opp_life = opp_card.current_life

        # check for counters
        for category in [category for category in categories if opp_card.sigil_in_category(category['self sigils'])] :
            if card_to_play.sigil_in_category(category['opp sigils'], sigil_slot) or category['stats'](opp_attack, opp_life, self_attack, self_life) :
                return True
        
        return False
    
    def add_to_in_strat(card_to_play, player_field, bushes, zone) :
        # error handling
        if zone not in range(1, 5) :
            raise ValueError('Invalid zone.')
        
        # set up variables
        opp_card = player_field[zone]
        bush_empty = bushes[zone].species == ''

        # if Leshy is winning enough to go on the offensive, regardless of card category
        if (score['opponent'] - score['player'] >= strat_change_threshold) and (card_to_play.base_attack > 0) :
            if bush_empty and opp_card.species == '' :
                return True
            else :
                False
        
        # get booleans
        s1_in_strat_check = is_in_strat(card_to_play, opp_card, 0)
        s1_out_strat_check = is_out_strat(card_to_play, opp_card, 0)
        s2_in_strat_check = is_in_strat(card_to_play, opp_card, 1)
        s2_out_strat_check = is_out_strat(card_to_play, opp_card, 1)

        # combine booleans
        in_strat_check = s1_in_strat_check or s2_in_strat_check
        out_strat_check = s1_out_strat_check or s2_out_strat_check

        match (in_strat_check, out_strat_check, bush_empty) :
            case (True, False, True) :
                return True
            case _ :
                return False
    
    in_strategy = [zone for zone in range(1, 5) if add_to_in_strat(card_to_play, player_field, bushes, zone)]
    out_of_strategy = [zone for zone in range(1, 5) if zone not in in_strategy]

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
    for card in [card for card in range(len(hand)) if hand[card].has_sigil('corpse eater')] : 
        corpse_eaters.append(card)
    return corpse_eaters

class Playmat :
    '''
    The field of play, including the bushes, the cards in play, the player's hand, and the score.

    Arguments:
        deck: the player's main deck (list)
        squirrels: the player's resource deck (list)
        opponent_deck: Leshy's deck (list)
        Leshy_play_count_median: the number of cards Leshy will play each turn (int)
        Leshy_play_count_variance: the variance of the number of cards Leshy will play each turn (int)
        Leshy_in_strategy_chance: the percent chance that Leshy will play a card in strategy (as opposed to out of strategy) (int)
        Leshy_strat_change_threshold: the score difference in Leshy's favor that will trigger a change in his strategy (int)
    
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
    def __init__(self, deck, squirrels, opponent_deck, Leshy_play_count_median, Leshy_play_count_variance, Leshy_in_strategy_chance, Leshy_strat_change_threshold) :
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
        gen_blank_row = lambda: {column: card.BlankCard() for column in range(6)}
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
        # error handling
        if index not in range(len(self.hand)) :
            raise ValueError('Invalid index.')
        if zone not in range(1, 5) :
            raise ValueError('Invalid zone.')

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
            
            sacc_indexes = [int(sacc) for sacc in sacc_index_list if sacc in [str(n) for n in range(1, 5)]] # get valid saccs

            for _ in [sacc for sacc in sacc_indexes if self.player_field[sacc].has_sigil('worthy sacrifice')] : # decrease cost for cards with worthy sacrifice
                cost -= 2 
                if cost < 0 :
                    cost = 0

            if len(sacc_indexes) > cost - len(sacc_list) : # too many saccs, serves as guard clause
                print('Too many sacrifices.')
                [sacc_list, cost] = fail_saccs() # reset saccs and cost to prevent player confusion, may change if alternate behavior is desired
                continue

            for sacc_index in sacc_indexes :
                if sacc_index not in range(1, 5) or sacc_index in sacc_list or self.player_field[sacc_index].species == '' : # invalid zone
                    print(str(sacc_index), 'is an invalid zone.')
                    break # do not reset, just don't add the sacc, may change if alternate behavior is desired
                else :
                    sacc_list.append(sacc_index)

            if self.player_field[zone].species == '' or len(sacc_list) != cost : # guard clause for playing on top of a card
                continue
            if zone not in sacc_list : # playing on top of a card that wasn't sacrificed
                print('Cannot play on top of a non sacrificed card.')
                [sacc_list, cost] = fail_saccs()
            elif self.player_field[zone].has_sigil('many lives') : # playing on top of a card with many lives
                print('Cannot play on top of a card with many lives.')
                [sacc_list, cost] = fail_saccs()
        
        # remove saccs
        for ind in sacc_list :
            QoL.exec_sigil_code(self.player_field[ind], sigils.on_sacrifices, None, locals())

            if self.player_field[ind].species == 'Cat' and self.player_field[ind].has_sigil('many lives') : # make sure cat still has many lives
                self.player_field[ind].spent_lives += 1
                if self.player_field[ind].spent_lives >= 9 :
                    self.player_field[ind] = card_library.UndeadCat()
            else :
                self.player_field[ind].die()

            if not self.player_field[ind].sigil_in_category(sigils.on_sacrifices) :
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
        # set up variables
        did_shift = False
        match self.active :
            case 'player' :
                attacking_field = self.player_field
                defending_field = self.opponent_field
                is_players = True
            case 'opponent' :
                attacking_field = self.opponent_field
                defending_field = self.player_field
                is_players = False
            case _ :
                raise ValueError('Invalid active player.')

        # attacking
        for zone in attacking_field :
            if attacking_field[zone].species != '' and attacking_field[zone].zone != 0 and attacking_field[zone].zone != 5 :
                attacker_points = attacking_field[zone].attack(defending_field[zone-1],defending_field[zone],defending_field[zone+1], self.hand, is_players=is_players, bushes=self.bushes)

                # score update
                self.score[self.active] += attacker_points

        # moving sigils
        for zone in attacking_field :
            if did_shift :
                did_shift = False
            else :
                [did_shift] = QoL.exec_sigil_code(attacking_field[zone], sigils.movers, None, locals(), ['did_shift'])

    def check_states(self) :
        '''
        checks for dead cards and removes them, plus returns unkillables if player's turn. Also summons corpse eaters if necessary.
        '''
        # set up variables
        corpses = []

        # check for dead cards
        for current_field, zone in [(current_field, zone) for current_field in [self.player_field, self.opponent_field, self.bushes] for zone in current_field] :
            # if a sigil applies
            [corpses] = QoL.exec_sigil_code(current_field[zone], sigils.on_deaths, None, locals(), ['corpses'])

            # if a normal card dies
            if current_field[zone].status == 'dead' and not current_field[zone].sigil_in_category(sigils.on_deaths) :
                current_field[zone].die()
                current_field[zone] = card.BlankCard()
                current_field[zone].play(zone)
                corpses.append((zone, current_field))
        
        # check for corpse eaters
        open_corpses = [corpse for (corpse, field) in corpses if field == self.player_field and self.player_field[corpse].species == '']
        corpse_eaters = get_corpse_eaters(self.hand)

        # play corpse eaters
        while open_corpses and corpse_eaters :
            zone_choice = random.choice(open_corpses)
            self.player_field[zone_choice] = self.hand[corpse_eaters[0]]
            self.player_field[zone_choice].play(zone_choice)
            self.hand.pop(corpse_eaters[0])
            open_corpses.remove(zone_choice)
            corpse_eaters = get_corpse_eaters(self.hand) # update corpse eaters

    def advance(self) : 
        '''
        advances cards from bushes to field, utilizing rudimentary decision making for Leshy
        '''
        # set up variables
        played = 0
        player_card_count = len([card_in_play for card_in_play in self.player_field.values() if card_in_play.species != ''])
        play_count_median = self.Leshy_play_count_median + (player_card_count > 2) - (player_card_count < 2) # shift range slightly to match amount of cards on player's field
        play_count = random.randint(play_count_median - self.Leshy_play_count_variance, play_count_median + self.Leshy_play_count_variance)
        play_count = max(min(play_count, len(self.opponent_deck), 4), 1) if self.opponent_deck else 0 # clamp play count

        # advance from bushes to field
        for zone in [zone for zone in self.opponent_field if self.opponent_field[zone].species == '' and zone % 5 != 0] :
            self.opponent_field[zone] = self.bushes[zone]
            self.opponent_field[zone].play(zone=zone)
            self.bushes[zone] = card.BlankCard()
        
        while played < play_count and [zone for zone in range(1, 5) if self.bushes[zone].species == ''] :
            # intelligent choosing of zones to prioritize
            in_strategy, out_of_strategy = ai_category_checking(card_library.AI_categories, self.player_field, self.opponent_deck[0], self.bushes, self.score, self.Leshy_strat_change_threshold)

            # playing cards to zones
            if (random.randint(1,100) <= self.Leshy_in_strategy_chance and in_strategy) or not out_of_strategy:
                zone = random.choice(in_strategy)
                self.bushes[zone] = self.opponent_deck[0]
                self.opponent_deck.pop(0)
            else :
                zone = random.choice(out_of_strategy)
                self.bushes[zone] = self.opponent_deck[0]
                self.opponent_deck.pop(0)

            played += 1

    def switch(self) :
        '''
        switches the active player
        '''
        if self.active == 'player' :
            self.active = 'opponent'
        elif self.active == 'opponent' :
            self.active = 'player'
        else :
            raise ValueError('Invalid active player.')

    def check_win(self) :
        '''
        checks for a win condition

        Returns:
            win: if a win condition has been met (bool)
            winner: the winner of the game (str)
            overkill: how much the player overkilled by (int)
            deck_out: if the player lost by running out of cards (bool)
        '''
        if abs(self.score['player'] - self.score['opponent']) < 5 and (self.player_deck != [] or self.player_squirrels != [] or self.active != 'player') : # no win condition
            return False, '', 0, False
        
        if self.score['player'] - self.score['opponent'] >= 5 : # player wins
            return True, 'player', self.score['player'] - self.score['opponent'] - 5, False
        
        elif self.score['opponent'] - self.score['player'] >= 5 : # opponent wins via score
            return True, 'opponent', 0, False
        
        return True, 'opponent', 0, True # opponent wins via deck out

    def print_remaining(self) :
        '''
        prints the remaining cards in the deck (sorted) and the squirrels (sorted) (clears screen first)
        '''
        # set up variables
        term_cols = os.get_terminal_size().columns
        card_gaps_space = ' '*((term_cols*55 // 100) // 5 - 15)
        deck_string = QoL.print_deck(self.player_deck, sort=True, fruitful=True, numbered=True)

        # print remaining cards in deck
        QoL.clear()
        print(card_gaps_space + 'Remaining cards in deck:')
        print(deck_string + '\n')
        print(card_gaps_space + 'Remaining squirrels: ' + str(len(self.player_squirrels)) + '\n')

    def print_graveyard(self) :
        '''
        prints the cards in the graveyard (in order) (clears screen first)
        '''
        # set up variables
        term_cols = os.get_terminal_size().columns
        card_gaps_space = ' '*((term_cols*55 // 100) // 5 - 15)
        graveyard_string = QoL.print_deck(self.graveyard, sort=False, fruitful=True, numbered=True)

        # print graveyard
        QoL.clear()
        print(card_gaps_space + 'Graveyard:')
        print(graveyard_string, end='')
    
    def print_hand(self) : 
        '''
        prints the cards in the player's hand (does NOT clear screen first)
        '''
        # set up variables
        term_cols = os.get_terminal_size().columns
        card_gaps_space = ' '*((term_cols*55 // 100) // 5 - 15)
        hand_string = QoL.print_deck(self.hand, sort=False, fruitful=True)

        # print hand
        print(card_gaps_space + 'Hand:', end='')
        print(hand_string)

    def print_field(self) :
        '''
        prints the field and score scales (clears screen first)
        '''
        # set up variables
        field_string = ''
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        if card_gaps <= 0 :
            score_gap = 31
        else :
            score_gap = card_gaps*6 + 31
        vis_bushes = [self.bushes[n] for n in range(1, 5)]
        vis_opponent_field = [self.opponent_field[n] for n in range(1, 5)]
        vis_player_field = [self.player_field[n] for n in range(1, 5)]

        # generate field string
        for row in [vis_bushes, vis_opponent_field, vis_player_field] :
            for _ in range(11) :
                field_string += ' '*card_gaps*3 + ''.join(card.text_by_line() + ' ' * (card_gaps * 3) for card in row) + '\n'

            field_string += ' '*card_gaps + '-'*(card_gaps*13 + 60) + '\n' if row == vis_opponent_field else '' # add a divider between opponent and player fields

        # print field
        QoL.clear()
        print(field_string, end='')
        ASCII_text.print_scales(self.score, score_gap)

    def print_full_field(self) :
        '''
        prints the field and player's hand (clears screen first)
        '''
        self.print_field()
        self.print_hand()

if __name__ == '__main__' :
    import sys

    def test_advancing() :
            QoL.clear()

            # create decks
            leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
            player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
            player_squirrels = duel.resource_gen(20)

            # Create a sample playmat with cards on the field
            playmat = Playmat(player_deck.shuffle(), player_squirrels.shuffle(), leshy_deck.shuffle(), 2, 1, 75, 3)
            card_list = []
            for cost in card_library.Poss_Playr :
                for species in card_library.Poss_Playr[cost] :
                    card_list.append(species)
                    card_list.append(card.BlankCard())
            for zone in range(1, 5) :
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
        player_squirrels = duel.resource_gen(20)

        # Create a sample playmat with cards on the field
        playmat = Playmat(player_deck.shuffle(), player_squirrels.shuffle(), leshy_deck.shuffle(), 2, 1, 75, 3)
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 5) :
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
        player_squirrels = duel.resource_gen(20)

        # Create a sample playmat with cards on the field
        playmat = Playmat(player_deck.shuffle(), player_squirrels.shuffle(), leshy_deck.shuffle(), 2, 1, 75, 3)
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 5) :
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))
        
        # populate hand
        for _ in range(5) :
            if random.randint(1, 2) == 1 :
                playmat.hand.append(card_library.CorpseMaggots(blank_cost=True))
            else :
                playmat.hand.append(card_library.Squirrel())
        
        # print the field
        playmat.print_full_field()

        # get user input
        input("Press enter to advance. (kill 2 cards)")

        # kill 2 cards and check states
        cards_to_kill = []
        for zone in range(1, 5) :
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
        def advance_hefty(playmat) :
            # get user input before advancing
            input("Press enter to advance.")

            # advance
            playmat.attack()

            # print the field
            playmat.print_field()
            print(playmat.player_field)

        QoL.clear()

        # create decks
        leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
        player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
        player_squirrels = duel.resource_gen(20)


        ### test hefty (right) ###
        # Create a sample playmat with cards on the field
        playmat = Playmat(player_deck.shuffle(), player_squirrels.shuffle(), leshy_deck.shuffle(), 2, 1, 75, 3)
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 5) :
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))
            playmat.player_field[zone].zone = zone

        # place a hefty card in the player's field
        playmat.player_field[2] = card_library.MooseBuck()
        playmat.player_field[2].play(zone=2)
        playmat.player_field[2].sigils = ['hefty (right)','']
        playmat.player_field[2].update_ASCII()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        advance_hefty(playmat)

        # get user input before advancing
        input("Press enter to play a squirrel to the right of the hefty card.")

        # place a card to the right of the hefty card
        playmat.player_field[4] = card_library.Squirrel()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        for _ in range(3) :
            advance_hefty(playmat)

        # get user input before moving on
        input("Press enter to move on to the next test.")

        ### test hefty (left) ###
        # Create a sample playmat with cards on the field
        playmat = Playmat(player_deck.shuffle(), player_squirrels.shuffle(), leshy_deck.shuffle(), 2, 1, 75, 3)
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 5) :
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))
            playmat.player_field[zone].zone = zone
        
        # place a hefty card in the player's field
        playmat.player_field[4] = card_library.MooseBuck()
        playmat.player_field[4].play(zone=4)
        playmat.player_field[4].sigils = ['hefty (left)','']
        playmat.player_field[4].update_ASCII()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        advance_hefty(playmat)

        # get user input before advancing
        input("Press enter to play a squirrel to the left of the hefty card.")

        # place a card to the left of the hefty card
        playmat.player_field[2] = card_library.Squirrel()

        # print the field
        playmat.print_field()
        print(playmat.player_field)

        for _ in range(3) :
            advance_hefty(playmat)

    def test_empty_deck() :
        QoL.clear()

        # create decks
        leshy_deck = duel.deck_gen(card_library.Poss_Leshy, 20)
        player_deck = duel.deck_gen(card_library.Poss_Playr, 20)
        player_squirrels = duel.resource_gen(20)

        # Create a sample playmat with cards on the field
        playmat = Playmat(player_deck.shuffle(), player_squirrels.shuffle(), leshy_deck.shuffle(), 2, 1, 75, 3)
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 5) :
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
        playmat.player_squirrels = duel.resource_gen(20).shuffle()

        # draw with empty deck
        input("Press enter to draw with empty deck.")
        duel.choose_draw(playmat)

        # see hand
        input("Press enter to see hand.")
        playmat.print_full_field()
    
    match sys.argv[1] :
        case 'advancing' :
            test_advancing()
        case 'split_dam' :
            test_split_dam()
        case 'corpse_eaters' :
            test_corpse_eaters()
        case 'hefty' :
            test_hefty()
        case 'empty_deck' :
            test_empty_deck()
        case _ :
            pass