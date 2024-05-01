import itertools

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

    def __str__(self) : # NOT WORKING (figure out showing a certain number per line)
        chunked = list(itertools.batched(self.cards, 4)) # batched not working????
        for chunk in chunked :
            for n in range(11) :
                for card in chunk :
                    card.displayByLine()
                    print('     ', end = '')

if __name__ == '__main__' :
    import card
    slot1 = card.BlankCard()
    slot2 = card.BlankCard()
    slot3 = card.BlankCard()
    slot4 = card.BlankCard()
    slot5 = card.BlankCard()
    slot6 = card.BlankCard()
    decklist = [slot1, slot2, slot3, slot4, slot5, slot6]
    testdeck = Deck(decklist)
    print(testdeck)