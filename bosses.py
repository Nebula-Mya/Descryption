import card_library
import deck
import field
import QoL
import ASCII_text
import random
import math
import os
import sys
import rogue

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
    def gameplay() :
        rogue.card_battle() # for testing prior to implementation

    gameplay() # add flavor text, context, etc.

def boss_fight_angler(campaign) : # boss fight 2
    def gameplay() :
        rogue.card_battle() # for testing prior to implementation

    gameplay() # add flavor text, context, etc.

def boss_fight_trapper_trader(campaign) : # boss fight 3
    def gameplay() :
        rogue.card_battle() # for testing prior to implementation

    gameplay() # add flavor text, context, etc.

def boss_fight_leshy(campaign) : # boss fight 4
    def gameplay() :
        rogue.card_battle() # for testing prior to implementation
        
    gameplay() # add flavor text, context, etc.