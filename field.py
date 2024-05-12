import card
import card_library
import deck
import sigils
import os
import ASCII_text

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
        check_states() : checks for dead cards and removes them, plus returns unkillables if player's turn (unimplemented)
        advance() : advances cards from bushes to field (unimplemented)
        switch() : switches the active player
        check_win() : checks for a win condition
        print_remaining() : prints the remaining cards in the deck (sorted) and the squirrels (sorted) (unimplemented)
        print_graveyard() : prints the cards in the graveyard (in order) (unimplemented)
        print_field() : prints the field and score scales
        print_full_field() : prints the field and player's hand (unimplemented)
    '''
    def __init__(self, deck, squirrels, opponent_deck) :
        self.bushes = {0: card.BlankCard(), 1: card.BlankCard(), 2: card.BlankCard(), 3: card.BlankCard(), 4: card.BlankCard(), 5: card.BlankCard(), 6: card.BlankCard()}
        self.player_field = {0: card.BlankCard(), 1: card.BlankCard(), 2: card.BlankCard(), 3: card.BlankCard(), 4: card.BlankCard(), 5: card.BlankCard(), 6: card.BlankCard()}
        self.opponent_field = {0: card.BlankCard, 1: card.BlankCard(), 2: card.BlankCard(), 3: card.BlankCard(), 4: card.BlankCard(), 5: card.BlankCard(), 6: card.BlankCard()}
        self.hand = []
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
            played: if the card was played successfully (bool)
        '''
        os.system('clear')
        self.print_field()
        print()
        self.hand[index].explain()
        cost = self.hand[index].saccs
        print('Sacrifices required:', cost)
        print('Select sacrifices: (none to go back)')
        sacc_list = []
        while len(sacc_list) < cost :
            sacc_index_list = input('')
            sacc_indexes = []
            for char in sacc_index_list :
                sacc_indexes.append(int(char))
            if sacc_index_list == '' :
                played = False
                sacc_list = []
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
        if len(sacc_list) != 0:
            for ind in sacc_list :
                self.player_field[ind].sacc()
                self.graveyard.append(self.player_field[ind])
                self.player_field[ind] = card.BlankCard()
            self.player_field[zone] = self.hand[index]
            self.player_field[zone].play(zone=zone)
            self.hand.pop(index)
            played = True
        os.system('clear')
        self.print_full_field()
        return played

    def attack(self) :
        pass

    def check_states(self) :
        pass

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
        pass

    def print_graveyard(self) :
        pass

    def print_field(self) :
        '''
        prints the field and score scales
        '''
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
        pass

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
    testmat.print_field()
    testmat.hand[0].explain()
    bad_input = True
    while bad_input :
        zone_to_play = input('Zone to play: ')
        try :
            zone_to_play = int(zone_to_play)
        except :
            zone_to_play = 0
        if zone_to_play in range(1, 6) :
            bad_input = False
        else :
            print('Invalid zone.')
    testmat.play_card(0, zone_to_play)
    testmat.print_field()