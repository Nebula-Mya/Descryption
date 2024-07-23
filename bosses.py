import card_library
import deck
import field
import QoL
import ASCII_text
import random
import math
import os
import sys
def card_battle(campaign, Poss_Leshy=None) : 
    '''
    starts a card battle between the player and Leshy, with the player's deck being campaign.player_deck
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
        Poss_Leshy: the possible cards for Leshy's deck, defaults to all allowed Leshy cards with costs <= to player's max cost (list)

    Returns:
        bool: True if the player wins, False if the player loses
    '''
    def gameplay(campaign, Poss_Leshy) :
        import duel

        data_to_read = [
            ['settings', 'difficulty', 'leshy median plays'],
            ['settings', 'difficulty', 'leshy plays variance'],
            ['settings', 'difficulty', 'leshy strat chance'],
            ['settings', 'difficulty', 'leshy offense threshold']
        ]
        [play_median, play_var, opp_strat, opp_threshold] = QoL.read_data(data_to_read)

        deck_size = len(campaign.player_deck.cards)

        if Poss_Leshy :
            leshy_deck = duel.deck_gen(Poss_Leshy, int(deck_size * 1.5))
        else :
            player_max_cost = max([card.saccs for card in campaign.player_deck.cards])
            fair_poss_leshy = {cost: [card for card in card_library.Poss_Leshy[cost]] for cost in range(0, max(3, player_max_cost+1))} # may be changed later for balancing
            leshy_deck = duel.deck_gen(fair_poss_leshy, int(deck_size * 1.5))
        
        QoL.clear()
        print('\n')
        wick_states = [2] + [3] * (campaign.lives - 1)
        wick_states += [0] * (3 - len(wick_states))
        ASCII_text.print_candelabra(wick_states)
        print(QoL.center_justified('As you approach the figure, Leshy blows out all but one of your candles.').rstrip())
        print(QoL.center_justified('"Beat this boss and I\'ll relight your candles."').rstrip())
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

        (_, winner, overkill, _) = duel.main(deck_size, 4, play_median, play_var, opp_strat, opp_threshold, player_deck_obj=campaign.player_deck, opponent_deck_obj=leshy_deck, squirrels_deck_obj=campaign.squirrel_deck, print_results=False)

        if winner == 'opponent' :
            campaign.lives = 0
            QoL.clear()
            print('\n'*3)
            wick_states = (campaign.lives) * [2] + [3]
            wick_states += [0] * (3 - len(wick_states))
            ASCII_text.print_candelabra(wick_states)
            print()
            input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
            return False
        
        campaign.add_teeth(overkill)
        QoL.clear()
        print('\n'*3)
        wick_states = (campaign.lives) * [2]
        wick_states += [0] * (3 - len(wick_states))
        ASCII_text.print_candelabra(wick_states)
        print()
        return True
    
    return gameplay(campaign, Poss_Leshy) # add flavor text, context, etc.

##### bosses will use the basic AI, but with higher difficulty settings and have their unique mechanics (pickaxe, ship, extra sigils, moon)

##### bosses essentially work as two duels, but winning the first duel triggers a special event (the bosses unique mechanic) and the second duel starts from where the first left off

##### before boss fights, all but one candle will be extinguished, and a smoke card will be added to the deck for each candle extinguished 

##### after a boss fight, remove all smoke cards from the deck

##### if the player loses to a boss, set campaign.has_lost = True, as lives arent updated during the previous thing

##### if the player wins, relight candles and update config file

def pre_boss_flavor(campaign) :
    # pre fight flavor text, extra lives being extinguished, etc.
    pass

def boss_fight_prospector(campaign) : # boss fight 1
    def gameplay(campaign) :
        return card_battle(campaign) # for testing prior to implementation

    return gameplay(campaign) # add flavor text, context, etc.

def boss_fight_angler(campaign) : # boss fight 2
    def gameplay(campaign) :
        return card_battle(campaign) # for testing prior to implementation

    return gameplay(campaign) # add flavor text, context, etc.

def boss_fight_trapper_trader(campaign) : # boss fight 3
    def gameplay(campaign) :
        return card_battle(campaign) # for testing prior to implementation

    return gameplay(campaign) # add flavor text, context, etc.

def boss_fight_leshy(campaign) : # boss fight 4
    def gameplay(campaign) :
        return card_battle(campaign) # for testing prior to implementation

    return gameplay(campaign) # add flavor text, context, etc.