import card
import card_library
import deck
import sigils
import os

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
        draw(deck) : draws a card from the deck to the hand (deck is main or resource (str))
        play_card(index, zone) : plays a card to the field (first opens card explanation and has player select saccs, then plays card to zone)
        attack() : attacks with all of the active player's cards in play and updates score (unimplemented)
        check_states() : checks for dead cards and removes them, plus returns unkillables if player's turn (unimplemented)
        advance() : advances cards from bushes to field (unimplemented)
        switch() : switches the active player (unimplemented)
        check_win() : checks for a win condition (unimplemented)
        print_remaining() : prints the remaining cards in the deck (sorted) and the squirrels (sorted) (unimplemented)
        print_graveyard() : prints the cards in the graveyard (in order) (unimplemented)
        print_field() : prints the field (unimplemented)
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
        plays a card to the field from the hand

        Arguments:
            index: the index of the card in the hand (int)
            zone: the zone to play the card to (int)
        '''
        self.player_field[zone] = self.hand[index]
        self.player_field[zone].play()
        self.hand.pop(index)

    def attack(self) :
        pass

    def check_states(self) :
        pass

    def advance(self) :
        pass

    def switch(self) :
        pass

    def check_win(self) :
        pass

    def print_remaining(self) :
        pass

    def print_graveyard(self) :
        pass

    def print_field(self) :
        pass

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
    print('Player Deck:')
    print(testmat.player_deck)
    print()
    print('Player Hand:')
    print(testmat.hand)
    print()
    print()
    print('Drawing from main deck...')
    testmat.draw('main')
    print()
    print('Player Deck:')
    print(testmat.player_deck)
    print()
    print('Player Hand:')
    print(testmat.hand)
    print()
    print()
    print('Playing card to zone 1...')
    testmat.play_card(0, 1)
    print()
    print('Player Hand:')
    print(testmat.hand)
    print()
    print('Player Field:')
    print(testmat.player_field)