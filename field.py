import card
import card_library
import deck
import QoL
import ASCII_text
import copy
import random
import os

def hefty_check(field, zone, direction) :
    '''
    recursively checks how many cards can be pushed by a card with hefty sigil

    Arguments:
        field: the field to check (dict)
        zone: the zone to check (int)
        direction: the direction to check (str)
    
    Returns:
        the number of cards that can be pushed (int)
    '''
    if direction == 'right' :
        if field[zone+1].species != '' and zone < 4 :
            return 1 + hefty_check(field, zone+1, direction)
        elif field[zone+1].species == '' and zone < 4:
            return 1
        else :
            return 0
    elif direction == 'left' :
        if field[zone-1].species != '' and zone > 2 :
            return 1 + hefty_check(field, zone-1, direction)
        if field[zone-1].species == '' and zone > 2 :
            return 1
        else :
            return 0

def ai_category_checking(categories, player_field, opponent_deck, bushes, score, strat_change_threshold, in_strategy_chance) :
    '''
    checks for cards in a category and assigns them to in_strategy or out_of_strategy

    Arguments:
        categories: the categories to check (list)
        player_field: the player's field (dict)
        opponent_deck: Leshy's deck (list)
        bushes: the bushes on the field (dict)
        score: the score of the game (dict)
        strat_change_threshold: the score difference in Leshy's favor that will trigger a change in his strategy (int)
        in_strategy_chance: the percent chance that leshy will play a card in strategy (as opposed to out of strategy) (int)

    Returns:
        in_strategy: the zones in strategy (list)
        out_of_strategy: the zones out of strategy (list)
    '''
    in_strategy = []
    out_of_strategy = []
    uninfluenced = True

    # check for strategy and categories, then assign zones to in_strategy or out_of_strategy
    # if a card in in a category, but the category does not apply, it will be checked for all other categories
    # if a card is not in a category, and Leshy is not past the strat change threshold, it will be played defensively
    # if a card is in a category, and it does apply, it will not be checked for other categories
    if (score['opponent'] - score['player'] >= strat_change_threshold) and (opponent_deck[0].base_attack > 0): # Leshy winning enough to go on the offensive, regardless of card category
        for zone in range(1, 6) :
            if bushes[zone].species == '' :
                if player_field[zone].species == '' :
                    in_strategy.append(zone)
                    uninfluenced = False
                else :
                    out_of_strategy.append(zone)

    # check for categories in order of priority
    for category in categories :
        if opponent_deck[0].species in category['cards'] and uninfluenced :
            out_of_strategy = []
            for zone in range(1, 6) :
                if bushes[zone].species == '' :
                    if player_field[zone].sigil in category['deals_with'] :
                        in_strategy.append(zone)
                        uninfluenced = False
                    else :
                        out_of_strategy.append(zone)

    # for those not in a category or whose category did not apply (defensive)
    if uninfluenced :
        out_of_strategy = []
        for zone in range(1, 6) :
            if bushes[zone].species == '' :
                if player_field[zone].species != '' :
                    in_strategy.append(zone)
                else :
                    out_of_strategy.append(zone)
    
    # check for cards that counter Leshy's cards
    for category in categories :
        if opponent_deck[0].sigil in category['deals_with'] :
            for zone in range(1, 6) :

                # left and right cards counter eachother, so it only focuses on anti shifting cards that don't move
                if category['category'] == 'anti_right' or category['category'] == 'anti_left' :
                    if opponent_deck[0].species in category['cards'] and ('left' not in player_field[zone].sigil) and ('right' not in player_field[zone].sigil) and random.randint(1,100) <= in_strategy_chance :
                        if zone in in_strategy :
                            in_strategy.remove(zone)
                        if zone in out_of_strategy :
                            out_of_strategy.remove(zone)
                else :
                    if opponent_deck[0].species in category['cards'] and random.randint(1,100) <= in_strategy_chance :
                        if zone in in_strategy :
                            in_strategy.remove(zone)
                        if zone in out_of_strategy :
                            out_of_strategy.remove(zone)

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
    corpse_eaters_index = []
    for card in range(len(hand)) :
        if hand[card].sigil == 'corpse eater' :
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
        self.bushes = {0: card.BlankCard(), 1: card.BlankCard(), 2: card.BlankCard(), 3: card.BlankCard(), 4: card.BlankCard(), 5: card.BlankCard(), 6: card.BlankCard()}
        self.player_field = {0: card.BlankCard(), 1: card.BlankCard(), 2: card.BlankCard(), 3: card.BlankCard(), 4: card.BlankCard(), 5: card.BlankCard(), 6: card.BlankCard()}
        self.opponent_field = {0: card.BlankCard(), 1: card.BlankCard(), 2: card.BlankCard(), 3: card.BlankCard(), 4: card.BlankCard(), 5: card.BlankCard(), 6: card.BlankCard()}
        self.hand = []
        self.graveyard = []
        self.score = {'player': 0, 'opponent': 0}
        self.player_deck = deck
        self.player_squirrels = squirrels
        self.opponent_deck = opponent_deck
        self.active = 'player'
        self.Leshy_play_count_median = Leshy_play_count_median
        self.Leshy_play_count_variance = Leshy_play_count_variance
        self.Leshy_in_strategy_chance = Leshy_in_strategy_chance
        self.Leshy_strat_change_threshold = Leshy_strat_change_threshold
    
    def draw(self, deck) :
        '''
        draws a card from a deck to the hand
        
        Arguments:
            deck: the deck to draw from (str) (main or resource)
        '''
        if deck == 'main' :
            self.hand.append(self.player_deck[0])
            self.player_deck.pop(0)
            # show card explanation
            self.print_field()
            self.hand[-1].explain()
            input('Press enter to continue.')
        elif deck == 'resource' :
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
        QoL.clear()
        self.print_field()
        self.hand[index].explain()
        cost = self.hand[index].saccs
        og_cost = cost
        print('Sacrifices required:', cost)
        print('Select sacrifices: (press enter to go back)', end=' ')
        sacc_list = []
        while len(sacc_list) < cost :
            sacc_index_list = input('')
            sacc_indexes = []
            for char in sacc_index_list :
                if self.player_field[int(char)].sigil == 'worthy sacrifice' :
                    cost -= 2
                sacc_indexes.append(int(char))
            if sacc_index_list == '' :
                sacc_list = []
                played = False
                break
            elif len(sacc_indexes) > cost - len(sacc_list) :
                print('Too many sacrifices.')
                cost = og_cost # to prevent goat cheesing
            else:
                sacc_list_snapshot = sacc_list.copy()
                for sacc_index in sacc_indexes :
                    if sacc_index in range(1, 6) and sacc_index not in sacc_list and self.player_field[sacc_index].species != '' :
                        sacc_list.append(sacc_index)
                    else :
                        print('Invalid zone.')
                        sacc_list = sacc_list_snapshot
                        break
            if self.player_field[zone].species != '' and zone not in sacc_list :
                print('Cannot play on top of a non sacrificed card.')
                sacc_list = []
                cost = og_cost # to prevent goat cheesing
        if len(sacc_list) != 0 or (len(sacc_list) == 0 and cost == 0):
            for ind in sacc_list :
                self.player_field[ind].sacc()
                if self.player_field[ind].sigil == 'unkillable' :
                    self.hand.append(self.player_field[ind])
                elif self.player_field[ind].sigil != 'many lives' :
                    self.graveyard.append(self.player_field[ind])
                if self.player_field[ind].sigil != 'many lives' :
                    self.player_field[ind] = card.BlankCard()
                elif self.player_field[ind].species == 'Cat' :
                    if self.player_field[ind].spent_lives >= 9 :
                        self.player_field[ind] = card_library.UndeadCat()
            self.player_field[zone] = self.hand[index]
            self.player_field[zone].play(zone=zone)
            self.hand.pop(index)
            if self.player_field[zone].sigil == 'vole hole' :
                self.hand.append(card_library.Vole())
            if self.player_field[zone].sigil == 'dam builder' :
                # play a copy to left and right if possible
                if self.player_field[zone-1].species == '' and zone != 1 :
                    self.player_field[zone-1] = card_library.Dam()
                    self.player_field[zone-1].play(zone=zone-1)
                if self.player_field[zone+1].species == '' and zone != 5 :
                    self.player_field[zone+1] = card_library.Dam()
                    self.player_field[zone+1].play(zone=zone+1)
            played = True
        QoL.clear()
        self.print_field()
        return played

    def attack(self) :
        '''
        attacks with all of the active player's cards in play and updates score
        '''
        did_shift = False
        if self.active == 'player' :
            # attacking
            for zone in self.player_field :
                if self.player_field[zone].species != '' and self.player_field[zone].zone != 0 and self.player_field[zone].zone != 6 :
                    (player_points, leshy_points) = self.player_field[zone].attack(self.opponent_field[zone-1],self.opponent_field[zone],self.opponent_field[zone+1],self.player_field[zone-1],self.player_field[zone+1], is_players=True, bushes=self.bushes)
                    self.score['player'] += player_points
                    self.score['opponent'] += leshy_points
            # post-attack sigils
            for zone in self.player_field :
                if did_shift :
                    did_shift = False
                elif self.player_field[zone].sigil == 'lane shift right' and self.player_field[zone].zone != 5 and self.player_field[zone+1].species == '' :
                    self.player_field[zone+1] = self.player_field[zone]
                    self.player_field[zone+1].zone = zone+1
                    self.player_field[zone] = card.BlankCard()
                    did_shift = True
                elif self.player_field[zone].sigil == 'lane shift left' and self.player_field[zone].zone != 2 and self.player_field[zone-1].species == '':
                    self.player_field[zone-1] = self.player_field[zone]
                    self.player_field[zone-1].zone = zone-1
                    self.player_field[zone] = card.BlankCard()
                elif self.player_field[zone].sigil == 'hefty (right)' :
                    if zone == 5 :
                        self.player_field[zone].sigil = 'hefty (left)'
                        self.player_field[zone].updateASCII()
                        break
                    push_count = hefty_check(self.player_field, zone + 1, 'right')
                    if push_count == 0:
                        self.player_field[zone].sigil = 'hefty (left)'
                        self.player_field[zone].updateASCII()
                    elif push_count >= 1 :
                        did_shift = True
                        for n in range(zone + push_count, zone - 1, -1) :
                            self.player_field[n+1] = self.player_field[n]
                            self.player_field[n+1].zone = n+1
                            self.player_field[n] = card.BlankCard()
                elif self.player_field[zone].sigil == 'hefty (left)' :
                    if zone == 1 :
                        self.player_field[zone].sigil = 'hefty (right)'
                        self.player_field[zone].updateASCII()
                        break
                    push_count = hefty_check(self.player_field, zone - 1, 'left')
                    if push_count == 0:
                        self.player_field[zone].sigil = 'hefty (right)'
                        self.player_field[zone].updateASCII()
                    elif push_count >= 1 :
                        for n in range(zone - push_count, zone + 1) :
                            self.player_field[n-1] = self.player_field[n]
                            self.player_field[n-1].zone = n-1
                            self.player_field[n] = card.BlankCard()
        elif self.active == 'opponent' :
            # attacking
            for zone in self.opponent_field :
                if self.opponent_field[zone].species != '' and self.opponent_field[zone].zone != 0 and self.opponent_field[zone].zone != 6:
                    (leshy_points, player_points) = self.opponent_field[zone].attack(self.player_field[zone-1],self.player_field[zone],self.player_field[zone+1],self.opponent_field[zone-1],self.opponent_field[zone+1])
                    if leshy_points < self.opponent_field[zone].current_attack and self.player_field[zone].sigil == 'bees within' :
                        self.hand.append(card_library.Bee())
                    self.score['player'] += player_points
                    self.score['opponent'] += leshy_points
            # post-attack sigils
            for zone in self.opponent_field :
                if did_shift :
                    did_shift = False
                elif self.opponent_field[zone].sigil == 'lane shift right' and self.opponent_field[zone].zone != 5 and self.opponent_field[zone+1].species == '':
                    self.opponent_field[zone+1] = self.opponent_field[zone]
                    self.opponent_field[zone+1].zone = zone+1
                    self.opponent_field[zone] = card.BlankCard()
                    did_shift = True
                elif self.opponent_field[zone].sigil == 'lane shift left' and self.opponent_field[zone].zone != 1 and self.opponent_field[zone-1].species == '':
                    self.opponent_field[zone-1] = self.opponent_field[zone]
                    self.opponent_field[zone-1].zone = zone-1
                    self.opponent_field[zone] = card.BlankCard()
                elif self.opponent_field[zone].sigil == 'hefty (right)' :
                    if zone == 5 :
                        self.opponent_field[zone].sigil = 'hefty (left)'
                        self.opponent_field[zone].updateASCII()
                        break
                    push_count = hefty_check(self.opponent_field, zone + 1, 'right')
                    if push_count == 0 :
                        self.opponent_field[zone].sigil = 'hefty (left)'
                    elif push_count >= 1 :
                        did_shift = True
                        for n in range(zone + push_count, zone - 1, -1) :
                            self.opponent_field[n+1] = self.opponent_field[n]
                            self.opponent_field[n+1].zone = n+1
                            self.opponent_field[n] = card.BlankCard()
                elif self.opponent_field[zone].sigil == 'hefty (left)' :
                    if zone == 1 :
                        self.opponent_field[zone].sigil = 'hefty (right)'
                        self.opponent_field[zone].updateASCII()
                        break
                    push_count = hefty_check(self.opponent_field, zone - 1, 'left')
                    if push_count == 0 :
                        self.opponent_field[zone].sigil = 'hefty (right)'
                    elif push_count >= 1 :
                        for n in range(zone - push_count, zone + 1) :
                            self.opponent_field[n-1] = self.opponent_field[n]
                            self.opponent_field[n-1].zone = n-1
                            self.opponent_field[n] = card.BlankCard()

    def check_states(self) :
        '''
        checks for dead cards and removes them, plus returns unkillables if player's turn. Also summons corpse eaters if necessary.
        '''
        # setup for corpse eaters
        corpses = []
        open_corpses = []

        # check for dead cards in player field
        for zone in self.player_field :

            # if a normal card dies
            if self.player_field[zone].status == 'dead' and self.player_field[zone].sigil != 'unkillable' and self.player_field[zone].sigil != 'split':
                self.player_field[zone].die()
                self.graveyard.append(self.player_field[zone])
                self.player_field[zone] = card.BlankCard()
                corpses.append(zone)

            # if an unkillable card dies
            elif self.player_field[zone].status == 'dead' and self.player_field[zone].sigil == 'unkillable' :
                self.player_field[zone].die()
                self.player_field[zone].status = 'alive'
                self.hand.append(self.player_field[zone])
                self.player_field[zone] = card.BlankCard()

            # if a split card dies
            elif self.player_field[zone].status == 'dead' and self.player_field[zone].sigil == 'split' :
                split_card = copy.deepcopy(self.player_field[zone])

                # play a copy to left and right if possible
                if self.player_field[zone-1].species == '' and zone != 1 :
                    self.player_field[zone-1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone - 1, blank_cost=True)
                if self.player_field[zone+1].species == '' and zone != 5 :
                    self.player_field[zone+1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone + 1, blank_cost=True)

                # removes the original card
                self.player_field[zone].die()
                self.graveyard.append(self.player_field[zone])
                self.player_field[zone] = card.BlankCard()
                corpses.append(zone)

        for zone in self.opponent_field :
            # if a normal card dies
            if self.opponent_field[zone].status == 'dead' and self.opponent_field[zone].sigil != 'unkillable' and self.opponent_field[zone].sigil != 'split':
                self.opponent_field[zone].die()
                self.opponent_field[zone] = card.BlankCard()
            # if a split card dies
            elif self.opponent_field[zone].status == 'dead' and self.opponent_field[zone].sigil == 'split' :
                split_card = copy.deepcopy(self.opponent_field[zone])

                # play a copy to left and right if possible
                if self.opponent_field[zone-1].species == '' and zone != 1 :
                    self.opponent_field[zone-1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone - 1, blank_cost=True)
                if self.opponent_field[zone+1].species == '' and zone != 5 :
                    self.opponent_field[zone+1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone + 1, blank_cost=True)

                # removes the original card
                self.opponent_field[zone].die()
                self.opponent_field[zone] = card.BlankCard()

        for zone in self.bushes :
            # if a normal card dies
            if self.bushes[zone].status == 'dead' and self.bushes[zone].sigil != 'unkillable' and self.bushes[zone].sigil != 'split':
                self.bushes[zone].die()
                self.bushes[zone] = card.BlankCard()
            
            # if a split card dies
            elif self.bushes[zone].status == 'dead' and self.bushes[zone].sigil == 'split' :
                split_card = copy.deepcopy(self.bushes[zone])

                # play a copy to left and right if possible
                if self.bushes[zone-1].species == '' and zone != 1 :
                    self.bushes[zone-1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone - 1, blank_cost=True)
                if self.bushes[zone+1].species == '' and zone != 5 :
                    self.bushes[zone+1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone + 1, blank_cost=True)

                # removes the original card
                self.bushes[zone].die()
                self.bushes[zone] = card.BlankCard()

        # check for corpse eaters
        for zone in corpses :
            if self.player_field[zone].species == '' :
                open_corpses.append(zone)
        corpse_eaters = get_corpse_eaters(self.hand)
        exhausted = False
        while not exhausted :
            if open_corpses != [] and corpse_eaters != []:
                zone_choice = random.choice(open_corpses)
                self.player_field[zone_choice] = self.hand[corpse_eaters[0]]
                self.player_field[zone_choice].play(zone=zone_choice)
                self.hand.pop(corpse_eaters[0])
                open_corpses.remove(zone_choice)
                corpse_eaters = get_corpse_eaters(self.hand) # refresh corpse eaters as hand indexes may have changed
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
        
        played = 0
        while played < play_count :
            
            # intelligent choosing of zones to prioritize
            in_strategy, out_of_strategy = ai_category_checking(card_library.AI_categories, self.player_field, self.opponent_deck, self.bushes, self.score, strat_change_threshold, in_strategy_chance)

            # ensure that the loop will not run if there are no zones to play to, preventing infinite loop
            if len(in_strategy) + len(out_of_strategy) == 0 :
                break

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
                    deck_string += card.TextByLine() + ' '*card_gaps
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
                    graveyard_string += card.TextByLine() + ' '*card_gaps
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
                    hand_string += card.TextByLine() + ' '*card_gaps
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
                    field_string += card.TextByLine() + ' '*card_gaps*3
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

