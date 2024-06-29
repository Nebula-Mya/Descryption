import deck
import duel
import QoL
import card_library
import ASCII_text
import menu

class campaign : # stores the current campaign data, such as the current level, the current decks, teeth (money), progress in the level, candles, etc.
    '''
    the current campaign data, such as the current level, the current decks, teeth (money), progress in the level, candles, etc.
    
    Attributes:
        level: the current level of the campaign (int)
        progress: the current progress in the level (int)
        player_deck: the player's deck (deck.Deck)
        teeth: the player's money (int)
        lives: the player's lives (int)

    Methods:
        add_teeth: adds teeth to the player's total
        add_life: adds a life to the player's total
        remove_life: removes a life from the player's total
        add_card: adds a card to the player's deck
        remove_card: removes a card from the player's deck
        change_sigil: changes the sigil of a card in the player's deck
        shuffle_deck: shuffles the player's deck
        print_deck: prints the player's deck
    '''
    def __init__(self, start_decklist, start_teeth=0, lives=2) :
        '''
        initializes the campaign object
        
        Arguments:
            start_decklist: the starting decklist for the player (list)
            start_teeth: the starting amount of teeth for the player, defaults to 0 (int)
            lives: the starting amount of lives for the player, defaults to 2 (int)
        '''
        self.level = 0
        self.progress = 0
        self.player_deck = deck.Deck(start_decklist)
        self.teeth = start_teeth
        self.lives = lives

    def add_teeth(self, amount) :
        self.teeth += amount
    
    def add_life(self) :
        self.lives += 1
    
    def remove_life(self) :
        self.lives -= 1
        if self.lives <= 0 :
            self.lost_run()

    def add_card(self, card) :
        '''
        adds a card to the player's deck
        
        Arguments:
            card: the card to add to the player's deck (card object)
        '''
        self.player_deck.add_card(card)

    def remove_card(self, index) :
        '''
        removes a card from the player's deck
        
        Arguments:
            index: the index of the card to remove (int)
        '''
        self.player_deck.remove_card(index)

    def change_sigil(self, index, sigil, sigil_slot) :
        '''
        changes the sigil of a card in the player's deck
        
        Arguments:
            index: index of card to change (int)
            sigil: sigil to change to (str)
            sigil_slot: slot to change sigil in, 1 or 2 (int)
        '''
        self.player_deck.change_sigil(index, sigil, sigil_slot)
    
    def shuffle_deck(self) :
        return self.player_deck.shuffle()
    
    def print_deck(self) :
        print(self.player_deck)

def card_battle(Poss_Leshy=None, Squirrels=None) : # random encounter
    '''
    starts a card battle between the player and Leshy, with the player's deck being campaign.player_deck
    
    Arguments:
        Poss_Leshy: the possible cards for Leshy's deck, defaults to None (list)
        Squirrels: the possible Squirrel deck, defaults to None (list)

    Returns:
        bool: True if the player wins, False if the player loses
    '''
    data_to_read = [
        ['settings', 'hand size'],
        ['settings', 'difficulty', 'leshy median plays'],
        ['settings', 'difficulty', 'leshy plays variance'],
        ['settings', 'difficulty', 'leshy strat chance'],
        ['settings', 'difficulty', 'leshy offense threshold']
    ]
    [hand_size, play_median, play_var, opp_strat, opp_threshold] = QoL.read_data(data_to_read)

    deck_size = len(campaign.player_deck)

    if Poss_Leshy :
        leshy_deck = duel.deck_gen(Poss_Leshy, deck_size*2)
    else :
        leshy_deck = None
    
    if Squirrels :
        squirrel_deck = deck.Deck(Squirrels)
    else :
        squirrel_deck = None

    (_, winner, overkill, _) = duel.main(deck_size, hand_size, play_median, play_var, opp_strat, opp_threshold, player_deck_obj=campaign.player_deck, leshy_deck_obj=leshy_deck, squirrel_deck_obj=squirrel_deck)

    if winner == 'opponent' :
        campaign.remove_life()
        return False
    
    campaign.add_teeth(overkill)

    return True

def card_choice(type=0) : # choose from 3 cards to add to deck
    '''
    <placeholder description>

    Arguments:
        type: the type of card choice, 0 for normal, 1 for cost, 2 for deathcards, defaults to 0 (int)
    '''
    def normal_choice() : # choose a card from a list of 3 taken from card_library.Poss_Playr
        pass

    def cost_choice() : # choose a card from a list of 3 taken from card_library.Poss_Cost, only seeing the costs of the cards
        pass

    def death_choice() : # choose from 3 death cards taken from card_library.Poss_Death, only available after 5 deaths
        pass

    match type : 
        case 0 : normal_choice()
        case 1 : cost_choice()
        case 2 : death_choice()
        case _ : raise ValueError('Invalid type')

def sigil_sacrifice() : # sacrifice a card to give its sigil to another card
    pass

def merge_cards() : # mycologists; merge two cards of the same species into one, with the new card having combined stats and sigils
    pass

def pelt_shop() : # trader; buy pelts with teeth
    pass

def card_shop() : # trader; buy cards with pelts
    pass

def break_rocks() : # prospector; break 1 of 3 rocks for bug cards or golden pelt (bugs may have additional sigils, only one rock has golden pelt)
    pass

def campfire() : # campfire; increase a cards health or damage, risking the card being destroyed
    '''
    each time a card rests by the Campfire, it gains a buff to its Power(+1) or Health(+2) (the stat is set before the player 'arrives')

    prior to 5 runs, the player can buff only once

    a card can be buffed up to 4 times, with the following chances of destruction:
    1 buff: 0% chance of destruction
    2 buffs: 22.5% chance of destruction
    3 buffs: 45% chance of destruction
    4 buffs: 67.5% chance of destruction
    '''
    pass

def lost_run() : # death / loss ('cutscene' of sorts, with flavor text, etc., + make death card after 4 deaths)
    pass # making a death card will shift the values of 'second' to 'third', 'first' to 'second', and the new death card will be written to 'first'

def beat_leshy() : # create 'win' card, largely the same as death / loss function, differing mostly in flavor
    pass

##### bosses will use the basic AI, but with higher difficulty settings and have their unique mechanics (pickaxe, ship, extra sigils, moon)

def boss_fight_prospector() : # boss fight 1
    pass

def boss_fight_angler() : # boss fight 2
    pass

def boss_fight_trapper_trader() : # boss fight 3
    pass

def boss_fight_leshy() : # boss fight 4
    pass

def split_road() : # choose path, the main function that handles all others, most of the game loop will be here
    pass

def main() : # coordinates the game loop, calls split_road, manages losses, initiates the game, etc.
    QoL.clear()
    print(menu.version_ID)
    print('\n'*2)
    ASCII_text.print_title()
    print('\n'*2)
    ASCII_text.print_WiP()
    input(QoL.center_justified('Press Enter to go back...').rstrip() + ' ')

if __name__ == '__main__' :
    pass
