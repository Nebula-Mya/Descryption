import card
import card_library
import deck
import sigils
import os
import ASCII_text
import itertools312

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
        attack() : attacks with all of the active player's cards in play and updates score (unimplemented)
        check_states() : checks for dead cards and removes them, plus returns unkillables if player's turn
        advance() : advances cards from bushes to field (unimplemented)
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
        self.hand = [card_library.squirrel()]
        self.graveyard = []
        self.score = {'player': 0, 'opponent': 0}
        self.player_deck = deck
        self.player_squirrels = squirrels
        self.opponent_deck = opponent_deck
        self.active = 'opponent'
    
    def draw(self, deck) :
        '''
        draws a card from a deck to the hand
        
        Arguments:
            deck: the deck to draw from (str) (main or resource)
        '''
        if deck == 'main' :
            self.hand.append(self.player_deck[0])
            self.player_deck.pop(0)     
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
        os.system('clear')
        self.print_field()
        self.hand[index].explain()
        cost = self.hand[index].saccs
        print('Sacrifices required:', cost)
        print('Select sacrifices: (press enter to go back)', end=' ')
        sacc_list = []
        while len(sacc_list) < cost :
            sacc_index_list = input('')
            sacc_indexes = []
            for char in sacc_index_list :
                sacc_indexes.append(int(char))
            if sacc_index_list == '' :
                sacc_list = []
                played = False
                break
            elif len(sacc_indexes) > cost - len(sacc_list) :
                print('Too many sacrifices.')
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
        if len(sacc_list) != 0 or (len(sacc_list) == 0 and cost == 0):
            for ind in sacc_list :
                self.player_field[ind].sacc()
                if self.player_field[ind].sigil == 'unkillable' :
                    self.hand.append(self.player_field[ind])
                else :
                    self.graveyard.append(self.player_field[ind])
                self.player_field[ind] = card.BlankCard()
            self.player_field[zone] = self.hand[index]
            self.player_field[zone].play(zone=zone)
            self.hand.pop(index)
            played = True
        os.system('clear')
        self.print_field()
        return played

    def attack(self) :
        pass

    def check_states(self) :
        '''
        checks for dead cards and removes them, plus returns unkillables if player's turn
        '''
        for zone in self.player_field :
            if self.player_field[zone].status == 'dead' and self.player_field[zone].sigil != 'unkillable' :
                self.player_field[zone].die(self.player_field[zone-1], self.player_field[zone+1], self.player_field)
                self.graveyard.append(self.player_field[zone])
                self.player_field[zone] = card.BlankCard()
            elif self.player_field[zone].status == 'dead' and self.player_field[zone].sigil == 'unkillable' :
                self.player_field[zone].die(self.player_field[zone-1], self.player_field[zone+1], self.player_field)
                self.player_field[zone].status = 'alive'
                self.hand.append(self.player_field[zone])
                self.player_field[zone] = card.BlankCard()
        for zone in self.opponent_field :
            if self.opponent_field[zone].status == 'dead' :
                self.opponent_field[zone].die(self.opponent_field[zone-1], self.opponent_field[zone+1], self.opponent_field)
                self.graveyard.append(self.opponent_field[zone])
                self.opponent_field[zone] = card.BlankCard()

    def advance(self) :
        pass

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
        if self.score['player'] - self.score['opponent'] >= 5 :
            win = True
            winner = 'player'
            overkill = self.score['player'] - self.score['opponent'] - 5
        elif self.score['opponent'] - self.score['player'] >= 5 :
            win = True
            winner = 'opponent'
        return (win, winner, overkill)

    def print_remaining(self) :
        '''
        prints the remaining cards in the deck (sorted) and the squirrels (sorted) (clears screen first)
        '''
        sorted_main_deck = sorted(self.player_deck, key=lambda x: x.name)
        sorted_main_deck = sorted(sorted_main_deck, key=lambda x: x.cost)
        chunked = list(itertools312.batched(sorted_main_deck, 8)) 
        deck_string = ''
        for chunk in chunked :
            for n in range(11) :
                deck_string += ' '*5
                for card in chunk :
                    deck_string += card.TextByLine() + ' '*5
                deck_string += '\n'
            deck_string += '\n'
        os.system('clear')
        print(' '*5 + 'Remaining cards in deck:')
        print(deck_string, end='')
        print(' '*5 + 'Remaining squirrels: ' + str(len(self.player_squirrels)))

    def print_graveyard(self) :
        '''
        prints the cards in the graveyard (in order) (clears screen first)
        '''
        chunked = list(itertools312.batched(self.graveyard, 8)) 
        graveyard_string = ''
        for chunk in chunked :
            for n in range(11) :
                graveyard_string += ' '*5
                for card in chunk :
                    graveyard_string += card.TextByLine() + ' '*5
                graveyard_string += '\n'
            graveyard_string += '\n'
        os.system('clear')
        print(' '*5 + 'Graveyard:')
        print(graveyard_string, end='')
    
    def print_hand(self) : # unsorted for the time being
        '''
        prints the cards in the player's hand (does NOT clear screen first)
        '''
        chunked = list(itertools312.batched(self.hand, 8))
        hand_string = ''
        for chunk in chunked :
            for n in range(11) :
                hand_string += ' '*5
                for card in chunk :
                    hand_string += card.TextByLine() + ' '*5
                hand_string += '\n'
        print(' '*5 + 'Hand:')
        print(hand_string, end='')

    def print_field(self) :
        '''
        prints the field and score scales (clears screen first)
        '''
        os.system('clear')
        vis_bushes = [self.bushes[1], self.bushes[2], self.bushes[3], self.bushes[4], self.bushes[5]]
        vis_opponent_field = [self.opponent_field[1], self.opponent_field[2], self.opponent_field[3], self.opponent_field[4], self.opponent_field[5]]
        vis_player_field = [self.player_field[1], self.player_field[2], self.player_field[3], self.player_field[4], self.player_field[5]]
        field_list = [vis_bushes, vis_opponent_field, vis_player_field]
        field_string = ''
        for row in field_list :
            for n in range(11) :
                field_string += ' '*16
                for card in row :
                    field_string += card.TextByLine() + ' '*16
                field_string += '\n'
            if row == vis_opponent_field :
                field_string += ' '*5 + '-'*161 + '\n'
        print(field_string, end='')
        # print scales
        if self.score['player'] > self.score['opponent'] :
            if self.score['player'] - self.score['opponent'] > 5 :
                player_weight = '▄▄▄▄▄'
                opponent_weight = '_____'
            player_weight = '▄' * (self.score['player'] - self.score['opponent'])
            player_weight += '_' * (5 - (self.score['player'] - self.score['opponent']))
            opponent_weight = '_____'
        elif self.score['opponent'] > self.score['player'] :
            if self.score['opponent'] - self.score['player'] > 5 :
                opponent_weight = '▄▄▄▄▄'
                player_weight = '_____'
            opponent_weight = '▄' * (self.score['opponent'] - self.score['player'])
            opponent_weight += '_' * (5 - (self.score['opponent'] - self.score['player']))
            player_weight = '_____'
        else :
            player_weight = '_____'
            opponent_weight = '_____'
        ASCII_text.print_scales(player_weight, opponent_weight)

    def print_full_field(self) :
        '''
        prints the field and player's hand (clears screen first)
        '''
        self.print_field()
        self.print_hand()

if __name__ == '__main__' :
    os.system('clear')
    leshy_deck = deck.Deck([card_library.Asp(), card_library.Rabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.Rabbit(), card_library.Falcon(), card_library.DumpyTF(), card_library.Rabbit(), card_library.Falcon(), card_library.DumpyTF()])
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
            os.system('clear')
            testmat.print_field()
            print(' '*5 + 'Card to play: ')
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
    input('Press enter to continue. (kill played card)')
    testmat.player_field[zone_to_play].status = 'dead'
    testmat.check_states()
    testmat.print_full_field()