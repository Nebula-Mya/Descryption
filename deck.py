import itertools312
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
        addCard(card): adds card to deck
        removeCard(index) : removes card from deck
        changeSigil(index, sigil): changes card's sigil
        shuffle(): generates a shuffled list of cards
        print(): prints decklist
    '''
    def __init__(self, cards) :
        self.cards = cards
    
    def addCard(self, card) :
        '''
        adds card to deck

        Arguments:
            card: card to add to deck (card object)
        '''
        self.cards.append(card)
    
    def removeCard(self, index) :
        '''
        removes card from deck

        Arguments:
            index: index of card to remove (int)
        '''
        sorted_deck = sorted(self.cards, key=lambda x: x.name)
        sorted_deck = sorted(sorted_deck, key=lambda x: x.cost)
        card = sorted_deck[index]
        self.cards.remove(card)

    def changeSigil(self, index, sigil) :
        '''
        changes card's sigil

        Arguments:
            index: index of card to change (int)
            sigil: sigil to change to (str)
        '''
        sorted_deck = sorted(self.cards, key=lambda x: x.name)
        sorted_deck = sorted(sorted_deck, key=lambda x: x.cost)
        sorted_deck[index].sigil = sigil 

    def shuffle(self) :
        '''
        generates a shuffled list of cards
        '''
        shuffled_deck = copy.deepcopy(self.cards) # deep copy to avoid changing original deck, may need to be changed to shallow copy, we shall see
        random.shuffle(shuffled_deck)
        return shuffled_deck

    def __str__(self) : 
        (term_cols, term_rows) = os.get_terminal_size()
        card_gaps = (term_cols*55 // 100) // 5 - 15
        sorted_deck = sorted(self.cards, key=lambda x: x.name)
        sorted_deck = sorted(sorted_deck, key=lambda x: x.cost)
        (term_cols, term_rows) = os.get_terminal_size()
        card_gaps = (term_cols*55 // 100) // 5 - 15
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8
        chunked = list(itertools312.batched(sorted_deck, cards_per_row)) 
        deck_string = ''
        for chunk in chunked :
            for n in range(11) :
                deck_string += ' '*card_gaps
                for card in chunk :
                    deck_string += card.TextByLine() + ' '*card_gaps
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
    slot4.takeDamage(1)
    QoL.clear()
    print(testdeck)
    slot5.explain()
    print(testdeck.shuffle())