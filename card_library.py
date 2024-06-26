import card
import QoL
import random

class Squirrel(card.BlankCard) :
    '''
    A squirrel card, which can be used as a resource to play other cards.
    '''
    def __init__(self, blank_cost=False) :
        super().__init__(species='Squirrel', cost=0, attack=0, life=1, blank_cost=blank_cost)

class Rabbit(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigil=['lane shift right'], blank_cost=blank_cost)
    
class OppositeRabbit(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost=False) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigil=['lane shift left'], blank_cost=blank_cost)

class Shrew(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigil=['lane shift left'], blank_cost=blank_cost)

class OppositeShrew(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost=False) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigil=['lane shift right'], blank_cost=blank_cost)

class DumpyTF(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Dumpy Tree Frog', cost=1, attack=2, life=2, blank_cost=blank_cost)

class Turtle(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Turtle', cost=1, attack=0, life=4, blank_cost=blank_cost)

class Asp(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Asp', cost=2, attack=2, life=2, sigil=['venom'], blank_cost=blank_cost)

class Falcon(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Falcon', cost=2, attack=3, life=1, sigil=['airborne'], blank_cost=blank_cost)

class Lobster(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Lobster', cost=3, attack=2, life=3, sigil=['bifurcate'], blank_cost=blank_cost)

class BoppitW(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Boppit Worm', cost=4, attack=3, life=5, sigil=['split'], blank_cost=blank_cost)

class Ouroboros(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        [oro_attack, oro_life] = QoL.read_data([['ouroboros', 'attack'], ['ouroboros', 'life']])
        super().__init__(species='Ouroboros', cost=2, attack=oro_attack, life=oro_life, sigil=['unkillable'], blank_cost=blank_cost)

    def die(self) :
        self.base_attack += 1
        self.base_life += 1
        QoL.write_data([(['ouroboros', 'attack'], self.base_attack), (['ouroboros', 'life'], self.base_life)])
        super().die()

class Cockroach(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Cockroach', cost=2, attack=1, life=1, sigil=['unkillable'], blank_cost=blank_cost)

class Stoat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Stoat', cost=1, attack=1, life=3, blank_cost=blank_cost)

class Wolf(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Wolf', cost=2, attack=3, life=2, blank_cost=blank_cost)

class Grizzly(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Grizzly', cost=3, attack=4, life=6, blank_cost=blank_cost)

class Urayuli(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Urayuli', cost=4, attack=7, life=7, blank_cost=blank_cost)

class Raven(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Raven', cost=2, attack=2, life=3, sigil=['airborne'], blank_cost=blank_cost)

class Bee(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=False, sigil=['airborne']) :
        super().__init__(species='Bee', cost=0, attack=1, life=1, sigil=sigil, blank_cost=blank_cost)

class Bullfrog(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Bullfrog', cost=1, attack=1, life=2, sigil=['mighty leap'], blank_cost=blank_cost)

class BlackGoat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Black Goat', cost=1, attack=0, life=1, sigil=['worthy sacrifice'], blank_cost=blank_cost)

class Beehive(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Beehive', cost=1, attack=0, life=2, sigil=['bees within'], blank_cost=blank_cost)

class Cat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Cat', cost=1, attack=0, life=1, sigil=['many lives'], blank_cost=blank_cost)
        self.spent_lives = 0
    
    def reset_stats(self):
        super().reset_stats()
        self.spent_lives = 0

class UndeadCat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Undead Cat', cost=1, attack=3, life=6, blank_cost=blank_cost)

class MooseBuck(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        if random.randint(0,1) == 0 :
            sigil_direction = ['hefty (left)']
        else :
            sigil_direction = ['hefty (right)']
        super().__init__(species='Moose Buck', cost=4, attack=3, life=7, sigil=sigil_direction, blank_cost=blank_cost)

class Dam(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=True) :
        super().__init__(species='Dam', cost=0, attack=0, life=2, blank_cost=blank_cost)

class Vole(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=False, sigil=None) :
        super().__init__(species='Vole', cost=0, attack=0, life=1, sigil=sigil, blank_cost=blank_cost)

class Warren(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Warren', cost=1, attack=0, life=2, sigil=['vole hole'], blank_cost=blank_cost)

class Beaver(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Beaver', cost=2, attack=1, life=3, sigil=['dam builder'], blank_cost=blank_cost)

class Adder(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Adder', cost=2, attack=1, life=1, sigil=['touch of death'], blank_cost=blank_cost)

class CorpseMaggots(card.BlankCard) : # in Leshy's 1 cost and the player's 2 cost groups due to the 3 cost mainly being a deterrent for the player
    def __init__(self, blank_cost=False) :
        super().__init__(species='Corpse Maggots', cost=3, attack=1, life=2, sigil=['corpse eater'], blank_cost=blank_cost)

class Otter(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Otter', cost=1, attack=1, life=1, sigil=['waterborne'], blank_cost=blank_cost)

class BullShark(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Bull Shark', cost=3, attack=4, life=2, sigil=['waterborne'], blank_cost=blank_cost)

# Allowed cards:
Poss_Playr = {
    0 : [Rabbit(), Shrew(), BlackGoat()],
    1 : [DumpyTF(), Turtle(), Stoat(), Bullfrog(), Beehive(), Cat(), Warren(), Otter()],
    2 : [Asp(), Falcon(), Cockroach(), Wolf(), Raven(), Beaver(), Adder(), CorpseMaggots()]*3 + [Ouroboros()],
    3 : [Lobster(), Grizzly(), BullShark()],
    4 : [BoppitW(), Urayuli(), MooseBuck()]
}
Poss_Leshy = {
    0 : [OppositeRabbit(True), OppositeShrew(True)],
    1 : [DumpyTF(True), Turtle(True), Stoat(True), Bullfrog(True), CorpseMaggots(True), Otter(True)],
    2 : [Asp(True), Falcon(True), Cockroach(True), Wolf(True), Raven(True), Adder(True)],
    3 : [Lobster(True), Grizzly(True), BullShark(True), BoppitW(True)]
}

# categories of cards for intelligent Leshy in order of priority (dicts in list)
AI_categories = [
    # good against airbornes (non airborne glass cannons and those with mighty leap)
    {
        'category' : 'anti_air', 
        'cards' : ['Bullfrog', 'Asp', 'Wolf'], 
        'deals_with' : ['airborne']
        },

    # good against deathtouch (waterbornes and those with deathtouch)
    {
        'category' : 'anti_deathtouch',
        'cards' : ['Adder', 'Otter', 'Bull Shark'], # maybe add some on death effects
        'deals_with' : ['touch of death']
    },

    # good against waterbornes (tanks and those with waterborne)
    {
        'category' : 'anti_water',
        'cards' : ['Otter', 'Bull Shark', 'Boppit Worm', 'Turtle', 'Grizzly', 'Urayuli'],
        'deals_with' : ['waterborne']
    },

    # good against bifurcates (non airborne glass cannons (airbornes wouldnt kill the bifurcate))
    {
        'category' : 'anti_bifurcate', 
        'cards' : ['Asp', 'Wolf'], 
        'deals_with' : ['bifurcate']
        },

    # good against those with on death effects (tanks, airbornes, and bifurcates) (death effects are bees within, split, many lives, and unkillable)
    {
        'category' : 'wont_kill', 
        'cards' : ['Turtle', 'Falcon', 'Raven', 'Lobster', 'Warren', 'Dam', 'Vole'], 
        'deals_with' : ['bees within', 'split', 'many lives', 'unkillable']
        },

    # good against those with venom (fragiles and waterbornes(to be added))
    {
        'category' : 'anti_venom', 
        'cards' : ['Asp', 'Cockroach', 'Dumpy Tree Frog', 'Otter', 'Bull Shark', 'Adder'], 
        'deals_with' : ['venom']
        },

    # good against those moving right (moves with, bifurcate, or trifurcate(to be added))
    {
        'category' : 'anti_right', 
        'cards' : ['Shrew', 'Lobster', 'Beaver'], 
        'deals_with' : ['lane shift right', 'hefty (right)']
        },

    # good against those moving left (moves with, bifurcate, or trifurcate(to be added))
    {
        'category' : 'anti_left', 
        'cards' : ['Rabbit', 'Lobster', 'Beaver'], 
        'deals_with' : ['lane shift left', 'hefty (left)']
        },
]

Better_AI_categories = [
    ### planning ###
    # each member will be a dict with the following keys :
    ### 'category' : the category/strategy's name for reference (having it stored will be useful for debugging)
    ### 'self sigils': a list of sigils that use the strategy
    ### 'opp sigils' : a list of sigils that the strategy is good against
    ### 'stats' : a lambda function that takes in the stats of the card and the opponent's card and returns a boolean of whether the card is good in the situation

    ### example (for waterborne) :
    ''' 
    'stats' : (lambda self_attack, self_life, opp_attack, opp_life : opp_attack < 3 and self_life > 2 * opp_attack),
    '''
    ### then you just call 'waterborne'['stats'](self_attack, self_life, opp_attack, opp_life) to get the result and factor that into the decision

    # use a function within ai_category_checking to get a boolean of whether the zone is in strategy or not, combining the different factors
]

if __name__ == '__main__' :
    import deck
    Leshy_cardlist = deck.Deck([])
    for cost in Poss_Leshy :
        for card in Poss_Leshy[cost] :
            Leshy_cardlist.add_card(card)

    Player_cardlist = deck.Deck([])
    for cost in Poss_Playr :
        for card in Poss_Playr[cost] :
            if card not in Player_cardlist.cards :
                Player_cardlist.add_card(card)

    QoL.clear()
    print(QoL.center_justified('Leshy Card List'))
    print()
    print(Leshy_cardlist)
    print()
    print(QoL.center_justified('Player Card List'))
    print()
    print(Player_cardlist)