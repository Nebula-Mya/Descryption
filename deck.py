import QoL
import random
import copy
import os

class Deck() :
    '''
    data structure for storing cards in player's decks

    Attributes:
        cards: cards in players deck (list)

    Methods:
        add_card(card): adds card to deck
        remove_card(index) : removes card from deck
        change_sigil(index, sigil): changes card's sigil
        shuffle(): generates a shuffled list of cards
        print(): prints decklist
    '''
    def __init__(self, cards) :
        self.cards = cards
    
    def sorted_deck(self) :
        '''
        sorts deck by cost then name
        '''
        sorted_deck = sorted(self.cards, key=lambda x: x.name) # sort by name (will be sub-sorting under cost)
        return sorted(sorted_deck, key=lambda x: x.cost) # sort by cost

    def add_card(self, card) :
        '''
        adds card to deck

        Arguments:
            card: card to add to deck (card object)
        '''
        self.cards.append(card)
    
    def remove_card(self, index) :
        '''
        removes card from deck

        Arguments:
            index: index of card to remove (int)
        '''
        sorted_deck = self.sorted_deck()
        card = sorted_deck[index]
        self.cards.remove(card)

    def change_sigil(self, index, sigil) :
        '''
        changes card's sigil

        Arguments:
            index: index of card to change (int)
            sigil: sigil to change to (str)
        '''
        sorted_deck = self.sorted_deck()
        sorted_deck[index].sigil = sigil 
        sorted_deck[index].update_ASCII()

    def shuffle(self) :
        '''
        generates a shuffled list of cards
        '''
        shuffled_deck = copy.deepcopy(self.cards) # avoid changing original deck
        random.shuffle(shuffled_deck)
        return shuffled_deck

    def __str__(self) : 
        # get terminal size
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15

        sorted_deck = self.sorted_deck()

        # get number of cards per row
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8
    
        chunked = QoL.chunk(sorted_deck, cards_per_row)

        # generate deck string
        deck_string = ''
        for chunk in chunked :
            for n in range(11) :
                deck_string += ' '*card_gaps
                for card in chunk :
                    deck_string += card.text_by_line() + ' '*card_gaps
                deck_string += '\n'
            deck_string += '\n'
        return deck_string

if __name__ == '__main__' :
    import card_library
    slot1 = card_library.Squirrel()
    slot2 = card_library.Rabbit()
    slot3 = card_library.Squirrel()
    slot4 = card_library.Lobster()
    slot5 = card_library.BoppitW()
    slot6 = card_library.Ouroboros()
    slot7 = card_library.Asp()
    slot8 = card_library.Turtle()
    slot9 = card_library.Falcon()
    slot10 = card_library.DumpyTF()
    decklist = [slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10]
    for n in range(2) :
        decklist.append(card_library.Squirrel())
    testdeck = Deck(decklist)
    print(testdeck)
    print(testdeck.cards[4])
    testdeck.cards[4].take_damage(1, hand=[])
    testdeck.change_sigil(4, 'hefty (right)')
    QoL.clear()
    print(testdeck)
    slot5.explain()
    print(testdeck.shuffle())