import itertools312
import os
import random
import copy

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
        self.cards.append(card)
    
    def removeCard(self, index) :
        sorted_deck = sorted(self.cards, key=lambda x: x.name)
        sorted_deck = sorted(sorted_deck, key=lambda x: x.cost)
        card = sorted_deck[index]
        self.cards.remove(card)

    def changeSigil(self, index, sigil) :
        sorted_deck = sorted(self.cards, key=lambda x: x.name)
        sorted_deck = sorted(sorted_deck, key=lambda x: x.cost)
        card = sorted_deck[index]
        card_name = card.species
        card_cost = card.saccs
        card_attack = card.base_attack
        card_life = card.base_life
        card = card.BlankCard(name=card_name, cost=card_cost, attack=card_attack, life=card_life, sigil=sigil) 

    def shuffle(self) :
        shuffled_deck = copy.deepcopy(self.cards) # deep copy to avoid changing original deck, may need to be changed to shallow copy, we shall see
        random.shuffle(shuffled_deck)
        return shuffled_deck

    def __str__(self) : 
        sorted_deck = sorted(self.cards, key=lambda x: x.name)
        sorted_deck = sorted(sorted_deck, key=lambda x: x.cost)
        chunked = list(itertools312.batched(sorted_deck, 8)) 
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
    testdeck = Deck(decklist)
    print(testdeck)
    slot4.takeDamage(1)
    os.system('clear')
    print(testdeck)
    slot5.explain()
    print(testdeck.shuffle())