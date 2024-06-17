import QoL
import random
import copy

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
        sorted_deck = QoL.sort_deck(self.cards)
        card = sorted_deck[index]
        self.cards.remove(card)

    def change_sigil(self, index, sigil) :
        '''
        changes card's sigil

        Arguments:
            index: index of card to change (int)
            sigil: sigil to change to (str)
        '''
        sorted_deck = QoL.sort_deck(self.cards)
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
        return QoL.print_deck(self.cards, sort=True, fruitful=True)

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
    for _ in range(2) :
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