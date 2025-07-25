from __future__ import annotations # prevent type hints needing import at runtime
from dataclasses import field
from typing import TYPE_CHECKING
if TYPE_CHECKING :
    from typing import Any, Callable

import card
import card_library
import QoL
import ASCII_text
import copy
import random
import os
import duel
import sigils
import time

def smart_category_checking(categories: list[dict[str, Any]], player_field: dict[int, card.BlankCard], card_to_play: card.BlankCard, bushes: dict[int, card.BlankCard], score: dict[str, int], strat_change_threshold: int)  -> tuple[list[int], list[int]]:
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
    def is_in_strat(card_to_play: card.BlankCard, opp_card: card.BlankCard, sigil_slot: int)  -> bool:
        if sigil_slot not in range(0,2) : raise ValueError

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
        if type(opp_card) != card.BlankCard and (self_life > opp_attack or self_attack >= opp_life or opp_attack >= 4) :
            return True
        
        return False
    
    def is_out_strat(card_to_play: card.BlankCard, opp_card: card.BlankCard, sigil_slot: int) -> bool :
        if sigil_slot not in range(0,2) : raise ValueError

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
    
    def add_to_in_strat(card_to_play: card.BlankCard, player_field: dict[int, card.BlankCard], bushes: dict[int, card.BlankCard], zone: int) -> bool :
        # error handling
        if zone not in range(1, 5) :
            raise ValueError('Invalid zone.')
        
        # set up variables
        opp_card = player_field[zone]
        bush_empty = bushes[zone].species == ''

        # if Leshy is winning enough to go on the offensive, regardless of card category
        if (score['opponent'] - score['player'] >= strat_change_threshold) and (card_to_play.base_attack > 0) :
            if bush_empty and type(opp_card) == card.BlankCard :
                return True
            else :
                return False
        
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
    out_of_strategy = [zone for zone in range(1, 5) if zone not in in_strategy and type(bushes[zone]) == card.BlankCard]

    return in_strategy, out_of_strategy

