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
        refresh_ASCII(): refreshes ASCII art for all cards in deck
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
    
    def check_index(self, index) :
        '''
        checks if index is valid

        Arguments:
            index: index to check (int)
        '''
        deck_length = len(self.cards)
        if index >= deck_length or index < 0:
            raise IndexError(f"index {index} is out of range for deck of length {deck_length}")

    def remove_card(self, index) :
        '''
        removes card from deck

        Arguments:
            index: index of card to remove (int)
        '''
        self.check_index(index) # error handling

        sorted_deck = QoL.sort_deck(self.cards)
        card = sorted_deck[index]
        self.cards.remove(card)

    def change_sigil(self, index, sigil, sigil_slot) :
        '''
        changes card's sigil

        Arguments:
            index: index of card to change (int)
            sigil: sigil to change to (str)
            sigil_slot: slot to change sigil in, 0 or 1 (int)
        '''
        # set up variables
        sorted_deck = QoL.sort_deck(self.cards)
        same_sigil = False

        # error handling
        self.check_index(index)
        if sigil_slot not in [0,1] :
            raise ValueError(f"invalid sigil slot: {sigil_slot}")
        if len(sorted_deck[index].sigils) != 2 :
            raise ValueError('Sigils must be a list of length 2.')
        match sigil_slot :
            case 0 :
                same_sigil = (sorted_deck[index].sigils[1] == sigil) or ('hefty' in sorted_deck[index].sigils[1] and 'hefty' in sigil) or ('lane shift' in sorted_deck[index].sigils[1] and 'lane shift' in sigil)
            case 1 :
                same_sigil = (sorted_deck[index].sigils[0] == sigil) or ('hefty' in sorted_deck[index].sigils[0] and 'hefty' in sigil) or ('lane shift' in sorted_deck[index].sigils[0] and 'lane shift' in sigil)
        if same_sigil :
            match sigil_slot :
                case 0 :
                    remaining_sigil = sorted_deck[index].sigils[1]
                case 1 :
                    remaining_sigil = sorted_deck[index].sigils[0]
                case _ :
                    remaining_sigil = ''
            raise ValueError(f"invalid sigil pair: {remaining_sigil} and {sigil}")
        
        # change sigil
        match sigil_slot :
            case 0 :
                sorted_deck[index].sigils[0] = sigil
            case 1 :
                sorted_deck[index].sigils[1] = sigil
        
        sorted_deck[index].update_ASCII()

    def shuffle(self, fair_hand=False) :
        '''
        generates a shuffled list of cards

        Arguments:
            fair_hand: whether to shuffle the deck in a way that ensures a playable hand (bool)
        '''
        hand_size = QoL.read_data([['settings', 'hand size']])[0]
        fair_check = lambda list : min([card.saccs for card in list[:hand_size - 1]]) <= (1 + len([card_ for card_ in list[:hand_size - 1] if card_.saccs == 0])) # check if hand is playable
        
        while True :
            shuffled_deck = copy.deepcopy(self.cards) # avoid changing original deck
            random.shuffle(shuffled_deck)
            if not fair_hand or fair_check(shuffled_deck) :
                return shuffled_deck

    def refresh_ASCII(self) :
        '''
        refreshes ASCII art for all cards in deck
        '''
        for card in self.cards :
            card.update_ASCII()

    def __str__(self) : 
        return QoL.print_deck(self.cards, sort=True, fruitful=True, numbered=True)

if __name__ == '__main__' :
    import card_library
    import duel

    test_deck_player = duel.deck_gen(card_library.Poss_Playr, 16)
    test_deck_opponent = duel.deck_gen(card_library.Poss_Leshy, 16)

    # display decks
    QoL.clear()
    print('Possible player deck:')
    print(test_deck_player)
    print()
    print('Possible opponent deck:')
    print(test_deck_opponent)