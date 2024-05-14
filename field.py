import card
import card_library
import deck
import QoL
import ASCII_text
import itertools312
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

class Playmat :
    '''
    The field of play, including the bushes, the cards in play, the player's hand, and the score.

    Arguments:
        deck: the player's main deck (list)
        squirrels: the player's resource deck (list)
        opponent_deck: Leshy's deck (list)
    
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
    def __init__(self, deck, squirrels, opponent_deck) :
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
            for zone in self.player_field :
                if self.player_field[zone].species != '' and self.player_field[zone].zone != 0 and self.player_field[zone].zone != 6 :
                    (player_points, leshy_points) = self.player_field[zone].attack(self.opponent_field[zone-1],self.opponent_field[zone],self.opponent_field[zone+1],self.player_field[zone-1],self.player_field[zone+1])
                    self.score['player'] += player_points
                    self.score['opponent'] += leshy_points
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
            for zone in self.opponent_field :
                if self.opponent_field[zone].species != '' and self.opponent_field[zone].zone != 0 and self.opponent_field[zone].zone != 6:
                    (leshy_points, player_points) = self.opponent_field[zone].attack(self.player_field[zone-1],self.player_field[zone],self.player_field[zone+1],self.opponent_field[zone-1],self.opponent_field[zone+1])
                    if leshy_points < self.opponent_field[zone].current_attack and self.player_field[zone].sigil == 'bees within' :
                        self.hand.append(card_library.Bee())
                    self.score['player'] += player_points
                    self.score['opponent'] += leshy_points
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
        checks for dead cards and removes them, plus returns unkillables if player's turn
        '''
        for zone in self.player_field :
            if self.player_field[zone].status == 'dead' and self.player_field[zone].sigil != 'unkillable' and self.player_field[zone].sigil != 'split':
                self.player_field[zone].die(self.player_field[zone-1], self.player_field[zone+1], self.player_field)
                self.graveyard.append(self.player_field[zone])
                self.player_field[zone] = card.BlankCard()
            elif self.player_field[zone].status == 'dead' and self.player_field[zone].sigil == 'unkillable' :
                self.player_field[zone].die(self.player_field[zone-1], self.player_field[zone+1], self.player_field)
                self.player_field[zone].status = 'alive'
                self.hand.append(self.player_field[zone])
                self.player_field[zone] = card.BlankCard()
            elif self.player_field[zone].status == 'dead' and self.player_field[zone].sigil == 'split' :
                split_card = copy.deepcopy(self.player_field[zone])
                if self.player_field[zone-1].species == '' and zone != 1 :
                    self.player_field[zone-1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone - 1)
                    self.player_field[zone] = card.BlankCard()
                if self.player_field[zone+1].species == '' and zone != 5 :
                    self.player_field[zone+1] = card.BlankCard(name=split_card.species,cost=split_card.saccs,attack=split_card.base_attack//2,life=split_card.base_life//2,sigil='',status='alive',zone=zone + 1)
                    self.player_field[zone] = card.BlankCard()
        for zone in self.opponent_field :
            if self.opponent_field[zone].status == 'dead' :
                self.opponent_field[zone].die(self.opponent_field[zone-1], self.opponent_field[zone+1], self.opponent_field)
                self.graveyard.append(self.opponent_field[zone])
                self.opponent_field[zone] = card.BlankCard()

    def advance(self) :
        '''
        advances cards from bushes to field
        '''
        bush_count = 0
        for zone in self.opponent_field :
            if self.opponent_field[zone].species == '' and zone != 0 and zone != 6 :
                if self.bushes[zone].species != '' :
                    bush_count -= 1 # decrement bush_count because the card is advancing
                self.opponent_field[zone] = self.bushes[zone]
                self.opponent_field[zone].play(zone=zone)
                if random.randrange(1,11) > 4 or bush_count >= 3:
                    self.bushes[zone] = card.BlankCard()
                else :
                    self.bushes[zone] = self.opponent_deck[0]
                    self.opponent_deck.pop(0)
                    bush_count += 1

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
        (term_cols, term_rows) = os.get_terminal_size()
        card_gaps = (term_cols*55 // 100) // 5 - 15
        sorted_main_deck = sorted(self.player_deck, key=lambda x: x.name)
        sorted_main_deck = sorted(sorted_main_deck, key=lambda x: x.cost)
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8 
        chunked = list(itertools312.batched(sorted_main_deck, cards_per_row))  
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
        (term_cols, term_rows) = os.get_terminal_size()
        card_gaps = (term_cols*55 // 100) // 5 - 15
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8 
        chunked = list(itertools312.batched(self.graveyard, cards_per_row))  
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
    
    def print_hand(self) : # unsorted for the time being
        '''
        prints the cards in the player's hand (does NOT clear screen first)
        '''
        (term_cols, term_rows) = os.get_terminal_size()
        card_gaps = (term_cols*55 // 100) // 5 - 15
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8 
        chunked = list(itertools312.batched(self.hand, cards_per_row)) 
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
        (term_cols, term_rows) = os.get_terminal_size()
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

if __name__ == '__main__' :
    (term_cols, term_rows) = os.get_terminal_size()
    card_gaps = (term_cols*55 // 100) // 5 - 15
    QoL.clear()
    leshy_deck = deck.Deck([card_library.Asp(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.OppositeRabbit(), card_library.Falcon(), card_library.DumpyTF()])
    player_deck = deck.Deck([card_library.DumpyTF(), card_library.Lobster(), card_library.BoppitW(), card_library.Ouroboros(), card_library.Turtle(), card_library.Asp(), card_library.Falcon(), card_library.DumpyTF(), card_library.Turtle(), card_library.BoppitW()])
    squirrels = [card_library.Squirrel()]
    for n in range(19) :
        squirrels.append(card_library.Squirrel())
    player_squirrels = deck.Deck(squirrels)
    testmat = Playmat(deck=player_deck.shuffle(), squirrels=player_squirrels.shuffle(), opponent_deck=leshy_deck.shuffle())
    testmat.player_field[1] = card_library.Rabbit()
    testmat.player_field[2] = card_library.Falcon()
    testmat.player_field[3] = card_library.DumpyTF()
    testmat.player_field[4] = card_library.Rabbit()
    testmat.player_field[1].play(zone=1)
    testmat.player_field[2].play(zone=2)
    testmat.player_field[3].play(zone=3)
    testmat.player_field[4].play(zone=4)
    testmat.draw('resource')
    testmat.draw('main')
    testmat.draw('resource')
    testmat.draw('resource')
    testmat.draw('main')
    bad_input = True
    second_bad_input = False
    invalid_index = False
    while bad_input :
        testmat.print_full_field()
        if invalid_index :
            print('Invalid index.')
            invalid_index = False
        play_index = input('Card to play: ')
        if play_index == 'quit' : # for testing purposes
            exit()
        # if play_index == '' : # commented for testing purposes
        #     break
        try :
            play_index = int(play_index) - 1
        except :
            play_index = len(testmat.hand) + 1
        if play_index in range(len(testmat.hand)) :
            bad_input = False
            QoL.clear()
            testmat.print_field()
            print(' '*card_gaps + 'Card to play: ')
            testmat.hand[play_index].explain()
            second_bad_input = True
        else :
            invalid_index = True
        while second_bad_input and not bad_input:
            zone_to_play = input('Zone to play: (press enter to go back) ')
            if zone_to_play == 'quit' : # for testing purposes
                exit()
            if zone_to_play == '' :
                bad_input = True
                break
            try :
                zone_to_play = int(zone_to_play)
            except :
                zone_to_play = 0
            if zone_to_play in range(1, 6) :
                second_bad_input = False
                if not testmat.play_card(play_index, zone_to_play) :
                    bad_input = True
                    second_bad_input = False
            else :
                print('Invalid zone.')
    input('Press enter to continue.')
    testmat.print_remaining()
    input('Press enter to continue.')
    testmat.print_graveyard()
    input('Press enter to continue.')
    testmat.print_full_field()
    input('Press enter to continue. (attack)')
    testmat.attack()
    testmat.check_states()
    testmat.print_full_field()
    input('Press enter to continue. (advance)')
    testmat.advance()
    testmat.print_full_field()