def get_corpse_eaters(hand: list[card.BlankCard]) -> list[int] :
    '''
    gets the indexes of all corpse eaters in the hand

    Arguments:
        hand: the player's hand (list)

    Returns:
        corpse_eaters: the corpse eaters in the hand (list)
    '''
    corpse_eaters: list[int] = []
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
    def __init__(self, deck: list[card.BlankCard], squirrels: list[card.BlankCard], opponent_deck: list[card.BlankCard], Leshy_play_count_median: int, Leshy_play_count_variance: int, Leshy_in_strategy_chance: int, Leshy_strat_change_threshold: int) :
        # basic variables
        self.hand: list[card.BlankCard] = []
        self.graveyard: list[card.BlankCard] = []
        self.score: dict[str, int] = {'player': 0, 'opponent': 0}
        self.active: str = 'player'
        self.player_deck: list[card.BlankCard] = deck
        self.player_squirrels: list[card.BlankCard] = squirrels
        self.opponent_deck: list[card.BlankCard] = opponent_deck
        self.Leshy_play_count_median: int = Leshy_play_count_median
        self.Leshy_play_count_variance: int = Leshy_play_count_variance
        self.Leshy_in_strategy_chance: int = Leshy_in_strategy_chance
        self.Leshy_strat_change_threshold: int = Leshy_strat_change_threshold

        # create the rows of the field
        gen_blank_row: Callable[[], dict[int, card.BlankCard]] = lambda: {column: card.BlankCard() for column in range(6)}
        self.bushes: dict[int, card.BlankCard] = gen_blank_row()
        self.player_field: dict[int, card.BlankCard] = gen_blank_row()
        self.opponent_field: dict[int, card.BlankCard] = gen_blank_row()
        for zone in range(1, 5) :
            for field in [self.player_field, self.bushes, self.opponent_field] :
                field[zone].play(zone=zone)
    
    def draw(self, deck: str) -> None :
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

            case 'resource' :
                if self.player_squirrels == [] :
                    raise ValueError('Deck is empty.')
                self.hand.append(self.player_squirrels[0])
                self.player_squirrels.pop(0)
            
            case _ : raise ValueError
        
        # show card explanation
        self.print_field()
        self.hand[-1].explain()
        input('Press enter to continue.')

    def play_card(self, index: int, zone: int) -> bool :
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

        if cost == 0 and type(self.player_field[zone]) != card.BlankCard : # playing on top of a card
            return False
        else :
            print('Sacrifices required:', cost)
            print('Select sacrifices: (press enter to go back)', end=' ')

        def fail_saccs() -> tuple[list[int], int, bool]:
                sacc_list = []
                cost = og_cost # to prevent goat cheesing
                worthy_sacc = False
                return sacc_list, cost, worthy_sacc

        # get sacrifices
        worthy_sacc = False
        while not (len(sacc_list) >= cost) :
            sacc_index_list = input('')

            if sacc_index_list == '' : # go back if user presses enter
                return False
            
            sacc_indexes = [int(sacc) for sacc in sacc_index_list if sacc in [str(n) for n in range(1, 5)]] # get valid saccs

            for _ in [sacc for sacc in sacc_indexes if self.player_field[sacc].has_sigil('worthy sacrifice')] : # decrease cost for cards with worthy sacrifice
                worthy_sacc = True
                cost -= 2 
                if cost < 0 :
                    cost = 0

            if len(sacc_indexes) > cost - len(sacc_list) and not worthy_sacc : # too many saccs, serves as guard clause
                print('Too many sacrifices.')
                sacc_list, cost, worthy_sacc = fail_saccs() # reset saccs and cost to prevent player confusion, may change if alternate behavior is desired
                continue

            for sacc_index in sacc_indexes :
                if sacc_index not in range(1, 5) or sacc_index in sacc_list or type(self.player_field[sacc_index]) == card.BlankCard : # invalid zone
                    print(str(sacc_index), 'is an invalid zone.')
                    break # do not reset, just don't add the sacc, may change if alternate behavior is desired
                elif type(self.player_field[sacc_index]) in card_library.Terrain_Cards : # cannot sacrifice terrain cards
                    print('Cannot sacrifice terrain cards.')
                    break # do not reset, just don't add the sacc, may change if alternate behavior is desired
                else :
                    sacc_list.append(sacc_index)

            if type(self.player_field[zone]) == card.BlankCard or len(sacc_list) != cost : # guard clause for playing on top of a card
                continue
            if zone not in sacc_list : # playing on top of a card that wasn't sacrificed
                print('Cannot play on top of a non sacrificed card.')
                sacc_list, cost, worthy_sacc = fail_saccs()
            elif self.player_field[zone].has_sigil('many lives') : # playing on top of a card with many lives
                print('Cannot play on top of a card with many lives.')
                sacc_list, cost, worthy_sacc = fail_saccs()
        
        # remove saccs
        for ind in sacc_list :
            QoL.exec_sigil_code(self.player_field[ind], sigils.on_sacrifices, None, locals())

            if type(self.player_field[ind]) == card_library.Cat and self.player_field[ind].has_sigil('many lives') : # make sure cat still has many lives
                self.player_field[ind].spent_lives += 1 # type: ignore
                if self.player_field[ind].spent_lives >= 9 : # type: ignore
                    self.player_field[ind] = card_library.UndeadCat()

            if not self.player_field[ind].sigil_in_category(sigils.on_sacrifices) :
                self.player_field[ind].die()
                self.graveyard.insert(0, self.player_field[ind])
                self.player_field[ind] = card.BlankCard()
        else : 
            # play card to zone
            self.summon_card(card=self.hand[index], field=self.player_field, zone=zone)
            self.hand.pop(index)
            
            # handle sigils
            QoL.exec_sigil_code(self.player_field[zone], sigils.on_plays, None, locals())

            self.print_field()
            return True
    
    def attack(self) -> None :
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
                omni_strike = False
            case 'opponent' :
                attacking_field = self.opponent_field
                defending_field = self.player_field
                is_players = False
                omni_strike = any([type(card_) == card_library.Moon for card_ in self.opponent_field.values()]) and all([type(card_) == card.BlankCard for card_ in self.player_field.values()])
            case _ :
                raise ValueError('Invalid active player.')

        # attacking
        for zone in attacking_field :
            if type(attacking_field[zone]) != card.BlankCard and attacking_field[zone].zone != 0 and attacking_field[zone].zone != 5 :
                attacker_points = attacking_field[zone].attack(defending_field[zone-1],defending_field[zone],defending_field[zone+1], self.hand, is_players=is_players, bushes=self.bushes)

                # score update
                self.score[self.active] += attacker_points
        
        # for omni strike sigil (only on the moon)
        if omni_strike : self.score['opponent'] += 1

        # moving sigils
        shifted_card = None
        for zone in attacking_field :
            zone_card = attacking_field[zone]
            if shifted_card == zone_card :
                did_shift = False
            else :
                [did_shift] = QoL.exec_sigil_code(attacking_field[zone], sigils.movers, None, locals(), ['did_shift'])
            if did_shift :
                shifted_card = zone_card

    def check_states(self) -> None :
        '''
        checks for dead cards and removes them, plus returns unkillables if player's turn. Also summons corpse eaters if necessary.
        '''
        # set up variables
        corpses = []

        # check for dead cards
        for current_field, zone in [(current_field, zone) for current_field in [self.player_field, self.opponent_field, self.bushes] for zone in range(1, 5)] :
            # if a sigil applies
            [corpses] = QoL.exec_sigil_code(current_field[zone], sigils.on_deaths, None, locals(), ['corpses'])

            ## specific cards will never have sigils that apply on death
            # if pack mule from Prospector fight
            if current_field[zone].species == 'Pack Mule' and current_field[zone].status == 'dead' and current_field in [self.opponent_field, self.bushes] : # keeping this as species because its a funny easter egg
                self.hand.append(card_library.Squirrel())
                one_cost = QoL.random_card(card_library.Poss_Playr[1])
                two_cost = QoL.random_card(card_library.Poss_Playr[2])
                bone_card = QoL.random_card(card_library.Poss_Playr[1]) # until bones are implemented
                self.hand.append(one_cost)
                self.hand.append(two_cost)
                self.hand.append(bone_card)
                current_field[zone].die()
                self.summon_card(card=card.BlankCard(), field=current_field, zone=zone)
                corpses.append((zone, current_field))

            # if bait bucket from Angler fight
            elif type(current_field[zone]) == card_library.BaitBucket and current_field[zone].status == 'dead' :
                current_field[zone].die()
                if current_field == self.player_field : self.graveyard.insert(0, current_field[zone])
                self.summon_card(card=card_library.BullShark(True), field=current_field, zone=zone)

            # if strange frog from Trapper fight
            elif type(current_field[zone]) == card_library.StrangeFrog and current_field[zone].status == 'dead' and current_field == self.opponent_field :
                current_field[zone].die()
                if current_field == self.player_field : self.graveyard.insert(0, current_field[zone])
                self.summon_card(card=card_library.LeapingTrap(True), field=current_field, zone=zone)

            # if moon from Leshy fight
            elif type(current_field[zone]) == card_library.Moon and current_field[zone].status == 'dead' :
                for zone in range(1, 5) :
                    self.bushes[zone].die()
                    self.opponent_field[zone].die()
                    self.summon_card(card=card.BlankCard(), field=self.bushes, zone=zone)
                    self.summon_card(card=card.BlankCard(), field=self.opponent_field, zone=zone)
                QoL.clear()
                print('\n'*5)
                print(QoL.center_justified('"You really destroyed the moon..."'))
                time.sleep(3)
                print(QoL.center_justified('"I suppose all that\'s left is to finish me off."'))
                time.sleep(2)
                print(QoL.center_justified('"..."'))
                time.sleep(2)
                print(QoL.center_justified('"Go on."'))
                time.sleep(3)
                print('\n'*2)
                input(QoL.center_justified('Press enter to continue...').rstrip() + ' ')

            # if a normal card dies
            # elif current_field[zone].status == 'dead' and not current_field[zone].sigil_in_category(sigils.on_deaths) :
            elif current_field[zone].status == 'dead' :
                current_field[zone].die()
                if type(self) != card.BlankCard and current_field == self.player_field : self.graveyard.insert(0, current_field[zone])
                self.summon_card(card=card.BlankCard(), field=current_field, zone=zone)
                corpses.append((zone, current_field))
        
        # check for corpse eaters
        open_corpses = [corpse for (corpse, field) in corpses if field == self.player_field and type(self.player_field[corpse]) == card.BlankCard]
        corpse_eaters = get_corpse_eaters(self.hand)

        # play corpse eaters
        while open_corpses and corpse_eaters :
            zone_choice = random.choice(open_corpses)
            self.summon_card(card=self.hand[corpse_eaters[0]], field=self.player_field, zone=zone_choice)
            self.hand.pop(corpse_eaters[0])
            open_corpses.remove(zone_choice)
            corpse_eaters = get_corpse_eaters(self.hand) # update corpse eaters

    def advance(self) -> None : 
        '''
        advances cards from bushes to field, utilizing opponent intelligence to play cards
        '''
        # set up variables
        played = 0
        player_card_count = len([card_in_play for card_in_play in self.player_field.values() if type(card_in_play) != card.BlankCard])
        play_count_median = self.Leshy_play_count_median + (player_card_count > 2) - (player_card_count < 2) # shift range slightly to match amount of cards on player's field
        play_count = random.randint(play_count_median - self.Leshy_play_count_variance, play_count_median + self.Leshy_play_count_variance)
        play_count = max(min(play_count, len(self.opponent_deck), 4), 1) if self.opponent_deck else 0 # clamp play count

        # advance from bushes to field
        for zone in [zone for zone in self.opponent_field if type(self.opponent_field[zone]) == card.BlankCard and zone % 5 != 0] :
            self.summon_card(card=self.bushes[zone], field=self.opponent_field, zone=zone)
            self.summon_card(card=card.BlankCard(), field=self.bushes, zone=zone)
        
        while played < play_count and [zone for zone in range(1, 5) if type(self.bushes[zone]) == card.BlankCard] :
            # intelligent choosing of zones to prioritize
            in_strategy, out_of_strategy = smart_category_checking(card_library.strat_categories, self.player_field, self.opponent_deck[0], self.bushes, self.score, self.Leshy_strat_change_threshold)

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

    def switch(self) -> None :
        '''
        switches the active player
        '''
        if self.active == 'player' :
            self.active = 'opponent'
        elif self.active == 'opponent' :
            self.active = 'player'
        else :
            raise ValueError('Invalid active player.')

    def check_win(self) -> tuple[bool, str, int, bool] :
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

    def print_remaining(self) -> None :
        '''
        prints the remaining cards in the deck (sorted) and the squirrels (sorted) (clears screen first)
        '''
        # set up variables
        term_cols = os.get_terminal_size().columns
        max_width = term_cols*80 // 100
        indent = min((term_cols - max_width) // 2, 4)
        cards_per_row = min(max_width // 15, 8)
        card_gaps = max_width // cards_per_row - 15
        card_gaps_space = ' '*(card_gaps + indent)

        # print remaining cards in deck
        QoL.clear()
        print(card_gaps_space + 'Remaining cards in deck:')
        QoL.print_deck(self.player_deck, sort=True, numbered=True)
        print('\n')
        print(card_gaps_space + 'Remaining squirrels: ' + str(len(self.player_squirrels)) + '\n')

    def print_graveyard(self) -> None :
        '''
        prints the cards in the graveyard (in order) (clears screen first)
        '''
        # set up variables
        term_cols = os.get_terminal_size().columns
        max_width = term_cols*80 // 100
        indent = min((term_cols - max_width) // 2, 4)
        cards_per_row = min(max_width // 15, 8)
        card_gaps = max_width // cards_per_row - 15
        card_gaps_space = ' '*(card_gaps + indent)

        # print graveyard
        QoL.clear()
        print(card_gaps_space + 'Graveyard:')
        QoL.print_deck(self.graveyard, sort=False, numbered=True)
    
    def print_hand(self) -> None : 
        '''
        prints the cards in the player's hand (does NOT clear screen first)
        '''
        # set up variables
        term_cols = os.get_terminal_size().columns
        max_width = term_cols*80 // 100
        indent = min((term_cols - max_width) // 2, 4)
        cards_per_row = min(max_width // 15, min(8, len(self.hand)))
        card_gaps = max_width // cards_per_row - 15
        card_gaps_space = ' '*(card_gaps + indent)

        # print hand
        print(card_gaps_space + 'Hand:', end='')
        QoL.print_deck(self.hand, sort=False)

    def print_field(self, score_scale: bool=True) -> None :
        '''
        prints the field and score scales (clears screen first)

        Arguments:
            score_scale: whether to print the score scales, defaults to True (bool)
        '''
        def get_connector(gaps: int, row: int, line: int, moon_lines: str) -> list[str] :
            '''
            gets the connectors for the given row and line

            Arguments:
                gaps: the number of spaces to print between each card
                row: the row of cards
                line: the line number
                moon_lines: the lines to print for the moon's ASCII
            
            Returns:
                connector: the list of strings to print as the connector
            '''
            match line :
                case 0 if row == 2 : connector = [' '*gaps*3] + ['-'*gaps*3]*3
                case _ if row == 2 and line in range(1, 11) : connector = ASCII_text.split_moon_lines(moon_lines)['connectors'][line - 1]
                case _ if row == 1 and line in range(10) : connector = ASCII_text.split_moon_lines(moon_lines)['connectors'][line + 10]
                case 10 if row == 1 : connector = [' '*gaps*3] + ['-'*gaps*3]*3
                case _ : connector = [' '*gaps*3]*4

            return connector
    
        # set up variables
        field_string = ''
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols - 60) // (7*3)
        if card_gaps <= 0 :
            score_gap = 31
        else :
            score_gap = card_gaps*6 + 31
        vis_bushes = [self.bushes[n] for n in range(1, 5)]
        vis_opponent_field = [self.opponent_field[n] for n in range(1, 5)]
        vis_player_field = [self.player_field[n] for n in range(1, 5)]
        cards = [vis_player_field, vis_opponent_field, vis_bushes]
        moon_on_field = any([type(card_) == card_library.Moon for card_ in vis_bushes + vis_opponent_field])

        # generate field string
        for row in [2, 1, 0] :
            for line in range(11) :
                if moon_on_field and row in [1, 2] : connector = get_connector(card_gaps, row, line, ASCII_text.moon_inner_str())
                else : connector = [' '*card_gaps*3]*4
                connector[0] = ''
                for i in range(4) : field_string += connector[i] + cards[row][i].text_by_line()
                field_string += '\n'

            # field_string += ' '*card_gaps + '-'*(card_gaps*13 + 60) + '\n' if row == 1 else '' # add a divider between opponent and player fields
            field_string += '-'*(card_gaps*13 + 60) + '\n' if row == 1 else '' # add a divider between opponent and player fields

        # print field
        QoL.clear()
        # print(field_string, end='')
        print(QoL.center_justified(field_string),end='')
        if score_scale : ASCII_text.print_scales(self.score, score_gap)

    def print_full_field(self) -> None :
        '''
        prints the field and player's hand (clears screen first)
        '''
        self.print_field()
        self.print_hand()

    def summon_card(self, card: card.BlankCard, field: dict[int, card.BlankCard], zone: int) -> None :
        '''
        summons a card to the field

        Arguments:
            card: the card to summon (card)
            field: the field to summon to (dict)
            zone: the zone to summon to (int)
        '''
        field[zone] = card
        field[zone].play(zone=zone)