def test_advancing() :
        QoL.clear()

        # create decks
        leshy_deck = deck.Deck([card_library.Asp(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF()])
        player_deck = deck.Deck([card_library.DumpyTF(), card_library.Lobster(), card_library.BoppitW(), card_library.Ouroboros(), card_library.Turtle(), card_library.Asp(), card_library.Falcon(), card_library.DumpyTF(), card_library.Turtle(), card_library.BoppitW()])
        squirrels = [card_library.Squirrel()]
        for n in range(19) :
            squirrels.append(card_library.Squirrel())
        player_squirrels = deck.Deck(squirrels)

        # Create a sample playmat with cards on the field
        playmat = Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
        card_list = []
        for cost in card_library.Poss_Playr :
            for species in card_library.Poss_Playr[cost] :
                card_list.append(species)
                card_list.append(card.BlankCard())
        for zone in range(1, 6) :
            playmat.player_field[zone] = copy.deepcopy(random.choice(card_list))

        # Print the initial field
        # print("Initial Field:")
        # playmat.print_full_field()

        # # Get user input before advancing
        # input("Press enter to advance.")

        # Call the advance method
        playmat.advance()

        # Print the field after advancing
        # print("Field after Advancing:")
        playmat.print_field()

def test_split_dam() :
    QoL.clear()

    # create decks
    leshy_deck = deck.Deck([card_library.Asp(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF()])
    player_deck = deck.Deck([card_library.DumpyTF(), card_library.Lobster(), card_library.BoppitW(), card_library.Ouroboros(), card_library.Turtle(), card_library.Asp(), card_library.Falcon(), card_library.DumpyTF(), card_library.Turtle(), card_library.BoppitW()])
    squirrels = [card_library.Squirrel()]
    for n in range(19) :
        squirrels.append(card_library.Squirrel())
    player_squirrels = deck.Deck(squirrels)

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
    leshy_deck = deck.Deck([card_library.Asp(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF()])
    player_deck = deck.Deck([card_library.DumpyTF(), card_library.Lobster(), card_library.BoppitW(), card_library.Ouroboros(), card_library.Turtle(), card_library.Asp(), card_library.Falcon(), card_library.DumpyTF(), card_library.Turtle(), card_library.BoppitW()])
    squirrels = [card_library.Squirrel()]
    for n in range(19) :
        squirrels.append(card_library.Squirrel())
    player_squirrels = deck.Deck(squirrels)

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
            playmat.hand.append(card.BlankCard(name='Corpse Eater', cost=1, attack=1, life=1, sigil='corpse eater', status='alive', blank_cost=True))
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

if __name__ == '__main__' :
    # test_advancing()
    # test_split_dam()
    test_corpse_eaters()

    pass