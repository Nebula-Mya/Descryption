import itertools312
import os

class Deck() :
    '''
    data structure for storing cards in player's decks

    Attributes:
        cards: cards in players deck (list)

    Methods:
        addCard(index): adds card to deck
        removeCard(index) : removes card from deck
        changeSigil(index, sigil): changes card's sigil
        shuffle(): generates a shuffled list of cards
        print(): prints decklist
    '''
    def __init__(self, cards) :
        self.cards = cards
    
    def addCard(self, index) :
        pass
    
    def removeCard(self, index) :
        pass

    def changeSigil(self, index, sigil) :
        pass

    def shuffle(self) :
        pass

    def __str__(self) : 
        chunked = list(itertools312.batched(self.cards, 8)) 
        deck_string = ''
        for chunk in chunked :
            for n in range(11) :
                for card in chunk :
                    deck_string += card.TextByLine() + '     '
                deck_string += '\n'
            deck_string += '\n'
        return deck_string

if __name__ == '__main__' :
    import card
    slot1 = card.BlankCard()
    slot2 = card.BlankCard(name='left',cost=3,attack=1,life=2,sigil='lane shift left')
    slot3 = card.BlankCard()
    slot4 = card.BlankCard(name='bifurcate',cost=3,attack=17,life=2,sigil='bifurcate')
    slot5 = card.BlankCard(name='split',cost=3,attack=1,life=2,sigil='split')
    slot6 = card.BlankCard(name='unkillable',cost=3,attack=1,life=2,sigil='unkillable')
    slot7 = card.BlankCard(name='venom',cost=3,attack=1,life=2,sigil='venom')
    slot8 = card.BlankCard()
    slot9 = card.BlankCard(name='right',cost=3,attack=1,life=2,sigil='lane shift right')
    slot10 = card.BlankCard()
    decklist = [slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10]
    testdeck = Deck(decklist)
    print(testdeck)
    slot4.takeDamage(1)
    os.system('clear')
    print(testdeck)